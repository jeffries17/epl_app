from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_on', 'updated_on')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'created_on'
    ordering = ('-created_on',)
    fields = ('title', 'slug', 'author', 'content', 'meta_description', 'featured_image', 'tags')

admin.site.register(Post)