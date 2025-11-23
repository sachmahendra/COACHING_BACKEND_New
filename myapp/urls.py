from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import *


router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'courses', CourseViewSet)

router.register(r"download-categories", DownloadCategoryViewSet, basename="download-category")
router.register(r"download-documents", DownloadDocumentViewSet, basename="download-document")

urlpatterns = [
    
    path('postcustomerData/',views.postcustomerData.as_view()),
    path('getcustomerData/',views.getcustomerData.as_view()),
    
    # path("signup/", StudentSignupView.as_view(), name="student-signup"),
    # path("login/", StudentLoginView.as_view(), name="student-login"),
    
    path("send-otp/", SendOTPView.as_view(), name="send-otp"),
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("complete-signup/", CompleteSignupView.as_view(), name="complete-signup"),
    path("login-with-otp/", LoginWithOTPView.as_view(), name="login-with-otp"),
    
    path('', include(router.urls)),   # auto adds /categories/ and /courses/
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    