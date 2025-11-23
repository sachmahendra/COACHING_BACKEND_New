from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status , generics
from .serializers import *
from .models import *
import ast
import uuid
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken

from dotenv import load_dotenv
import os


# views.py
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.decorators import action

load_dotenv()  # This loads the variables from .env
        
# class postcustomerData(APIView):
#     def post(self,request):
#         serializerdata = postcustomerDataSerializer(data=request.data)
#         if serializerdata.is_valid():
#             #orm to create new record in db
#             customer.objects.create(**serializerdata.data)
#             message = {'message':"Customer Data Submitted Sucessfully"}
#             return Response(message,status=status.HTTP_201_CREATED)
#         return Response(serializerdata.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class postcustomerData(APIView):
    def post(self, request):
        serializerdata = postcustomerDataSerializer(data=request.data)
        if serializerdata.is_valid():
            # Save to DB
            new_customer = customer.objects.create(**serializerdata.validated_data)

            # Prepare email content
            subject = "New Customer Callback Request"
            message = (
                f"New customer details:\n\n"
                f"Name: {new_customer.customer_name}\n"
                f"Class: {new_customer.customer_class}\n"
                f"Goal: {new_customer.customer_goal}\n"
                f"Preferred Course: {new_customer.customer_course}\n"
                f"Mobile: {new_customer.customer_mobile}\n"
                f"Email: {new_customer.customer_email}\n"
                f"Message: {new_customer.customer_message}\n"
            )

            # Send email (to admin/you)
            send_mail(
                subject,
                message,
                None,  # uses DEFAULT_FROM_EMAIL
                ['mahendramh8081@gmail.com'],  # where you want to receive emails
                fail_silently=False,
            )

            return Response(
                {"message": "Customer Data Submitted Successfully & Email Sent"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializerdata.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class getcustomerData(APIView):
    def get(self,request):
        try:
            customerData = list(customer.objects.filter().values())
            return Response(customerData, status=status.HTTP_200_OK)
        except Exception as e:
            message = {'Error':str(e)}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
        
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_queryset(self):
        queryset = Course.objects.all()
        category = self.request.query_params.get("category")  # ?category=neet

        if category:
            queryset = queryset.filter(category__slug__iexact=category)  # filter by slug (case-insensitive)

        return queryset
    
    


class ReadOnlyOrAdminMixin:
    """
    Helper mixin to allow read-only to anyone and write only to admin users.
    We will use this by setting get_permissions in viewsets below.
    """
    pass


class DownloadCategoryViewSet(viewsets.ModelViewSet):
    queryset = DownloadCategory.objects.all().order_by("name")
    serializer_class = DownloadCategorySerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [p() for p in permission_classes]


class DownloadDocumentViewSet(viewsets.ModelViewSet):
    queryset = DownloadDocument.objects.select_related("category").all().order_by("-uploaded_at")
    serializer_class = DownloadDocumentSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [p() for p in permission_classes]

    def get_queryset(self):
        """
        Allow filtering by:
          - category (slug)
          - category_name (case-insensitive match)
          - subject
          - doc_type
        Example:
          /download-documents/?category=jee_mains
          /download-documents/?category_name=Class 11 with JEE Coaching
          /download-documents/?subject=physics&doc_type=chapter
        """
        qs = super().get_queryset()
        request = self.request

        cat_slug = request.query_params.get("category")
        cat_name = request.query_params.get("category_name")
        subject = request.query_params.get("subject")
        doc_type = request.query_params.get("doc_type")

        if cat_slug:
            qs = qs.filter(category__slug__iexact=cat_slug)
        if cat_name:
            qs = qs.filter(category__name__icontains=cat_name)
        if subject:
            qs = qs.filter(subject__iexact=subject)
        if doc_type:
            qs = qs.filter(doc_type__iexact=doc_type)

        return qs



# You can call your API like this:

# http://127.0.0.1:8000/download-documents/?category=jee_mains
# → Returns documents in category with slug jee_mains

# http://127.0.0.1:8000/download-documents/?category_name=Class 11 with JEE Coaching
# → Returns documents whose category name contains that phrase (case-insensitive)

# http://127.0.0.1:8000/download-documents/?subject=physics&doc_type=chapter
# → Returns physics documents of type "chapter"

# -------------------------------------------------------------------------------------------------------

# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
# from .models import Student
# from .serializers import StudentSignupSerializer, StudentLoginSerializer

# # ---------------- SIGNUP -----------------
# class StudentSignupView(generics.CreateAPIView):
#     serializer_class = StudentSignupSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if not serializer.is_valid():
#             print(serializer.errors)  # 👈 Add this line
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         user = serializer.save()
#         return Response({"message": "User created successfully!"}, status=status.HTTP_201_CREATED)


# # ---------------- LOGIN -----------------
# class StudentLoginView(generics.GenericAPIView):
#     serializer_class = StudentLoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data["email"]
#         password = serializer.validated_data["password"]

#         user = authenticate(request, email=email, password=password)
#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             return Response({
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#                 "user": {
#                     "email": user.email,
#                     "full_name": user.full_name
#                 }
#             })
#         return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)



# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import (
    SendOTPSerializer, VerifyOTPSerializer, CompleteSignupSerializer, StudentSerializer
)
from .models import OTPRequest, Student
import random
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

OTP_TTL_MINUTES = 5

def generate_otp():
    return f"{random.randint(100000, 999999)}"


# USE BELOW TO SEND OTP IN CONSOLE
# def send_sms_placeholder(mobile, code):
#     # In dev we just print. Replace with SMS provider in production (Twilio, Fast2SMS, etc.)
#     print(f"[OTP SEND] to {mobile}: {code}")


# def send_sms_fast2sms(mobile, code):
#     # In dev we just print. Replace with SMS provider in production (Twilio, Fast2SMS, etc.)
#     print(f"[OTP SEND] to {mobile}: {code}")
    
def send_sms_twilio(mobile, code):
    # In dev we just print. Replace with SMS provider in production (Twilio, Fast2SMS, etc.)
    print(f"[OTP SEND] to {mobile}: {code}")

class SendOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile_number"]
        # rate-limit: optional — you can check recent OTPs and prevent spamming
        code = generate_otp()
        otp_obj = OTPRequest.objects.create(mobile_number=mobile, code=code)
        # send via SMS provider (here placeholder)
        
        # send via SMS provider (here placeholder)
        
        # send_sms_placeholder(mobile, code) #for sending otp in terminal

        # send_sms_fast2sms(mobile, code)
        send_sms_twilio(mobile, code)
        return Response({"message": "OTP sent"}, 
                        
                        
                        status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile_number"]
        code = serializer.validated_data["code"]
        # find latest un-used OTP for mobile
        try:
            otp = OTPRequest.objects.filter(mobile_number=mobile, used=False).order_by("-created_at").first()
            if not otp:
                return Response({"error": "No OTP found for this number"}, status=status.HTTP_400_BAD_REQUEST)
            if otp.code != code:
                return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
            if otp.is_expired(OTP_TTL_MINUTES):
                return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
            # mark verified but not used yet — used will be set when completing signup or login
            otp.verified = True
            otp.save()
            return Response({"verified": True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CompleteSignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = CompleteSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile_number"]
        # find a verified OTP
        otp = OTPRequest.objects.filter(mobile_number=mobile, verified=True, used=False).order_by("-created_at").first()
        if not otp:
            return Response({"error": "OTP not verified or already used"}, status=status.HTTP_400_BAD_REQUEST)
        if otp.is_expired(OTP_TTL_MINUTES):
            return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
        # create or error if user exists
        if Student.objects.filter(mobile_number=mobile).exists():
            return Response({"error": "User already exists, please login"}, status=status.HTTP_400_BAD_REQUEST)
        student = Student.objects.create_user(
            mobile_number=mobile,
            full_name=serializer.validated_data.get("full_name", ""),
        )
        # fill optional fields
        student.email = serializer.validated_data.get("email", "")
        student.target_course = serializer.validated_data.get("target_course", "")
        student.student_class = serializer.validated_data.get("student_class", "")
        student.save()
        # mark otp used
        otp.used = True
        otp.save()
        # issue tokens
        refresh = RefreshToken.for_user(student)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": StudentSerializer(student).data
        }
        return Response(data, status=status.HTTP_201_CREATED)

class LoginWithOTPView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # This endpoint expects mobile_number and requires that an OTP was verified for this mobile (verified=True, used=False)
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        mobile = serializer.validated_data["mobile_number"]
        code = serializer.validated_data["code"]

        otp = OTPRequest.objects.filter(mobile_number=mobile, used=False).order_by("-created_at").first()
        if not otp:
            return Response({"error": "No OTP found"}, status=status.HTTP_400_BAD_REQUEST)
        if otp.code != code:
            return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)
        if otp.is_expired(OTP_TTL_MINUTES):
            return Response({"error": "OTP expired"}, status=status.HTTP_400_BAD_REQUEST)
        # find user
        try:
            user = Student.objects.get(mobile_number=mobile)
        except Student.DoesNotExist:
            return Response({"error": "User not found. Please signup first."}, status=status.HTTP_400_BAD_REQUEST)
        # mark otp used
        otp.used = True
        otp.save()
        # issue tokens
        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": StudentSerializer(user).data
        }, status=status.HTTP_200_OK)
        
        
# import requests

# def send_sms_fast2sms(mobile, code):
#     api_key = "ANEGKlmz9ZM1SHbgBjTRFeDc5tkwVLos2n0p74U6Whq8vyiPur7VTgvPuymkIlMpiLYQXWR9q2KO4jB8"  # 🔒 keep this secret, use environment variable in production
#     message = f"Your verification OTP is {code}. It will expire in 5 minutes."
#     url = "https://www.fast2sms.com/dev/bulkV2"
#     payload = {
#         "authorization": api_key,
#         "sender_id": "TXTIND",
#         "message": message,
#         "language": "english",
#         "route": "v3",
#         "numbers": mobile,
#     }
#     headers = {
#         'cache-control': "no-cache"
#     }
#     response = requests.get(url, params=payload, headers=headers)
#     print(response.text)  # for debugging


from twilio.rest import Client

def send_sms_twilio(mobile, code):
    account_sid = os.environ.get("account_sid")
    auth_token = os.environ.get("auth_token")
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body=f"Your verification OTP is {code}",
        from_="+19789638428",  # your Twilio number
        to=f"+91{mobile}"
    )
    print(message.sid)

