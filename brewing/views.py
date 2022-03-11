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
        for i in range(steps_number[0]['step']):
            steps.append(i+1)
        
        dates_ = messurement.objects.all()
        dates = {
            "real": [],
            "pretty": []
        }
        for i in dates_:
            d = i.time.strftime("%d/%m/%Y")
            if(d not in dates):
                dates["real"].append(i.time)
                dates["pretty"].append(i.time.strftime("%d/%m/%Y"))
        minutes = []
        for i in range(len(dates)):
            minutes.append(messurement.objects.get(time=dates["real"][i]).time.strftime("%H:%M:%S"))
        print(minutes)
        
        return render(request, 'brewing/evaluate.html', {
            "data": messurement.objects.filter(step=1),
            "dates": dates,
            "steps": steps,
            "minutes": minutes
        })
    else:
        steps_number = messurement.objects.values('step').annotate(Count('step')).order_by('step')
        steps = []
        for i in range(steps_number[0]['step']):
            steps.append(i+1)
        
        dates_ = messurement.objects.all()
        dates = []
        for i in dates_:
            d = i.time.strftime("%d/%m/%Y")
            if(d not in dates):
                dates.append(d)

        step = request.POST.get('step')
        date = request.POST.get('date')
        return render(request, 'brewing/evaluate.html', {
            "data": messurement.objects.filter(step=step, time=date),
            "dates": dates,
            "steps": steps
        })