from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import RedirectView, ListView
from django.contrib.auth.decorators import login_required
from articleapp.models import Article
from subscribapp.models import Subscription
from projectapp.models import Project


# Create your views here.

@method_decorator(login_required, 'get')
class SubscriptionView(RedirectView):

    def get_redirect_url(self,*args, **kwargs):
        return reverse('projectapp:detail',kwargs={'pk':self.request.GET.get('project.pk')})
        
    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.request.GET.get('project.pk'))
        user = self.request.user

        subscription = Subscription.objects.filter(project=project, user=user)

        if subscription.exists():
            subscription.delete()
        else:
            Subscription(user=user, project=project).save()

        return super(SubscriptionView, self).get(request, *args, **kwargs)

@method_decorator(login_required, 'get')
class SubscriptionListView(ListView):
    model = Article
    template_name = 'subscribapp/list.html'
    context_object_name = 'article_list'
    paginate_by = 5

    def get_queryset(self):
        projects = Subscription.objects.filter(user=self.request.user).values_list('project')
        article_list = Article.objects.filter(project__in=projects)
        return article_list