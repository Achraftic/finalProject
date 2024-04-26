from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import re

# Create your models here.
class Utilisateur(AbstractUser):
    est_bibliothecaire = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
    def save(self, *args, **kwargs):
        # Générer un slug à partir du nom d'utilisateur si le slug est vide
        if not self.slug:
            self.slug = slugify(self.username)
        super().save(*args, **kwargs)
    def save(self, *args, **kwargs):
    # Vérifier si l'objet utilisateur est nouvellement créé ou existant
        if not self.pk or self._state.adding:
        # Si nouvellement créé, appeler clean_password pour valider le mot de passe
            self.clean_password()
    # Appeler la méthode save() de la classe parent
        super().save(*args, **kwargs)

    def clean_password(self):
        password = self.password

        # Valider la longueur du mot de passe
        if len(password) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")

        # Valider la présence d'au moins un chiffre
        if not any(char.isdigit() for char in password):
            raise ValidationError("Le mot de passe doit contenir au moins un chiffre.")

        # Valider la présence d'au moins une lettre majuscule
        if not any(char.isupper() for char in password):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre majuscule.")

        # Valider la présence d'au moins une lettre minuscule
        if not any(char.islower() for char in password):
            raise ValidationError("Le mot de passe doit contenir au moins une lettre minuscule.")

        # Valider la présence d'au moins un caractère spécial
        if not re.search(r"[!@#$%^&*()_+=\[\]{};:.,<>?|\\]", password):
            raise ValidationError("Le mot de passe doit contenir au moins un caractère spécial.")