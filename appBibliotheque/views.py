from django.shortcuts import render,redirect,get_object_or_404
from appBibliotheque.models import Livre,Emprunter,Exemplaire,DemandeEmprunt
from django.contrib import messages
from django.core.mail import BadHeaderError,send_mail
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator 
from accounts.models import Utilisateur
from datetime import datetime
def get_paginated_books(request, livres):
    paginator = Paginator(livres, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj

def home(request):
    livres = Livre.objects.order_by('id')
    page_obj = get_paginated_books(request, livres)
    return render(request, 'appBibliotheque/user/home.html', {'page_obj': page_obj})

def rechercher_livre(request):
    query = request.GET.get('titre')
    livres = Livre.objects.filter(titre__icontains=query) if query else []
    page_obj = get_paginated_books(request, livres)
    message = "No search query provided." if not query else ""
    return render(request, 'appBibliotheque/user/home.html', {'page_obj': page_obj, 'query': query, 'message': message})  


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
   
    query = request.GET.get('nom')
    
   
    message=""
    if query:
        livres = Livre.objects.filter(titre__icontains=query)
        
        
        if not livres :
            message = "Aucun livre trouvé ."
    else:
        livres = Livre.objects.all()
    page_obj = get_paginated_books(request, livres)
    return render(request,'appBibliotheque/dashboard/livre.html',{'livres' : livres ,'page_obj':page_obj,'message': message,query:"query"})

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
            Exemplaire.objects.create(livre=livre, disponible=True)
            messages.success(request, "Le livre a été ajouté avec succès.")
            return redirect("liste_livres")  # Assurez-vous que 'acceuileBli' est correct
        else:
            messages.error(request, "Le formulaire nest pas valide. Veuillez corriger les erreurs.")
            return redirect("ajouter_livre")
    else:
       return render(request, 'appBibliotheque/dashboard/ajouter.html')
   
   
def supprimer_exemplaire(request,id):
    
    livre = get_object_or_404(Livre,id=id)
    exemplaires = Exemplaire.objects.filter(livre=livre,disponible = True)
    if exemplaires.exists():
        
        exemplaire = exemplaires.first()
        exemplaire.delete()
        messages.success(request,"le exemplaire est supprime avec succès")
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
    nbExemplaire=Exemplaire.objects.count();

    return render(request,'appBibliotheque/dashboard/detailLivre.html',{'livre':livre,'exemplaires':exemplaires})

def page_UnLivre(request):
    return render(request,'appBibliotheque/user/unLivre.html')

def filterLivre(request,genre):
    if(genre=="all"):
         livres = Livre.objects.order_by('id')
    else:
       livres = Livre.objects.order_by('id').filter(categories__icontains=genre)
    page_obj = get_paginated_books(request, livres)
   
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



def demande_emprunt(request):
    if request.method == 'POST':
        try:
            utilisateur = request.user
            id = request.POST.get("id")
            exemplaire = Exemplaire.objects.filter(livre_id=id, disponible=True).first()
            # print(Exemplaire.objects.filter(livre_id=id, disponible=True).query)

            if exemplaire and exemplaire.disponible:
                demande_existante = DemandeEmprunt.objects.filter(exemplaire=exemplaire, 
                                                                  utilisateur=utilisateur,
                                                                  acceptee=False).exists()
                if demande_existante:
                    messages.warning(request, "Vous avez déjà une demande en cours pour cet exemplaire.")
                else:
                    date_retour_str = request.POST.get('date_retour')
                    try:
                        date_retour = datetime.strptime(date_retour_str, '%Y-%m-%d')
                        demande = DemandeEmprunt.objects.create(exemplaire=exemplaire, 
                                                                utilisateur=utilisateur,
                                                                date_retour=date_retour)
                        demande.save()
                        messages.success(request, "Le livre a été demandé avec succès.")
                    except ValueError:
                        messages.error(request, "Format de date invalide.")
            else:
                messages.warning(request, "Cet exemplaire n'est pas disponible.")
        except Exception as e:
            print(e)
            messages.error(request, f"Une erreur s'est produite : {e}")
    return redirect("home")


# def is_admin(user):
#     return user.est_bibliothecaire

	

    









@login_required
def liste_demandes_emprunt(request):
    # Récupérer toutes les demandes d'emprunt
    demandes = DemandeEmprunt.objects.all().order_by("date_demande")
    
    return render(request, 'appBibliotheque/dashboard/demande_Empruntes.html',
                  {'demandes': demandes})

def accepter_demande_emprunt(request, id):
    demande = get_object_or_404(DemandeEmprunt, pk=id)
    print(demande.exemplaire)
    
    exemplaire = Exemplaire.objects.get(id=demande.exemplaire.id, disponible=True)
        
    utilisateur = demande.utilisateur
    livre = exemplaire.livre

    if Emprunter.objects.filter(utilisateur=utilisateur, exemplaire__livre=livre).exists():
        messages.warning(request, f"Vous avez déjà emprunté le livre '{livre.titre}'.")
    else:
        # Créer un nouvel emprunt
        emprunt = Emprunter.objects.create(exemplaire=exemplaire, utilisateur=utilisateur,date_retour=demande.date_retour)
        emprunt.save()
        # Mettre à jour la disponibilité de l'exemplaire
        exemplaire.disponible = False
        exemplaire.save()
        # Marquer la demande comme acceptée
        demande.acceptee = True
        demande.save()
        demande.delete()
        messages.success(request, 'La demande d\'emprunt a été acceptée avec succès.')
        
        dest_mail = utilisateur.email
        message = f"Mr. {utilisateur.username} votre demande a été acceptée vous avez 48h pour récuperer votre exemplaire. Merci!"
        admin_mail="alykeita295@gmail.com"
        subject ="Demande Accepte"
        # send_mail(subject,message,admin_mail,[dest_mail])
        
        try:
         send_mail(subject, message, admin_mail, [dest_mail])
         print("Email sent successfully")
        except Exception as e:
         print(f"Failed to send email")
        """ 
        send mail
        
        
        """
    
    # Rediriger vers la liste des demandes d'emprunt
    return redirect('liste_demandes_emprunt')



def refuser_demande_emprunt(request, id):
    # Récupérer la demande d'emprunt à partir de son identifiant
    demande = DemandeEmprunt.objects.get(pk=id)
    
    # Supprimer la demande
    demande.delete()
    
    # Rediriger vers la liste des demandes d'emprunt après avoir refusé
    return redirect('liste_demandes_emprunt')
def list_exemplaire_empruntes(request):
    query = request.GET.get('nom')
    message = ""
    
    if query:
        livres = Livre.objects.filter(titre__icontains=query)
        exemplaires = Exemplaire.objects.filter(livre__in=livres)
        emprunts = Emprunter.objects.filter(exemplaire__in=exemplaires)
        
        if not emprunts.exists():
            message = "Aucun emprunt trouvé."
    else:
        emprunts = Emprunter.objects.all().order_by("date_retour")
        
    return render(request, 'appBibliotheque/dashboard/empruntes.html', {'emprunts': emprunts, 'message': message,query:"query"})
    


def rendre_exemplaire(request, id):
    emprunt = get_object_or_404(Emprunter, id=id)
    exemplaire=emprunt.exemplaire
    exemplaire.disponible = True
    exemplaire.save()
    emprunt.delete()
   
    messages.success(request,"L\'exemplaire est en état prêt maintenant")
   
    
    return redirect('list_empruntes')


def mise_pret_horspret(request, id):
    exemplaire = get_object_or_404(Exemplaire, id=id)
    
    if exemplaire.disponible:
        exemplaire.disponible = False
        exemplaire.save()
        messages.success(request, "Exemplaire mis hors prêt avec succès.")
    else:
        # Check if the exemplaire is not currently borrowed
        if not Emprunter.objects.filter(exemplaire=exemplaire).exists():
            exemplaire.disponible = True
            exemplaire.save()
            messages.success(request, "Exemplaire remis en prêt avec succès.")
        else:
            messages.warning(request, "L'exemplaire est actuellement emprunté et ne peut pas être remis en prêt.")
    
    # Redirect to the referring page or a default page if not available
    return redirect(request.META.get('HTTP_REFERER', 'detailLivre'))
    
    



   

      


