from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import ArticleForms, CommentForm
from .models import Article, Like


class AuthorArticleView(ListView):
    model = Article
    template_name = 'author_articles.html'
    context_object_name = 'posts'


class EditPageView(ListView):
    model = Article
    template_name = 'edit_page.html'
    context_object_name = 'post_list'


class HomeListView(ListView):
    model = Article
    template_name = 'home_page.html'
    context_object_name = 'list_article'


class HomeDetailView(FormMixin, DetailView):
    model = Article
    template_name = 'detail.html'
    context_object_name = 'get_article'
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.article = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('detail_page', kwargs={'pk': self.get_object().id})

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.count_view += 1
        self.object.save()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login_page')
    model = Article
    template_name = 'create.html'
    form_class = ArticleForms
    success_url = reverse_lazy('edit_page')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login_page')
    model = Article
    template_name = 'update_form.html'
    form_class = ArticleForms
    success_url = reverse_lazy('edit_page')
    ''' 
        Переопределил метод для ограничения прав на редактирование постов
        Если текущий пользователь не является автором постов
        будет выводиться 403 ошибка
        т.к. это не совсем удобно, поэтому в шаблоне, используя синтаксис jinja
        ограничил доступ к ссылкам на редактирование постов

    '''

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user != kwargs['instance'].author:
            return self.handle_no_permission()
        return kwargs


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    template_name = 'edit_page.html'
    success_url = reverse_lazy('edit_page')

    def post(self, request, *args, **kwargs):
        return super().post(request)

    ''' 
        Переопределили метод для ограничения прав на удаление постов
        Если текущий пользователь не является автором постов
        будет выводиться 403 ошибка
        т.к. это не совсем удобно, поэтому в шаблоне, используя синтаксис jinja
        ограничил доступ к ссылкам на удаление постов
    
    '''

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.request.user != self.object.author:
            return self.handle_no_permission()

        success_url = self.get_success_url()
        self.object.delete()

        return HttpResponseRedirect(success_url)


class LikeView(ListView):
    model = Like

    def post(self, request, *args, **kwargs):
        user = request.user
        if request.method == 'POST':
            post_id = request.POST.get('post_id')
            post_obj = Article.objects.get(id=post_id)

            if user in post_obj.liked.all():
                post_obj.liked.remove(user)
            else:
                post_obj.liked.add(user)
            like, created = Like.objects.get_or_create(user=user, post_id=post_id)
            if not created:
                if like.value == 'Like':
                    like.value = 'Unlike'
                else:
                    like.value = 'Like'
            like.save()
        return redirect('home')
