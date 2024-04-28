from django.http import HttpResponse

def home(request):
    return HttpResponse("Hello, world. Let's get packing.")