from django.shortcuts import render
from random import randint
from django.contrib.auth import get_user_model,login,logout,authenticate
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import User
from .models import Utilisateur
from django.contrib.auth.hashers import make_password
from django.core.mail import BadHeaderError,send_mail
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from urllib.parse import unquote

User = get_user_model()

def register(request):
    return render(request,'accounts/register.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Vérifier si les mots de passe correspondent
        if password != confirm_password:
            # Gérer l'erreur de mots de passe non correspondants
            return render(request, 'accounts/register.html', {'error': 'Les mots de passe ne correspondent pas'})

        # Créer un nouvel utilisateur
        user = Utilisateur.objects.create_user(username=username, email=email, password=password)
        user.save()

        # Authentifier et connecter l'utilisateur
        user = authenticate(username=username, password=password)
        login(request, user)

        # Rediriger vers la page d'accueil
        return redirect('home')

    # Si la méthode de la requête n'est pas POST, afficher le formulaire vide
    return render(request, 'accounts/register.html')

def pagelogin(request):
    return render(request,'accounts/login.html')
def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            is_admin = Utilisateur.objects.filter(username=username, est_bibliothecaire=True).exists()
            if is_admin:
                return redirect('dashboard')
            else:
                return redirect('home')
        else:
            error = 'Invalid username or password'
            return render(request, 'accounts/login.html', {'error': error})

    return render(request, 'accounts/login.html')
def logout_user(request):#champs à definir
    logout(request)
    return redirect('home')

def users_lists(request):
    query = request.GET.get('nom')
    message = ""
    allUsers = Utilisateur.objects.filter(est_bibliothecaire=False)

    if query:
        allUsers = allUsers.filter(username__icontains=query)
        if not allUsers.exists():
            message = "Aucun utilisateur trouvé."

    return render(request, 'appBibliotheque/dashboard/users.html', {'users': allUsers, 'query': query, 'message': message})


def delete_user(request,username):
    #users = users = Utilisateur.objects.all()
    decoded_username = unquote(username)
    u_username = get_object_or_404(Utilisateur,username=decoded_username)
    if u_username and u_username.est_bibliothecaire == False:   
        u_username.delete()
        messages.success(request,"le utilasteur est supprime avec succès")
    return redirect('users_lists')
        
def forget_password_view(request):
    if request.method == 'POST' :
        
        email = request.POST.get('email')
        user = Utilisateur.objects.filter(email=email).first()
        print(user)
        if user :
            new_password = f"{user.username}{randint(0, 1000)}"
            user.password = make_password(new_password)
            user.save()
            dest_mail = user.email
            message = f"Mr. {user.username} Voici votre nouveau mot de passe:{new_password}. Merci!"
            admin_mail="alykeita295@gmail.com"
            subject ="Envoi de password"
            
            try:
                send_mail(subject, message, admin_mail, [dest_mail])
                print("Email sent successfully")
                messages.success(request,"Veuillez vérifier votre email...") 
                return redirect("login")
            except Exception as e:
                print(f"Failed to send email")
       
        messages.success(request,"Cet email ne correspond pas à un compte..") 
        return redirect("forgot_password")
    return render(request,"accounts/forget_password.html")
            
    