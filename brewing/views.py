from django.shortcuts import render
from django.db.models import Count
from django.template import engines

from .models import recipe, messurement
# Create your views here.
def index(request):
    return render(request, 'brewing/index.html')

def dashboard(request):
    return render(request, 'brewing/dashboard.html')

def evaluate(request):
    if(request.method == "GET"):
        steps_number = messurement.objects.values('step').annotate(Count('step')).order_by('step')
        steps = []
        for i in range(steps_number.count()):
            steps.append(i+1)

        engine = []
        for mode in messurement.objects.filter(step=1).values('engine'):
            if(mode['engine'] == True):
                engine.append(1)
            else:
                engine.append(0)
    
        return render(request, 'brewing/evaluate.html', {
            "data": messurement.objects.filter(step=1),
            "steps": steps,
            "engine": engine,
        })
    else:
        step = request.POST.get('step')
        steps_number = messurement.objects.values('step').annotate(Count('step')).order_by('step')
        steps = []
        for i in range(steps_number.count()):
            steps.append(i+1)
        
        engine = []
        for mode in messurement.objects.filter(step=step).values('engine'):
            if(mode['engine'] == True):
                engine.append(1)
            else:
                engine.append(0)

        return render(request, 'brewing/evaluate.html', {
            "data": messurement.objects.filter(step=step),
            "steps": steps,
            "engine": engine,
        })

def template(request):
    return render(request, 'brewing/template.html')

def home(request):
    return render(request, 'brewing/home.html')

def brewing(request):
    return render(request, 'brewing/brewing.html')

def create(request):
    return render(request, 'brewing/create.html')