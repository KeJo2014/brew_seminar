from django.shortcuts import render, redirect
from django.db.models import Count
from django.template import engines

from .models import brew_recipe, messurement
from .process.brew_server import brew_server

brew_system = brew_server()
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
            steps.append(i+2)

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
            steps.append(i+2)
        
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

# def template(request):
#     return render(request, 'brewing/template.html')

def home(request):
    order_by = request.GET.get('order_by', 'name')
    recipes = brew_recipe.objects.all().order_by(order_by);
    return render(request, 'brewing/home.html',{
        "recipes": recipes,
    })
    
def delete(request, recipe_id):
    brew_recipe.objects.get(id=recipe_id).delete()
    return redirect('home')

def brewing(request):
    #check if user is authenticated
    if(True):       #request.user.is_authenticated
        if(request.method == "GET"):
            if(brew_system.get_recipe() != None):
                recipe = brew_recipe.objects.get(id=brew_system.get_recipe())
                return render(request, 'brewing/brewing.html', {
                    "recipe": recipe,
                    "status": brew_system.get_status(),
                })
            else:
                return render(request, 'brewing/home.html',{
                    "recipes": brew_recipe.objects.all(),
                    "msg": "You have to select a recipe first!",
                })
        else:
            print(request.POST)
            if(request.POST.get('command') == "set_recipe_id"):
                brew_system.set_recipe(request.POST.get('recipe_id'))
                return redirect('/brewing')
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
    if(request.method == "GET"):
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
        recipe = brew_recipe.objects.get(id=recipe_id)
        recipe.name = request.POST.get('name')
        recipe.date = request.POST.get('date')
        recipe.bier_sorte = request.POST.get('sort')
        recipe.author = request.POST.get('author')
        recipe.ausschlagwuerze = request.POST.get('ausschlagswuerze')
        recipe.sudhausausbeute = request.POST.get('sudhausausbeute')
        recipe.stamwuerze = request.POST.get('stammwuerze')
        recipe.ibu = request.POST.get('bittere')
        recipe.ebc = request.POST.get('farbe')
        recipe.alcohol = request.POST.get('alkohol')
        recipe.description = request.POST.get('beschreibung')
        
        recipe.brau_wasser = request.POST.get('json_brauwasser')
        recipe.schuettung = request.POST.get('json_schuettung')
        recipe.maischplan = request.POST.get('json_maisch')
        recipe.wuerze_kochen = request.POST.get('json_wuerze')
        recipe.gaerung = request.POST.get('json_gaerung')
        recipe.save()

        return redirect('home')
    