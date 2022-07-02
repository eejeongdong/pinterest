from ast import Mult
from multiprocessing import context
from tempfile import template
from xml.etree.ElementTree import Comment
from django.shortcuts import render
from django.urls import reverse, reverse_lazy

from articleapp.models import Article
from articleapp.forms import ArticleCreationForm
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic import ListView

from django.views.generic.edit import FormMixin
from commentapp.forms import CommentCreationForm

@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ArticleCreateView(CreateView):
  model = Article
  form_class = ArticleCreationForm
  template_name = 'articleapp/create.html'

  def form_valid(self, form):
    temp_article = form.save(commit=False)
    temp_article.writer = self.request.user
    temp_article.save()
    return super().form_valid(form)

  def get_success_url(self):
    return reverse('articleapp:detail', kwargs={'pk':self.object.pk})


class ArticleDetailView(DetailView, FormMixin):
  model = Article
  form_class = CommentCreationForm
  context_object_name = 'target_article'
  template_name = 'articleapp/detail.html'

@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ArticleUpdateView(UpdateView):
  model = Article
  form_class = ArticleCreationForm
  context_object_name = 'target_article'
  template_name = 'articleapp/update.html'

  def get_success_url(self):
    return reverse('articleapp:detail', kwargs={'pk':self.object.pk})


@method_decorator(login_required, 'get')
@method_decorator(login_required, 'post')
class ArticleDeleteView(DeleteView):
  model = Article
  context_object_name = 'target_article'
  template_name = 'articleapp/delete.html'
  success_url = reverse_lazy('articleapp:list')


class ArticleListView(ListView):
  model = Article
  context_object_name = 'article_list'
  template_name = 'articleapp/list.html'
  paginate_by = 3