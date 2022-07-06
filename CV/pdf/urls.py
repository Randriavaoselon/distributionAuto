from django.urls import path
from . import views

urlpatterns = [
    path('', views.acceuil, name="index"),
    path('acceuil',views.index, name="acceuil"),
    path('creercv',views.formulaire, name="creer"),
    path('verification',views.verification, name="verification"),
    path('<int:id>',views.generer, name="generer"),
    path('download',views.download, name="download"),
    path('envoye_email',views.email, name="email"),
    path('finisse_page', views.finission_page, name="finisse"),
    path('envoi_mail', views.envoi_email, name='send_mail'),
    

    #---------------Compte------------------------------------
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='signout')
]