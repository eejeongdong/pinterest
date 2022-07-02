from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.list import MultipleObjectMixin
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator
from articleapp.models import Article
from subscribapp.models import Subscription
from projectapp.forms import ProjectCreationForm
from projectapp.models import Project


@method_decorator(login_required,'get')
@method_decorator(login_required,'post')
class ProjectCreateView(CreateView):
    model = Project
    template_name = 'projectapp/create.html'
    form_class = ProjectCreationForm

    def get_success_url(self):
        return reverse('projectapp:detail',kwargs={'pk':self.object.pk})


class ProjectDetailView(DetailView, MultipleObjectMixin):
    model = Project
    template_name = 'projectapp/detail.html'
    context_object_name = 'target_project'
    paginate_by = 25

    def get_context_data(self, **kwargs):
        project = self.object
        user = self.request.user

        if user.is_authenticated:
            subscription = Subscription.objects.filter(user=user, project=project)
        else:
            subscription = None

        object_list = Article.objects.filter(project=self.get_object())
        return super(ProjectDetailView, self).get_context_data(object_list=object_list, 
                                                                subscription=subscription,**kwargs)

class ProjectListView(ListView):
    model = Project
    template_name = 'projectapp/list.html'
    context_object_name = 'project_list'
    paginate_by: int = 25