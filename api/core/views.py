from django.shortcuts import render
from rest_framework import generics, viewsets, permissions, filters
from rest_framework.response import Response
import requests
from django.conf import settings
from .models import CourseSales, Transaction
from .serializers import SalesSerializer, TransactionSerializer

from django.core.mail import send_mail
from rest_framework import status
from .mixins import LoggingMixin

class CourseGenericViewset(viewsets.ModelViewSet):
    queryset = CourseSales.objects.all()
    serializer_class = SalesSerializer

sandbox_apiuser = "159c3024-396a-47ff-814b-163c19191723"
sandbox_apikey = "FAK_TEST_1cd4331800b4df6ae913"
initiatePaymentUrlSandbox = "https://sandbox.fapshi.com/initiate-pay"
checkPaymentUrlSandbox = "https://sandbox.fapshi.com/payment-status/"

# initiatePaymentUrl = "https://sandbox.fapshi.com/initiate-pay"
# initiatePaymentUrl = "https://sandbox.fapshi.com/payment-status/"

live_apiuser = "2979828e-189a-4771-8a78-c613035863ba"
live_apikey = "FAK_83219f5f35bd66dc728e65e787a1dd1a"
initiatePaymentUrl = "https://live.fapshi.com/initiate-pay"
checkPaymentUrl = "https://live.fapshi.com/payment-status/"

message = '''
            Salutations,
            
            Merci pour votre participation a cette formation en Agriculture !
            Vos fichiers et vidoes sont dispoibles dans les liens suivants.

            Videos:
            Module 1 : https://www.youtube.com/watch?v=MA1JvvSAM24&feature=youtu.be
            Module 2 : https://www.youtube.com/watch?v=MjW7BpsmzYI&feature=youtu.be
            Module 3 : https://youtu.be/TXnoEdA7QwI

            Fiches Techniques: https://drive.google.com/uc?export=download&id=1z79PR2b4sHuvsBPbPWkyYCEMUZ54It9c

            Pour tout soucis, n'hesitez pas a nous contacter.
            Pour recuperer ces fichiers, entrez votre code dans la page de reclamation https://www.agribea.com/redeem.html


            Meilleures salutations,
            AGRIBEA
        '''

class InitiatePayment(generics.GenericAPIView, LoggingMixin):
    def get(self, request):
        payload = {
            "amount":25000,
            "redirectUrl":"http://www.agribea.com/payment-done.html",
            }
        headers = {
            "apiuser":live_apiuser,
            "apikey":live_apikey
        }
        request = requests.post(initiatePaymentUrl, json=payload, headers=headers) 
        print(request.status_code)
        if (request.status_code==200):
            response = request.json()
            try:
                print(response["message"]) 
                return Response(response)

            except Exception as e:
                print(e)
                return Response(request) 
        return Response (request)
        
class CheckPayment(generics.GenericAPIView, LoggingMixin):
    def get(self, request):
        transId = request.query_params.get('transId') 
        headers = {
            "apiuser":live_apiuser,
            "apikey":live_apikey
        }
        checkPaymentUrlFull = str(checkPaymentUrl) + str(transId)
        print(checkPaymentUrlFull)
        request = requests.get(checkPaymentUrlFull,headers=headers) 
        print(request.json())
        if (request.status_code==200):
            response = request.json()
            try:
                response["file_link"] = "https://drive.google.com/uc?export=download&id=1z79PR2b4sHuvsBPbPWkyYCEMUZ54It9c"
                send_mail("VOTRE COURS AGRIBEA", message, settings.EMAIL_HOST_USER, [response['email']])

                print(response["status"]) 
                return Response(response)

            except Exception as e:
                print(e)
                return Response({'message':e, 'error':request.json()}) 
        else:
            return Response({'error':'request error','message':request.json()})

class RedeemPayment(generics.GenericAPIView, LoggingMixin):
    def get(self, request):
        transId = request.query_params.get('code') 
        email_addreess = request.query_params.get('email') 
        headers = {
            "apiuser":live_apiuser,
            "apikey":live_apikey
        } 
        checkPaymentUrlFull = str(checkPaymentUrl) + str(transId)
        print(checkPaymentUrlFull)
        request = requests.get(checkPaymentUrlFull,headers=headers) 
        print(request.status_code)
        if (request.status_code==200):
            response = request.json()
            try:
                print(response["status"]) 
                send_mail("VOTRE COURS AGRIBEA", message, settings.EMAIL_HOST_USER, [email_addreess])
                response["file_link"] = "https://drive.google.com/uc?export=download&id=1z79PR2b4sHuvsBPbPWkyYCEMUZ54It9c"
                return Response(response)

            except Exception as e:
                print(e)
                return Response({'message':e}) 
        else:
            return Response({'message':request.json()})

# class WebHookViewSet(viewsets.ModelViewSet):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer 
#     def create(self, request):
#         print(request.data)
#         if request.data['status']=='SUCCESSFUL':
#             send_mail("VOTRE COURS AGRIBEA", message, settings.EMAIL_HOST_USER, [request.data['email']])
#         return super().create(request)

class WebHookViewSet(viewsets.ModelViewSet, LoggingMixin):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Send email
        if request.data.get('status') == 'SUCCESSFUL':
            send_mail("VOTRE COURS AGRIBEA",  message, settings.EMAIL_HOST_USER, [request.data.get('email')])
        else:
            print(request.data)
            

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)