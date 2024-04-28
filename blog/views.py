from django.views.generic import ListView, DetailView
from .models import Post

class BlogListView(ListView):
    model = Post
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'
    paginate_by = 10  # Add pagination to handle multiple posts

class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/blog_detail.html'
    slug_field = 'slug'  # Specifies which field in the model corresponds to the slug in the URL
    slug_url_kwarg = 'slug'  # Specifies that the URLconf looks for a slug parameter named 'slug'


