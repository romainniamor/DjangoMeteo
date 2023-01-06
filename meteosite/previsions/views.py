from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Ville, Departement
from .forms import VilleForm
import logging
from .business.components.meteo_ville_previsions import MeteoVillePrevisions
from .utils.helper.ui_helper import UIHelper




logger = logging.getLogger("previsions")

@login_required(login_url=f'/previsions/login/?next=/previsions/login/')
def index(request):

    logger.debug("entrée dans la view index")

    template = loader.get_template('previsions/index.html')
    context = {}

    logger.warning("context vide")

    logger.info("definition des villes favorites pour l'utilisateur")

    liste_villes_favorites = ['lyon', 'paris', 'nantes']
    request.session['favoris'] = liste_villes_favorites
    return HttpResponse(template.render(context, request))

def departements(request):

    # on obtient ici toutes les villes dont la clée étrangère est égale à 1
    #
    # ce qui correspond à la requête SQL :
    # select * from ville where id_departement = 1
    villes_du_departement = Ville.objects.filter(id_departement=1).order_by('nom')
    nom_departement = "Ain"

    paginator = Paginator(villes_du_departement, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # maintenant que nous avons les données, nous allons les associer
    # au context. Ainsi le Template pourra les utiliser pour générer l'affichage
    # avec les données.
    context = {
        'villes_du_departement': villes_du_departement,
        'nom_departement': nom_departement,
        'page_obj': page_obj,
    }

    # nous pouvons utiliser un objet template pour générer l'affichage puis
    # le retourner via un objet HttpResponse mais... django propose
    # une methode 'render' qui le fait pour nous, alors utilisons la :-)
    return render(request, 'previsions/departements.html', context)



def select_departement(request):

    liste_departements = Departement.objects.all()

    context = {
        'liste_departements': liste_departements,
    }

    return render(request, 'previsions/select_departement.html', context)

def display_villes(request):

    id_departement = request.POST['id_departement']

    departement = Departement.objects.get(pk=id_departement)
    villes_du_departement = Ville.objects.filter(id_departement=id_departement).order_by('nom')
    paginator = Paginator(villes_du_departement, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    context = {
        'villes_du_departement': villes_du_departement,
        'departement': departement,
        'page_obj': page_obj,

    }
    return render(request, 'previsions/display_villes.html', context)

def add_ville(request):
    save_error = False
    is_create = True

    if request.method == 'POST':
        is_create = False

        form = VilleForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            code_postal = form.cleaned_data['code_postal']
            departement = form.cleaned_data['departement']

            try:
                print("enregistrement de la ville en 800")
                ville = Ville()
                ville.nom = nom
                ville.code_postal = code_postal
                ville.id_departement = departement
                ville.save()
                print('enregistrement ok')

                form = VilleForm()

            except:
                save_error = True

    else:
        form = VilleForm()

    return render(request, 'previsions/add_ville.html', {'form': form, 'save_error': save_error, 'is_create': is_create})

def favoris(request):
    liste_villes_favorites = request.session['favoris']
    context = {
        'favoris': liste_villes_favorites,
    }

    return render(request, 'previsions/favoris.html', context)


def display_previsions_ville(request):
    # on récupère la ville provenant du formulaire
    nom_ville = request.POST['ville']

    # on récupère les prévisions associées à la ville depuis la couche business
    meteo_ville_previsions = MeteoVillePrevisions(nom_ville)

    previsions_jour = meteo_ville_previsions.get_previsions_jour()
    previsions_force_vent = meteo_ville_previsions.get_previsions_force_vent()
    previsions_description = meteo_ville_previsions.get_previsions_description()

    # on construit une liste contenant des dictionnaires afin de pouvoir utiliser
    # les données dans le template
    #
    # /!\ la manipulation des éléments Python dans le template n'est pas du pure Python,
    #     c'est une syntaxe propre au langage de template de Django
    #
    #     ainsi, pour consulter dans la template une information de dictionnaire,
    #     on utilisera le "." pour définir la clé.
    #
    #     ce qui donne dans le code python
    #     ma_variable[ma_cle] = "valeur"
    #
    #     et dans le template, accédera à la valeur ainsi :
    #     {{ ma_variable.ma_cle }}

    previsions_affichage = []
    for jour in range(7):
        prevision_jour = {}
        prevision_jour["temperature"] = previsions_jour[jour]
        prevision_jour["force_vent"] = previsions_force_vent[jour]
        prevision_jour["description"] = previsions_description[jour]
        prevision_jour["jour"] = UIHelper.day_of_the_week_from_period(jour)
        prevision_jour["icon"] = "previsions/images/" + UIHelper.image_from_weather_status(previsions_description[jour])

        previsions_affichage.append(prevision_jour)

    context = {
        'ville': nom_ville,
        'previsions_affichage': previsions_affichage,
    }

    return render(request, 'previsions/display_previsions_ville.html', context)


