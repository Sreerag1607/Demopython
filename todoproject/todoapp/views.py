from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import TodoForm
from .models import Task
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, DeleteView

# now we are using class instead of function for listview, detailview, updateview, etc
class TaskListView(ListView):
    model = Task
    # template_name is for where this would show
    template_name = 'home.html'
    # this is where all objects had been fetched to task2 and stored in context_object_name
    context_object_name = 'task2'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'detail.html'
    context_object_name = 'task'

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'update.html'
    context_object_name = 'task'
    fields = ('name','priority','date')
    # giving url
    def get_success_url(self):
        return reverse_lazy('cbvdetail',kwargs={'pk':self.object.id})

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('cbvhome')


# Create your views here.
def index(request):
    task2=Task.objects.all()
    if request.method == 'POST':
        name = request.POST.get('task','')
        priority = request.POST.get('priority','')
        date = request.POST.get('date', '')
        task = Task(name=name,priority=priority,date=date)
        task.save()
        return redirect('/')
    return render(request,"home.html",{'task2':task2})

# def detls(request):
#     task=Task.objects.all()
#     return render(request,'detail.html',{'task':task})

def delete(request,taskid):
    task=Task.objects.get(id=taskid)
    if request.method=='POST':
        task.delete()
        return redirect('/')
    return render(request,"delete.html")

def update(request,id):
    task=Task.objects.get(id=id)
    f=TodoForm(request.POST or None,instance=task)
    if f.is_valid():
        f.save()
        return redirect('/')
    return render(request,"edit.html",{'task':task,'f':f})