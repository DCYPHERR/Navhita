
from django.urls import path
from . import views

urlpatterns =[
    path('',views.home,name='home'),
    path('registerPatient/', views.registerPatient, name='registerPatient'),
    path('loginPatient/', views.loginPatient, name='loginPatient'),
    path('registerCaretaker/', views.registerCaretaker, name='registerCaretaker'),
    path('service/',views.sendServiceMail,name="sendServiceMail"),
    path('logout/',views.logout,name='logout')
    # path('login/', views.login.as_view()),
    # path('home/', views.show_rooms.as_view()),
    
]