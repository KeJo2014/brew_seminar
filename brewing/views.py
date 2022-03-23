from django.shortcuts import render, redirect
from django.db.models import Count
from django.template import engines

from .models import brew_recipe, messurement
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
    if(request.method == "GET"):
        recipes = brew_recipe.objects.all()
        return render(request, 'brewing/home.html',{
            "recipes": recipes,
        })
    else:
        command = request.POST.get('command')
        if(command == "delete"):
            recipe_name = request.POST.get('recipe_name')
            #delete recipe
            brew_recipe.objects.filter(name=recipe_name).delete()
            return render(request, 'brewing/home.html',{
                "recipes": brew_recipe.objects.all(),
            })
    

def brewing(request, recipe_id):
    #check if user is authenticated
    if(request.user.is_authenticated):
        try:
            recipe = brew_recipe.objects.get(id=recipe_id)
        except:
            return render(request, 'brewing/home.html',{
                "recipes": brew_recipe.objects.all(),
                "msg": "Recipe not found",
            })
        return render(request, 'brewing/brewing.html',{
            "recipe": recipe,
        })
    else:
        return redirect('/login')

def create(request): 
    if(request.method == "GET"):
        return render(request, 'brewing/create.html')
    else:
        name = request.POST.get('name')
        date = request.POST.get('date')
        bier_sorte = request.POST.get('sort')
        author = request.POST.get('author')
        ausschlagwuerze = request.POST.get('ausschlagswuerze')
        sudhausausbeute = request.POST.get('sudhausausbeute')
        stamwuerze = request.POST.get('stammwuerze')
        ibu = request.POST.get('bittere')
        ebc = request.POST.get('farbe')
        alcohol = request.POST.get('alkohol')
        description = request.POST.get('beschreibung')
        
        brau_wasser = request.POST.get('json_brauwasser')
        schuettung = request.POST.get('json_schuettung')
        maischplan = request.POST.get('json_maisch')
        wuerze_kochen = request.POST.get('json_wuerze')
        gaerung = request.POST.get('json_gaerung')

        recipe = brew_recipe(name=name, date=date, bier_sorte=bier_sorte, author=author, ausschlagwuerze=ausschlagwuerze, sudhausausbeute=sudhausausbeute, stamwuerze=stamwuerze, ibu=ibu, ebc=ebc, alcohol=alcohol, description=description, brauwasser=brau_wasser, schüttung=schuettung, maischplan=maischplan, wuerzekochen=wuerze_kochen, gärung=gaerung)
        recipe.save()

        return render(request, 'brewing/create.html')

def edit(request, recipe_id):
    if(request.user.is_authenticated):
        try:
            recipe = brew_recipe.objects.get(id=recipe_id)
        except:
            return render(request, 'brewing/home.html',{
                "recipes": brew_recipe.objects.all(),
                "msg": "Recipe not found",
            })
        return render(request, 'brewing/edit.html',{
            "recipe": recipe,
        })
    else:
        name = request.POST.get('name')
        date = request.POST.get('date')
        bier_sorte = request.POST.get('sort')
        author = request.POST.get('author')
        ausschlagwuerze = request.POST.get('ausschlagswuerze')
        sudhausausbeute = request.POST.get('sudhausausbeute')
        stamwuerze = request.POST.get('stammwuerze')
        ibu = request.POST.get('bittere')
        ebc = request.POST.get('farbe')
        alcohol = request.POST.get('alkohol')
        description = request.POST.get('beschreibung')
        
        brau_wasser = request.POST.get('json_brauwasser')
        schuettung = request.POST.get('json_schuettung')
        maischplan = request.POST.get('json_maisch')
        wuerze_kochen = request.POST.get('json_wuerze')
        gaerung = request.POST.get('json_gaerung')

        recipe = brew_recipe(name=name, date=date, bier_sorte=bier_sorte, author=author, ausschlagwuerze=ausschlagwuerze, sudhausausbeute=sudhausausbeute, stamwuerze=stamwuerze, ibu=ibu, ebc=ebc, alcohol=alcohol, description=description, brauwasser=brau_wasser, schüttung=schuettung, maischplan=maischplan, wuerzekochen=wuerze_kochen, gärung=gaerung)
        recipe.save()

        return render(request, 'brewing/edit.html')
    