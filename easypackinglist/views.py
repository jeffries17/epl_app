from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from django.db.models import Q
import json
import os
import pandas as pd
from .models import Trip, Item
from django.utils.timezone import now

DEFAULT_CATEGORIES = ['clothing', 'documents', 'medication', 'toiletries', 'footwear', 'tech', 'snacks', 'etc']

def home(request):
    # Reading template names from the JSON file
    with open('easypackinglist/template_lists.json', 'r') as file:
        templates_data = json.load(file)
    template_names = [template["template_name"] for template in templates_data]
    
    # Querying the database for the count of all trips
    trip_count = Trip.objects.count()

    # Pass both the trip count and template names to the template
    context = {
        'templates': template_names,
        'trip_count': trip_count
    }
    return render(request, 'home.html', context)

@login_required
def handle_post_request(request, trip_uuid):
    if trip_uuid:
        trip = update_trip(request, trip_uuid)
    else:
        trip = create_trip(request)
    
    handle_items(request, trip)
    messages.success(request, "List saved successfully!")
    return HttpResponseRedirect(request.path_info)

@login_required
def create_trip(request):
    trip_name = request.POST.get('name')
    destination_city = request.POST.get('destination_city')
    start_date = request.POST.get('start_date')
    user = request.user
    selected_template_name = request.POST.get('template_name', 'default')
    print("Template Name Received for Create:", selected_template_name)  # Debugging line
    image_path = f'trip_images/{selected_template_name}_background.jpg'
    
    trip = Trip.objects.create(
        user=user, name=trip_name, destination=destination_city,
        start_date=start_date, image=image_path
    )
    return trip

@login_required
def update_trip(request, trip_uuid):
    trip = get_object_or_404(Trip, uuid=trip_uuid, user=request.user)
    trip.name = request.POST.get('name')
    trip.destination = request.POST.get('destination_city')
    trip.start_date = request.POST.get('start_date')
    selected_template_name = request.POST.get('template_name', 'default')
    print("Template Name Received for Update:", selected_template_name)  # Debugging line
    trip.image = f'trip_images/{selected_template_name}_background.jpg'
    trip.save()
    return trip

@login_required
def handle_items(request, trip):
    items_to_pack = json.loads(request.POST.get('items_to_pack', '[]'))
    items_packed = json.loads(request.POST.get('items_packed', '[]'))

    print("Items to pack:", items_to_pack)
    print("Items packed:", items_packed)

    # First, update or create all mentioned items
    all_items = {item['name']: item for item in items_to_pack + items_packed}
    for name, item_data in all_items.items():
        is_packed = item_data in items_packed
        Item.objects.update_or_create(
            trip=trip, name=name,
            defaults={
                'category': item_data['category'].replace('toPackList-', '').replace('packedList-', ''),
                'is_packed': is_packed
            }
        )

    # Delete items that are no longer mentioned
    existing_item_names = set(Item.objects.filter(trip=trip).values_list('name', flat=True))
    items_mentioned = set(all_items.keys())
    items_to_delete = existing_item_names - items_mentioned
    Item.objects.filter(trip=trip, name__in=items_to_delete).delete()


def load_default_data(trip_uuid):
    if not trip_uuid:
        template_file_path = os.path.join(settings.BASE_DIR, 'easypackinglist', 'template_lists.json')
        with open(template_file_path, 'r') as file:
            templates_data = json.load(file)

        passport_file_path = os.path.join(settings.BASE_DIR, 'easypackinglist', 'passport_all.csv')
        visa_requirements_df = pd.read_csv(passport_file_path)
        countries = sorted(set(visa_requirements_df['Passport'].unique()) | set(visa_requirements_df['Destination'].unique()))
        visa_requirements = visa_requirements_df.to_dict(orient='records')
        return templates_data, countries, visa_requirements
    return {}, [], []

@login_required
def packing_list(request, trip_uuid=None):
    trip = None
    if request.method == 'POST':
        post_trip_uuid = request.POST.get('trip_uuid', None)
        return handle_post_request(request, post_trip_uuid)

    categories, to_pack, packed = set(), {}, {}
    selected_template_name = request.GET.get('template')
    templates_data, countries, visa_requirements = load_default_data(trip_uuid)

    selected_template = next((item for item in templates_data if item["template_name"] == selected_template_name), None)
    if selected_template:
        categories, to_pack, packed = setup_packing_lists(selected_template)

    if trip_uuid:
        trip, categories, to_pack, packed = setup_existing_trip(request, trip_uuid, categories)

    return render(request, 'packing_list.html', {
        'trip': trip,
        'countries': countries, 
        'categories': sorted(categories),
        'selected_template_name': selected_template_name,
        'selected_template': selected_template,
        'visa_requirements': visa_requirements,
        'lists': {'to_pack': to_pack, 'packed': packed},
    })

def setup_packing_lists(selected_template):
    categories = DEFAULT_CATEGORIES.copy()
    to_pack = {category: [] for category in categories}
    packed = {category: [] for category in categories}

    for category, items in selected_template.items():
        if category != "template_name" and category in categories:
            to_pack[category].extend(items)

    return categories, to_pack, packed

def setup_existing_trip(request, trip_uuid, categories):
    trip = get_object_or_404(Trip, uuid=trip_uuid, user=request.user)
    items = Item.objects.filter(trip=trip)
    categories = DEFAULT_CATEGORIES.copy()
    to_pack = {category: [] for category in categories}
    packed = {category: [] for category in categories}

    for item in items:
        category = item.category
        if category in categories:
            if item.is_packed:
                packed[category].append(item.name)
            else:
                to_pack[category].append(item.name)
        else:  
            if category not in to_pack:
                to_pack[category] = []
                packed[category] = []
            if item.is_packed:
                packed[category].append(item.name)
            else:
                to_pack[category].append(item.name)

    return trip, categories, to_pack, packed

@login_required
def user_trips_view(request):
    # Filter trips by the current user, and possibly other criteria such as start_date
    in_progress_trips = Trip.objects.filter(user=request.user, start_date__gte=now()).order_by('start_date')

    return render(request, 'my_trips.html', {'in_progress_trips': in_progress_trips})

@login_required
@require_POST
def delete_trip(request, trip_uuid):
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Optionally, handle non-AJAX request differently or return an error
        return HttpResponseBadRequest('Invalid request')

    trip = get_object_or_404(Trip, uuid=trip_uuid, user=request.user)  # Ensure the trip belongs to the logged-in user

    # Attempt to delete the trip
    try:
        trip.delete()
        return JsonResponse({'message': 'Trip deleted successfully'})
    except Exception as e:
        # Log the error, inform the user, or handle the exception as needed
        return JsonResponse({'error': str(e)}, status=500)
    
def about(request):
    return render(request, 'about.html')