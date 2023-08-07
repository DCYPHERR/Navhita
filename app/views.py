

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.conf import settings
import requests
from django.contrib import messages
from django.db.models import Count
import django.contrib.auth as auth

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from .models import *


def home(request):
    return render (request, 'index.html')

def registerPatient(request):
    if (request.user.is_authenticated):
        return redirect('home')
    if (request.method=='POST'):
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        country = request.POST['country']
        state = request.POST['state']
        city = request.POST['city']
        pincode = request.POST['pincode']
        guardian_name = request.POST['guardian_name']
        guardian_email = request.POST['guardian_email']
        guardian_contact = request.POST['guardian_phone']
        emergency_contact = request.POST['emergency_contact']
        
        if email is None or password is None or name is None or phone is None:
            messages.error(request, 'All the fields are mandatory')
            return redirect('registerPatient')
        user = User.objects.create_user(email,password)
        user.is_patient = True
        patient=Patient(
            user=user,
            name=name,
            phone=phone,
            address = address,
            country = country,
            state = state,
            city = city,
            pincode = pincode,
            guardian_name = guardian_name,
            guardian_email = guardian_email,
            guardian_phone = guardian_contact,
            emergency_contact = emergency_contact
        )
        caretaker=CareTaker.objects.annotate(num_patients=Count('patient')).order_by('num_patients').first()
        patient.caretaker=caretaker
        user.save()
        patient.save()
        
        return redirect('home')
    
    return render(request, 'patient_registration.html')

def registerCaretaker(request):
    if (request.user.is_authenticated):
        return redirect('home')
    if (request.method=='POST'):
        email = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        state = request.POST['state']
        city = request.POST['city']
        pincode = request.POST['pincode']
        
        if email is None or password is None or name is None or phone is None:
            messages.error(request, 'All the fields are mandatory')
            return redirect('/')
        user = User.objects.create_user(email,password)
        user.is_caretaker = True
        caretaker=CareTaker(
            user=user,
            name=name,
            phone=phone,
            address = address,
            state = state,
            city = city,
            pincode = pincode,
        )
        user.save()
        caretaker.save()
        
        return redirect('home')
    
    return render(request, 'caretaker_registration.html')

def loginPatient(request):
    if (request.user.is_authenticated):
        return redirect('home')
    if (request.method=='POST'):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email,password=password)
        if user is not None and user.is_patient:
            auth.login(request,user)
            return redirect('sendServiceMail')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('loginPatient')
    
    return render(request, 'patient_login.html')

def sendServiceMail(request):
    if (not request.user.is_authenticated):
        return redirect('loginPatient')

    if (request.method=='POST'):
        user=request.user
        service_id = request.POST['id']
        print(service_id)
        # srvc = service.objects.filter(id=service_id).first();
        if service_id == 'water':
            srvc = "The patient needs water"
        elif service_id == "washroom":
            srvc = "The patient needs to use the washroom"
        elif service_id == "food":
            srvc = "The patient needs food"
        elif service_id == "medicine":
            srvc = "The patient needs medicine"
        elif service_id == "sleep":
            srvc = "The patient needs to sleep"
        elif service_id == "help":
            srvc = "The patient needs help"
        elif service_id == "television":
            srvc = "The patient needs to watch television"
        elif service_id == "play":
            srvc = "The patient wants to play"
        elif service_id == "others":
            srvc = "The patient needs some help"
        elif service_id == "sos":
            srvc = "The patient raised an SOS and needs immediate help" 
        else:
            messages.error(request, 'Invalid Service ID')
            return redirect('sendServiceMail')
        patient=user.patient
        context = {
            'name':patient.name,
            'patient_email':user.email,
            'caretaker_email':patient.caretaker.user.email,
            'help':srvc
        }
        send_email(context)
        messages.add_message(request, messages.INFO, 'Your message has been sent!\nA caretaker will come to help you shortly')
        return redirect(sendServiceMail)
    services = service.objects.all()
    return render(request,'service.html',{'user_name':request.user.patient.name,'services':services})
    
    

def send_email(context):
    sub = 'A patient needs your help'
    mess="Patient name : "+context['name']+"\nPatient email : "+context['patient_email']+"\nHelp needed : "+context['help']
    email_message = EmailMessage(
        sub,
        mess,
        settings.EMAIL_HOST_USER,
        [context['caretaker_email']]
    )
    print("email sent to "+context['caretaker_email'])
    email_message.send()
    
def logout(request):
    auth.logout(request)
    return redirect('home')

# class registerCareTaker(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         name = request.data.get('name')
#         phone = request.data.get('phone')
#         if email is None or password is None or name is None or phone is None:
#             return Response({'error': 'All the fields are mandatory'},
#                             status=status.HTTP_400_BAD_REQUEST)
#         user = User.objects.create_user(email,password)
#         caretaker=CareTaker(user=user,name=name,phone=phone)
#         user.save()
#         caretaker.save()
        
#         return Response({'status':'success'},status=status.HTTP_201_CREATED)
    
    
# class loginPatient(APIView):
#     def post(self,request):
#         email=request.data.get('email')
#         password=request.data.get('password')
#         user=authenticate(email=email,password=password)
#         if user:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key},status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid Credentials'},
#                             status=status.HTTP_400_BAD_REQUEST)
    
# class getPatientInfo(APIView):
#     permission_classes = (IsAuthenticated,)
#     def get(self,request):
#         user=request.user
#         # patients=User.objects.filter(email='patient1@gmail.com').first()
#         # print(patients.patient.name)
#         # patients=[patient.name for patient in patients]
#         try: 
#             email=user.email
#             name=user.patient.name
#             phone=user.patient.phone
            
#             return Response({'email':email, 'name':name, 'phone':phone},status=status.HTTP_200_OK)
#         except:
#             return Response({'error': 'Patient not found'},status=status.HTTP_400_BAD_REQUEST)
        