
from django.contrib import admin
from django.urls import path
from appBibliotheque.views import home,rechercher_livre,detail_livre,ajouter_livre,ajouter_exemplaire,page_UnLivre,filterLivre
from appBibliotheque.views import emprunter_exemplaire,liste_livres,page_ajout,supprimer_exemplaire,detailLivre
# from appBibliotheque.views import categorie_math,categorie_Roman,categorie_Physique,categorie_Sport,categorie_Social,categorie_culture
from accounts.views import register,signup,pagelogin,login_user,logout_user,users_lists,delete_user
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name="home"),
    path('register/',register,name='register'),
    path('genre/<str:genre>/', filterLivre, name='filterLivre'),
    path('page_UnLivre/',page_UnLivre,name='page_UnLivre'),
    path('signup/',signup,name='signup'),
    path('logout_user/',logout_user,name='logout_user'),
    path('users_lists/',users_lists,name='users_lists'),
    path('delete_user/<slug:username>/',delete_user,name='delete_user'),
    path('page_ajout/',page_ajout,name='page_ajout'),
    path('pagelogin/',pagelogin,name='pagelogin'),
    path('rechercher_livre/',rechercher_livre,name='rechercher_livre'),
    path('ajouter_livre/',ajouter_livre,name='ajouter_livre'),
    path('liste_livres/',liste_livres,name='liste_livres'),
    path('supprimer_exemplaire/<int:id>/',supprimer_exemplaire,name='supprimer_exemplaire'),
    path('detail_livre/<slug:slug>/',detail_livre,name='detail_livre'),
    path('ajouter_exemplaire/<int:id>/',ajouter_exemplaire,name='ajouter_exemplaire'),
    path('detailLivre/<int:id>/',detailLivre,name='detailLivre'),
    path('livre/<slug:slug>/emprunter_exemplaire/',emprunter_exemplaire,name='emprunter_exemplaire'),
    path('login/',login_user,name='login'),
] + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
