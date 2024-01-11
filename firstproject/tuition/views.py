from django.db.models.base import Model
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.template import context
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import Class_in, Contact,Post,Subject
from .forms import ContactForm,PostForm
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib import messages
from django.db.models import Q, query
def search(request):
    query=request.POST.get('search','')
    if query:
        queryset=(Q(title__icontains=query)) | (Q(details__icontains=query)) | (Q(medium__icontains=query)) | (Q(category__icontains=query)) | (Q(subject__name__icontains=query)) | (Q(class_in__name__icontains=query))
        results= Post.objects.filter(queryset).distinct()
    else:
        results=[]
    context ={
        'results':results
    }
    return render(request, 'tuition/search.html',context)
    
def filter(request):
    print("filter")
    if request.method=="POST":
        subject=request.POST['subject']
        class_in=request.POST['class_in']
        salary_from=request.POST['salary_from']
        salary_to=request.POST['salary_to']
        available=request.POST['available']
        print(subject, class_in)
        if subject or class_in:
            queryset=(Q(subject__name__icontains=subject)) & (Q(class_in__name__icontains=class_in)) 
            results= Post.objects.filter(queryset).distinct()
            if available:
                results=results.filter(available=True)
            if salary_from:
                results=results.filter(salary__gte=salary_from)
            if salary_to:
                results=results.filter(salary__lte=salary_to)

        else:
            results=[]
        
        context ={
        'results':results
        }
        return render(request, 'tuition/search.html',context)

class ContactView(FormView):
    form_class=ContactForm
    template_name='contact.html'
    #success_url='/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request,'Form Successfully Submited')
        return super().form_valid(form)
    def form_invalid(self, form):
        return super().form_invalid(form)
    def get_success_url(self):
        return reverse_lazy('homeview')
      

#class ContactView(View):
#    form_class=ContactForm
 #   template_name='contact.html'
  #  def get(self,request,*args,**kwargs):
#     form=self.form_class
 #       return render(request,self.template_name,{'form':form})
#  def post(self,request,*args,**kwargs):
#       form=self.form_class(request.POST)
#       if form.is_valid():
#           form.save()
 #           return HttpResponse("Success")
  #      return render(request,self.template_name,{'form':form})

# Create your views here.
def contact(request):
    initials={
        'name': 'My name is ',
        'phone':'+880',
        'content':'My content is '
    }
    if request.method=="POST":
        form=ContactForm(request.POST,initial=initials)
        if form.is_valid():
            form.save()
    else:
        form=ContactForm(initial=initials)   
    return render(request,'contact.html',{'form':form})
from django.views.generic import ListView
#class PostListView(ListView):
    #template_name='tuition/postlist.html'
    #queryset=Post.objects.all()
   # context_object_name='posts'
    #def get_context_data(self,*args, **kwargs):
     #   context=super().get_context_data(*args,**kwargs)
      #  context['posts']=context.get('object_list')
       # context['msg']="This is Postlist"
        #return context

class PostListView(ListView):
    template_name='tuition/postlist.html'
    queryset=Post.objects.all()
    context_object_name='posts'
    def get_context_data(self,*args, **kwargs):
        context=super().get_context_data(*args, **kwargs)
        posts=context.get('object_list')
        context['posts']= posts
        context['subjects']= Subject.objects.all()
        context['classes']= Class_in.objects.all()
        return context


from django.views.generic import DetailView
class PostDetailView(DetailView):
    model=Post
    template_name='tuition/postdetail.html'


def postview(request):
    post=Post.objects.all()
    return render(request,'tuition/postview.html',{'post':post})

def subview(request):
    sub=Subject.objects.get(name="Physics")
    post=sub.subject_set.all()
    return render(request,'tuition/subjectview.html',{'sub':sub,'post':post})

class PostCreateView(CreateView):
    model=Post
    form_class=PostForm
    template_name='tuition/postcreate.html'
    #success_url='/'
    def form_valid(self, form):
        form.instance.user=self.request.user
        return super().form_valid(form)
    def get_success_url(self):
       # id=self.object.id
        return reverse_lazy('tuition:subjects')
from django.views.generic import UpdateView,DeleteView
class PostEditView(UpdateView):
    model=Post
    form_class=PostForm
    template_name='tuition/postcreate.html'
    def get_success_url(self):
           id=self.object.id
           return reverse_lazy('tuition:postdetail',kwargs={'pk':id})

class PostDeleteView(DeleteView):
    model=Post
    template_name='tuition/delete.html'
    success_url=reverse_lazy('tuition:postlist')

def postcreate(request):
    if request.method=="POST":
        form=PostForm(request.POST,request.FILES )
        if form.is_valid():
            obj=form.save(commit=False)
            obj.user=request.user
            obj.save()
            sub=form.cleaned_data['subject']
            for i in sub:
                obj.subject.add(i)
                obj.save()
            class_in=form.cleaned_data['class_in']
            for i in class_in:
                obj.class_in.add(i)
                obj.save()
            return HttpResponse("Success")
    else:
        form=PostForm()
    return render(request,'tuition/postcreate.html',{'form':form})
