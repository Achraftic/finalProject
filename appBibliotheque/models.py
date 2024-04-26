from django.db import models
from accounts.models import Utilisateur
from django.urls import reverse

class Livre(models.Model):
    id = models.AutoField(primary_key=True)
    auteur = models.CharField(max_length=128)
    titre = models.CharField(max_length=128)
    isbn = models.CharField(max_length=50, unique = True)
    slug = models.SlugField(max_length=200)
    description = models.TextField()
    date_publication = models.DateField(auto_now_add=True)
    image_couverture = models.ImageField(upload_to ='images',null = True,blank = True)
    categories = models.CharField(max_length=128,null = True)
    def get_NbrExemple(self):
        return self.exemplaires_livre.count()+1
    def __str__(self) -> str:
        return self.titre 
    def get_absolute_url(self):
        return reverse("livre",kwargs={'slug': self.slug})
    def save(self, *args, **kwargs):
        # Si le slug n'est pas déjà défini, le créer à partir de l'ISBN
        if not self.slug:
            self.slug = self.isbn
        super().save(*args, **kwargs)
class Exemplaire(models.Model):
    id = models.AutoField(primary_key=True)
    livre = models.ForeignKey(Livre,on_delete=models.CASCADE,related_name='exemplaires_livre')
    disponible = models.BooleanField(default=True) 
    perdu = models.BooleanField(default=False)
class Emprunter(models.Model):
    exemplaire = models.OneToOneField(Exemplaire,on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur,on_delete=models.CASCADE)
    date_emprunt = models.DateField(auto_now_add=True)
    date_retour = models.DateField(blank=True, null = True)
    accepter = models.BooleanField(default=False)

