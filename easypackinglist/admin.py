from django.contrib import admin
from .models import Trip, Item, Category

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'start_date', 'end_date', 'user')
    # Add more options as needed

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'trip', 'is_packed')
    # Add more options as needed

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    # Add more options as needed