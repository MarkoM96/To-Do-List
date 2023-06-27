from django.shortcuts import render ,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from .models import Task


# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')
    

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = "base/task_list.html" 
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete = False).count()
        return context
    


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "base/task.html" 
    context_object_name = "task"
    # default context_object_name je object

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "base/task_form.html" 
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "base/task_form.html" #ovo task_form je i po defaultu
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "base/task_delete.html"
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')


# u slucaju da nisam definisao template_name, django bi po defaultu trazio template(html fajl) po nazivu klase
# odnosno task_list(TaskList), moze i bez definisanja ali bolje je navesti!
# detail_view sluzi da bi videli detalje neke liste
# Update view smo iskoristili da nas odvede do istog Podsetnika i omoguci nam da ga promenimo