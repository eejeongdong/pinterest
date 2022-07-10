
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import RedirectView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from articleapp.models import Article
from likeapp.models import Like
from django.contrib import messages
# Create your views here.


@method_decorator(login_required , 'get')
class LikeArticleView(RedirectView):
  def get_redirect_url(self, *args, **kwargs):
    return reverse('articleapp:detail', kwargs={'pk': kwargs['pk']})

  def get(self, *args, **kwargs):
    user = self.request.user
    article = get_object_or_404(Article, pk=kwargs['pk'])
    like = Like.objects.filter(user=user, article=article)

    if like.exists():
      like.delete()
      article.like -= 1
      article.save()
      messages.add_message(self.request, messages.SUCCESS, '좋아요 취소')

    else:
      Like(user=user, article=article).save()
      article.like += 1
      article.save()
      messages.add_message(self.request, messages.SUCCESS, '좋아요')


    return super(LikeArticleView, self).get(self.request, *args, **kwargs)