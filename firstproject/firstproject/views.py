from django.shortcuts import render, HttpResponse
from tuition.models import Contact
from django.views.generic import TemplateView
def home(request):
    name=['Sajeeb','Shanto','Molla','Tamanna']
    context={
        'name':name,
    }
    return render(request,'home.html',context)
class HomeView(TemplateView):
    template_name='home.html'
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['msg']='Welcome to our Website'
        return context
        
        

        