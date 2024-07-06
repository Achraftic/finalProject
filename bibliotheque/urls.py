from django.contrib import admin
from django.urls import path
from appBibliotheque.views import (
    home, rechercher_livre, detail_livre, ajouter_livre, ajouter_exemplaire,
    page_UnLivre, filterLivre, edit_livre, liste_demandes_emprunt, rendre_exemplaire,
    mise_pret_horspret, emprunter_exemplaire, liste_livres, page_ajout, supprimer_exemplaire,
    detailLivre, dashboard, update_livre, demande_emprunt, refuser_demande_emprunt,
    accepter_demande_emprunt, list_exemplaire_empruntes,ajouterEmprunt
)
from accounts.views import (
    register, signup, pagelogin, login_user, logout_user, users_lists, delete_user,
    forget_password_view
)
from  accounts.decorators import bibliothecaire_required
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name="home"),
    path('register/', register, name='register'),
    path('genre/<str:genre>', filterLivre, name='filterLivre'),
    path('page_UnLivre/', page_UnLivre, name='page_UnLivre'),
    path('signup/', signup, name='signup'),
    path('forgot_password/', forget_password_view, name='forgot_password'),
    path('logout_user/', logout_user, name='logout_user'),
    
    path('users_lists/', bibliothecaire_required(users_lists), name='users_lists'),
    path('delete_user/<slug:username>',bibliothecaire_required(delete_user)  , name='delete_user'),
    path('page_ajout/', bibliothecaire_required(page_ajout) , name='page_ajout'),
    path('pagelogin/', pagelogin, name='pagelogin'),
    path('rechercher_livre/', rechercher_livre, name='rechercher_livre'),
    path('ajouter_livre/', bibliothecaire_required(ajouter_livre), name='ajouter_livre'),
    path('edit_livre/<int:id>', bibliothecaire_required(edit_livre), name='edit_livre'),
    path('update_livre/<int:id>', bibliothecaire_required(update_livre), name='update_livre'),
    path('liste_livres/', bibliothecaire_required(liste_livres), name='liste_livres'),
    path('supprimer_exemplaire/<int:id>', bibliothecaire_required(supprimer_exemplaire), name='supprimer_exemplaire'),
    path('detail_livre/<slug:slug>', detail_livre, name='detail_livre'),
    path('ajouter_exemplaire/<int:id>', bibliothecaire_required(ajouter_exemplaire), name='ajouter_exemplaire'),
    path('detailLivre/<int:id>',  bibliothecaire_required(detailLivre), name='detailLivre'),
    path('livre/<slug:slug>/emprunter_exemplaire', emprunter_exemplaire, name='emprunter_exemplaire'),
    path('login/', login_user, name='login'),
    path('dashboard/', bibliothecaire_required(dashboard), name="dashboard"),
    path('liste_demandes_emprunt/', bibliothecaire_required(liste_demandes_emprunt), name="liste_demandes_emprunt"),
    path('list_empruntes/', bibliothecaire_required(list_exemplaire_empruntes), name="list_empruntes"),
    path('refuser_demande_emprunt/<int:id>', bibliothecaire_required(refuser_demande_emprunt), name="refuser_demande_emprunt"),
    path('accepter_demande_emprunt/<int:id>', bibliothecaire_required(accepter_demande_emprunt), name="accepter_demande_emprunt"),
    path('rendre_exemplaire/<int:id>', bibliothecaire_required(rendre_exemplaire), name="rendre_exemplaire"),
    path('mise_pret_horspret/<int:id>', bibliothecaire_required(mise_pret_horspret), name="mise_pret_horspret"),
    path('demande_emprunt/', demande_emprunt, name="demande_emprunt"),
    
    path('ajouterEmprunt/',bibliothecaire_required(ajouterEmprunt), name="ajouterEmprunt")
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
