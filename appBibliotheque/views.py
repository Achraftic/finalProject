from django.shortcuts import render,redirect,get_object_or_404
from appBibliotheque.models import Livre,Emprunter,Exemplaire
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator 
from accounts.models import Utilisateur

def home(request):
    livres = Livre.objects.order_by('id')
    paginator = Paginator(livres, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request,'appBibliotheque/user/home.html',{'page_obj' : page_obj })
# @login_required
def rechercher_livre(request):
    query = request.GET.get('titre')
    livres = []
    message=""
    if query:
        livres = Livre.objects.filter(titre__icontains=query)
        paginator = Paginator(livres, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    else:
        message = "No search query provided."

    return render(request, 'appBibliotheque/user/home.html', {'page_obj': page_obj if query else None, 'query': query, 'message': message})
      
def detail_livre(request,slug):
    livre = get_object_or_404(Livre,slug=slug)
    return render(request,'appBibliotheque/user/unLivre.html',{"livre_detail":livre})

def emprunter_exemplaire(request, slug):
    livre = get_object_or_404(Livre, slug=slug)
    message = ""
    # Vérifier si l'utilisateur a déjà emprunté ce livre
    utilisateur = request.user 
    if Emprunter.objects.filter(utilisateur=utilisateur, exemplaire__livre=livre).exists():
        message = f"Vous avez déjà emprunté le livre '{livre.titre}'."
    else:
        # Vérifier si des exemplaires sont disponibles
        exemplaires_disponibles = Exemplaire.objects.filter(livre=livre, disponible=True)
        if exemplaires_disponibles.exists():
            exemplaire = exemplaires_disponibles.first()
            # Créer un nouvel emprunt
            emprunt = Emprunter.objects.create(exemplaire=exemplaire, utilisateur=utilisateur)
            emprunt.save()
            # Mettre à jour la disponibilité de l'exemplaire
            exemplaire.disponible = False
            exemplaire.save()
            message = f"L'exemplaire du livre '{livre.titre}' a été emprunté avec succès."
        else:
            message = f"Aucun exemplaire disponible pour le livre '{livre.titre}'."
    
    return render(request, 'appBibliotheque/user/home.html', {'livre': livre, 'message': message})


def liste_livres(request):
    livres = Livre.objects.all()
    return render(request,'appBibliotheque/dashboard/livre.html',{'livres' : livres })

def page_ajout(request):
    return render(request, 'appBibliotheque/dashboard/ajouter.html')

def edit_livre(request,id):
    livre = get_object_or_404(Livre,id=id)
    return render(request,'appBibliotheque/dashboard/edit.html',{'livre' : livre })

def update_livre(request, id):
    livre = get_object_or_404(Livre, id=id)
    if request.method == 'POST':
        titre = request.POST.get('titre')
        auteur = request.POST.get('auteur')
        isbn = request.POST.get('isbn')
        categories = request.POST.get('categories')
        description = request.POST.get('description')
        image_couverture = request.FILES.get('image_couverture')

        livre.titre = titre
        livre.auteur = auteur
        livre.isbn = isbn
        livre.categories = categories
        livre.description = description
        if image_couverture:
            livre.image_couverture = image_couverture
        livre.save()

        messages.success(request, "Le livre a été mis à jour avec succès.")
        return redirect('liste_livres')

    return render(request, 'appBibliotheque/dashboard/edit.html', {'livre': livre})


def ajouter_livre(request):
    livres = Livre.objects.all()
    if request.method == 'POST':
        titre = request.POST.get('titre')
        auteur = request.POST.get('auteur')
        isbn = request.POST.get('isbn')
        categories = request.POST.get('categories')
        description = request.POST.get('description')
        image_couverture = request.FILES.get('image_couverture')
        livre = Livre(titre=titre, auteur=auteur, isbn=isbn,categories=categories, description=description, image_couverture=image_couverture)
        if titre and auteur and isbn and description and image_couverture:
            livre.save()
            messages.success(request, "Le livre a été ajouté avec succès.")
            return render(request,'appBibliotheque/dashboard/ajouter.html',{'livres' : livres })  # Assurez-vous que 'acceuileBli' est correct
        else:
            messages.error(request, "Le formulaire n'est pas valide. Veuillez corriger les erreurs.")
    else:
       return render(request, 'appBibliotheque/dashboard/ajouter.html', {'livres' : livres })
   
   
def supprimer_exemplaire(request,id):
    
    livre = get_object_or_404(Livre,id=id)
    exemplaires = Exemplaire.objects.filter(livre=livre,disponible = True)
    if exemplaires.exists():
        exemplaire = exemplaires.first()
        exemplaire.delete()
        return redirect('liste_livres')
    else:
        return redirect('liste_livres')
def ajouter_exemplaire(request, id):
    livre = get_object_or_404(Livre,id=id)
    exemplaire = Exemplaire.objects.create(livre = livre, disponible=True)
    exemplaire.save()
    return redirect('liste_livres')

def detailLivre(request,id):
    livre = get_object_or_404(Livre,id=id)
    exemplaires = Exemplaire.objects.filter(livre=livre)#disponible = True
    return render(request,'appBibliotheque/dashboard/detailLivre.html',{'livre':livre,'exemplaires':exemplaires })

def page_UnLivre(request):
    return render(request,'appBibliotheque/user/unLivre.html')

def filterLivre(request,genre):
    if(genre=="all"):
         livres = Livre.objects.order_by('id')
    else:
       livres = Livre.objects.order_by('id').filter(categories__icontains=genre)
    
    paginator = Paginator(livres, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
   
    return render(request,'appBibliotheque/user/home.html', {'genre': genre, 'page_obj': page_obj}) 

def dashboard(request):
    nbUsers = Utilisateur.objects.all().filter(est_bibliothecaire=False).count()
    nbLivres=Livre.objects.all().count()
    nbEmpruntes=Emprunter.objects.all().count()
    nbExemplairePerdu=Exemplaire.objects.all().filter(perdu=True).count()
    context={
        "nbUsers":nbUsers,
         "nbLivres":nbLivres,
         "nbEmpruntes":nbEmpruntes,
         "nbExemplairePerdu":nbExemplairePerdu
    }
    return render(request,'appBibliotheque/dashboard/dashboard.html',context)