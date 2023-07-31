from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blog.forms import AddBlogForm, UpdateBlogForm
from blog.models import Blog


class BlogListView(ListView):
    model = Blog
    extra_context = {
        'title': 'Блог'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff or self.request.user.groups.filter(name='moderators').exists():
            return queryset
        else:
            queryset = queryset.filter(is_published=True)
        return queryset


class BlogDetailView(DetailView):
    model = Blog

    def get_context_data(self, *args, **kwargs):
        blog = Blog.objects.get(pk=self.object.pk)
        blog.count_views += 1
        blog.save()
        context = super().get_context_data(*args, **kwargs)
        context['title'] = context['object']
        return context


class BlogCreateView(PermissionRequiredMixin, CreateView):
    model = Blog
    permission_required = ['blog.add_blog']
    extra_context = {
        'title': 'Добавить пост'
    }
    form_class = AddBlogForm


class BlogUpdateView(PermissionRequiredMixin, UpdateView):
    model = Blog
    permission_required = ['blog.change_blog']
    form_class = UpdateBlogForm

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = context['object']
        return context


class BlogDeleteView(PermissionRequiredMixin, DeleteView):
    model = Blog
    permission_required = ['blog.delete_blog']
    success_url = reverse_lazy('blog:blogs')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = context['object']
        return context
