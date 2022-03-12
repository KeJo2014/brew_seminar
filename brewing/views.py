from django.shortcuts import render
from django.db.models import Count

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
    
        return render(request, 'brewing/evaluate.html', {
            "data": messurement.objects.filter(step=1),
            "steps": steps,
        })
    else:
        steps_number = messurement.objects.values('step').annotate(Count('step')).order_by('step')
        steps = []
        for i in range(steps_number.count()):
            steps.append(i+1)

        step = request.POST.get('step')
        return render(request, 'brewing/evaluate.html', {
            "data": messurement.objects.filter(step=step),
            "steps": steps
        })