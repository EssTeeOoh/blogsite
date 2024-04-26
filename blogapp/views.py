from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment, Profile
from .forms import PostForm, UpdateForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django import forms



'''
def index(request):
    return render(request, 'home.html', {})
'''

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('single-post', args= [str(pk)]))


class IndexView(ListView):
    model = Post
    template_name = 'index.html'

    def get_queryset(self):
        return Post.objects.all().order_by('-post_date', '-post_time')

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(IndexView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

def CategoryView(request, cats):
    category_posts = Post.objects.filter(category = cats)
    return render(request, 'categories.html', {'cats':cats.title(), 'category_posts':category_posts})

class SinglePostView(DetailView):
    model = Post
    template_name = 'single-post.html'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(SinglePostView, self).get_context_data(*args, **kwargs)

        stuff = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = stuff.total_likes()

        liked = False
        if stuff.likes.filter(id=self.request.user.id).exists():
            liked = True

        
        context["cat_menu"] = cat_menu
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context
    
    
    

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    #fields = '__all__'

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'
    #fields = '__all__'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        comment = form.save(commit=False)
        if self.request.user.is_authenticated:
            comment.user = Profile.objects.get(user=self.request.user)
            comment.author_name = None  # Or set to None, as you prefer
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy( 'single-post', kwargs={'pk':self.kwargs['pk']})
    
    def get_form(self, form_class=None):
        form = super(AddCommentView, self).get_form(form_class)
        if self.request.user.is_authenticated:
            form.fields['name'].widget = forms.HiddenInput()
            form.fields['name'].required = False
        return form
    
    
    

class AddCategorytView(CreateView):
    model = Category
    #form_class = PostForm
    template_name = 'add_category.html'
    fields = '__all__'

class UpdatePostView(UpdateView):
    model = Post
    form_class = UpdateForm
    template_name = 'update_post.html'
    #fields = ['title', 'title_tag', 'body']

class DeletePostView(DeleteView):
    model = Post
    template_name = "delete_post.html"
    success_url = reverse_lazy('index')
