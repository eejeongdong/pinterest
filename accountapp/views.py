from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse, reverse_lazy # reverse = 함수형 뷰, reverse_lazy = 클래스형 뷰에서 사용
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from accountapp.forms import AccountUpdateForm
from accountapp.decorators import account_ownership_required

from django.views.generic.list import MultipleObjectMixin

from articleapp.models import Article
from articleapp.views import ArticleDetailView

# Create your views here.

has_ownership = [account_ownership_required, login_required]



class AccountCreateView(CreateView):
  model = User
  form_class = UserCreationForm
  success_url = reverse_lazy('articleapp:list')
  template_name = 'accountapp/create.html'

class AccountDetailView(DetailView, MultipleObjectMixin):
  model = User
  context_object_name = 'target_user'
  template_name = 'accountapp/detail.html'
  paginate_by: int = 25

  def get_context_data(self, **kwargs):
    object_list = Article.objects.filter(writer=self.get_object())
    return super(AccountDetailView, self).get_context_data(object_list=object_list, **kwargs)


@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountUpdateView(UpdateView):
  model = User
  form_class = AccountUpdateForm
  success_url = reverse_lazy('articleapp:list')
  context_object_name = 'target_user'
  template_name = 'accountapp/update.html'




@method_decorator(has_ownership, 'get')
@method_decorator(has_ownership, 'post')
class AccountDeleteView(DeleteView):
  model = User
  success_url = reverse_lazy('accountapp:login')
  context_object_name = 'target_user'
  template_name = 'accountapp/delete.html'

