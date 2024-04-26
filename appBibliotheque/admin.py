from django.contrib import admin
from appBibliotheque.models import Livre,Exemplaire,Emprunter

admin.site.register(Livre)
admin.site.register(Exemplaire)
admin.site.register(Emprunter)
