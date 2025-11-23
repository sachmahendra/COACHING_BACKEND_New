from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate

    
    
class postcustomerDataSerializer(serializers.Serializer):
    customer_id = serializers.CharField(read_only=True)   # auto-generated
    customer_name = serializers.CharField(max_length=100)
    customer_class = serializers.CharField()
    customer_email = serializers.EmailField()
    customer_mobile = serializers.IntegerField()
    customer_goal = serializers.CharField()
    customer_course = serializers.CharField()
    customer_message = serializers.CharField()
    customer_timestamp = serializers.DateTimeField(read_only=True)  # auto-generated
    
    
    
# Category serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


# Course serializer
class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    image = serializers.ImageField(required=False)  # <-- allows upload
    image_url = serializers.SerializerMethodField()  # <-- returns full URL

    class Meta:
        model = Course
        fields = [
            "course_id", "title", "description",
            "category", "category_id", "duration",
            "teacher", "image", "image_url", "created_at"
        ]

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None
        
        


# class DownloadDocumentSerializer(serializers.ModelSerializer):
#     file = serializers.SerializerMethodField()

#     class Meta:
#         model = DownloadDocument
#         fields = ["document_id", "title", "doc_type", "subject", "order", "file", "uploaded_at", "category"]
#         read_only_fields = ["document_id", "uploaded_at"]

#     def get_file(self, obj):
#         request = self.context.get("request")
#         if obj.file and request:
#             return request.build_absolute_uri(obj.file.url)
#         elif obj.file:
#             # fallback if no request in context
#             return obj.file.url
#         return None


# class DownloadCategorySerializer(serializers.ModelSerializer):
#     documents = DownloadDocumentSerializer(many=True, read_only=True)

#     class Meta:
#         model = DownloadCategory
#         fields = ["category_id", "name", "slug", "syllabus_url", "documents", "created_at"]
#         read_only_fields = ["category_id", "created_at"]


class DownloadCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadCategory
        fields = "__all__"

class DownloadDocumentSerializer(serializers.ModelSerializer):
    category = DownloadCategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=DownloadCategory.objects.all(),
        source="category",
        write_only=True
    )

    class Meta:
        model = DownloadDocument
        fields = [
            "document_id",
            "title",
            "category",
            "category_id",
            "doc_type",
            "subject",
            "order",
            "file",
            "uploaded_at",
        ]


# from rest_framework import serializers
# from .models import Student
# from django.contrib.auth.password_validation import validate_password

# class StudentSignupSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
#     password2 = serializers.CharField(write_only=True, required=True)

#     class Meta:
#         model = Student
#         fields = ["email", "full_name", "password", "password2"]

#     def validate(self, attrs):
#         if attrs["password"] != attrs["password2"]:
#             raise serializers.ValidationError({"password": "Password fields didn’t match."})
#         return attrs

#     def create(self, validated_data):
#         validated_data.pop("password2")
#         user = Student.objects.create_user(
#             email=validated_data["email"],
#             password=validated_data["password"],
#             full_name=validated_data.get("full_name", "")
#         )
#         return user


# class StudentLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)


# myapp/serializers.py
from rest_framework import serializers
from .models import Student, OTPRequest

class SendOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15)

class VerifyOTPSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15)
    code = serializers.CharField(max_length=6)

class CompleteSignupSerializer(serializers.Serializer):
    mobile_number = serializers.CharField(max_length=15)
    full_name = serializers.CharField(max_length=150)
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)
    target_course = serializers.CharField(max_length=200, required=False, allow_blank=True)
    student_class = serializers.CharField(max_length=50, required=False, allow_blank=True)

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "mobile_number", "full_name", "email", "target_course", "student_class", "created_at"]

