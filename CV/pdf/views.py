from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from .models import Profile
import pdfkit
from django.template.loader import get_template
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.conf import settings

#------------COMPTE--------------------------

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, RegistrationForm

# Create your views here.
def acceuil(request):
    return render(request, 'pdf/acceuil.html')

@login_required
def index(request):
   
   return render(request, 'pdf/resume.html')

@login_required
def formulaire(request):
   if request.method == "POST":
      name = request.POST.get("name")
      email = request.POST.get("email")
      phone = request.POST.get("phone")
      address = request.POST.get("address")
      competence = request.POST.get("competance")
      langue = request.POST.get("langue")
      interet = request.POST.get("interet")
      objectif = request.POST.get("objectif")
      experience = request.POST.get("experience")
      education = request.POST.get("education")
      project = request.POST.get("project")
      donnees = Profile(name=name, email=email, phone=phone, address=address, competance=competence, experience=experience, objectif=objectif, projet=project, interet=interet, langue=langue, education=education)
      donnees.save()
      return redirect('verification')

   return render(request, 'pdf/form.html')

@login_required
def verification(request):
   profiles = Profile.objects.all()[:1]
   for profile in profiles:
      name = profile.name
      phone = profile.phone
      email = profile.email
      address = profile.address
      com = profile.competance
      langue = profile.langue
      interet = profile.interet
      exp = profile.experience
      objectif = profile.objectif
      education = profile.education
      project = profile.projet
   return render(request, "pdf/verification.html", { 'address':address, 'name':name, 'email':email, 'phone':phone, 'competance':com, 'interet':interet, 'langue':langue, 'experience':exp, 'objectif':objectif, 'education':education, 'projet':project})

@login_required
def generer(request, id):
      profile = Profile.objects.get(pk=id)
      name = profile.name
      phone = profile.phone
      email = profile.email
      address = profile.address
      com = profile.competance
      langue = profile.langue
      interet = profile.interet
      exp = profile.experience
      objectif = profile.objectif
      education = profile.education
      project = profile.projet

      template = get_template('pdf/generator.html')
      context = { 'address':address, 'name': name, 'email': email, 'phone': phone, 'competance': com, 'interet': interet,'langue':langue, 'experience':exp, 'objectif':objectif, 'education':education, 'projet':project}
      html = template.render(context)
      options ={
           'page-size':'Letter',
           'encoding':'UTF-8',
      }
      pdf = pdfkit.from_string(html, False, options)
      reponse = HttpResponse(pdf, content_type='application/pdf')
      reponse['Content-Disposition'] = "attachement"
      return reponse 

@login_required
def download(request):
   profile = Profile.objects.all()
   return render(request, 'pdf/download.html', {'profile': profile})

@login_required
def email(request):
   if request.method == "POST":
      name = request.POST.get("full-name")
      email = request.POST.get("email")
      subject = request.POST.get("subject")
      message = request.POST.get("message")
      data = {
         'name':name,
         'email':email,
         'subject':subject,
         'message':message
      }

      message = """
      New message: {}

      From: {}
        """.format(data['message'], data['email'])
      send_mail(data['subject'], message, '', ['selonrandriavao209@gmail.com'])
   return render(request, 'pdf/envoye_mail.html', {})

@login_required
def finission_page(request):
   profile = Profile.objects.all()
   context = {'tel': profile}
   return render(request, 'pdf/finission.html', context)

@login_required
def envoi_email(request):
   test_email()
   data = {
      'success': True,
      'message': 'api to send an email'
   }
   return JsonResponse(data)


def test_email():
    html_tpl_path = 'pdf/teste_email.html'
    context_data = {'name': 'JK'}
    email_html_template = get_template(html_tpl_path).render(context_data)
    receiver_email = 'randriavaoselon@gmail.com'
    email_msg = EmailMessage('Bienvenue dans la creation de CV automatique',
                              email_html_template, settings.APPLICATION_EMAIL, [receiver_email],
                              reply_to=[settings.APPLICATION_EMAIL]
                             )
    email_msg.content_subtype = 'html'
    email_msg.send(fail_silently=False)
    
#-------------------------AUTHENTIFICATION--------------------------------------------------------------

def signin(request):
    forms = LoginForm()
    if request.method == 'POST':
        forms = LoginForm(request.POST)
        if forms.is_valid():
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect('send_mail')
    context = {
        'form': forms
    }
    return render(request, 'authentification/signin.html', context)


def signup(request):
    forms = RegistrationForm()
    if request.method == 'POST':
        forms = RegistrationForm(request.POST)
        if forms.is_valid():
            firstname = forms.cleaned_data['firstname']
            lastname = forms.cleaned_data['lastname']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            confirm_password = forms.cleaned_data['confirm_password']
            if password == confirm_password:
                try:
                    User.objects.create_user(username=username, password=password, email=email, first_name=firstname, last_name=lastname)
                    return redirect('signin')
                except:
                    context = {
                        'form': forms,
                        'error': 'This Username Already exists!'
                    }
                    return render(request, 'authentification/signup.html', context)
    context = {
        'form': forms
    }
    return render(request, 'authentification/signup.html', context)

def signout(request):
    logout(request)
    return redirect('signin')