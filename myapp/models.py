from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

customertype = (("Individual","Individual"),
                ("Company","Company")
                )

class customer(models.Model):
    customer_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer_name = models.CharField(max_length=100)
    customer_class= models.CharField(max_length=100)
    customer_email = models.EmailField()
    customer_mobile = models.IntegerField()
    customer_goal = models.TextField()
    customer_course = models.TextField()
    customer_message = models.CharField()
    customer_timestamp = models.DateTimeField(default=timezone.now)

    
    
    def __str__(self):
        return self.customer_name
    
    
    
# New models for courses
class Category(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)   # for clean URLs (iit-jee, neet, etc.)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    course_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="courses")
    duration = models.CharField(max_length=50, blank=True, null=True)   # "6 months"
    teacher = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to="courses/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    


DOC_TYPE_CHOICES = [
    ("chapter", "Chapter"),
    ("bonus", "Bonus Document"),
    ("model", "Model Paper"),
    ("other", "Other"),
]

SUBJECT_CHOICES = [
    ("physics", "Physics"),
    ("chemistry", "Chemistry"),
    ("maths", "Maths"),
    ("biology", "Biology"),
    ("english", "English"),
    ("other", "Other"),
]

class DownloadCategory(models.Model):
    category_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    syllabus_url = models.URLField(blank=True, null=True)  # external syllabus link (NTA)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class DownloadDocument(models.Model):
    document_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    category = models.ForeignKey(
        DownloadCategory, on_delete=models.CASCADE, related_name="documents"
    )
    title = models.CharField(max_length=255)
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES, default="chapter")
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES, default="other")
    order = models.PositiveIntegerField(default=0, help_text="Use to order chapters within a subject")
    file = models.FileField(upload_to="downloads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["category__name", "subject", "order", "-uploaded_at"]

    def __str__(self):
        return f"{self.title} ({self.category.name})"


    
# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
# import uuid

# class StudentManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("Email is required")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         return self.create_user(email, password, **extra_fields)

# class Student(AbstractBaseUser, PermissionsMixin):
#     student_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     email = models.EmailField(unique=True)
#     full_name = models.CharField(max_length=100, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = []

#     objects = StudentManager()

#     def __str__(self):
#         return self.email



from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# ---------------- STUDENT USER MANAGER ----------------
class StudentManager(BaseUserManager):
    def create_user(self, mobile_number, **extra_fields):
        if not mobile_number:
            raise ValueError("Mobile number is required")
        mobile_number = str(mobile_number)
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_unusable_password()  # No password used in OTP flow
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        if password is None:
            raise ValueError("Superuser requires a password")

        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


# ---------------- STUDENT MODEL ----------------
class Student(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    full_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True, null=True)
    target_course = models.CharField(max_length=200, blank=True, null=True)
    student_class = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "mobile_number"
    REQUIRED_FIELDS = []

    objects = StudentManager()

    class Meta:
        db_table = "StudentData"  # ✅ This ensures table name is exactly StudentData

    def __str__(self):
        return f"{self.mobile_number} - {self.full_name or 'NoName'}"


# ---------------- OTP MODEL ----------------
class OTPRequest(models.Model):
    """
    Stores OTPs issued for a mobile number. Single-use, short TTL.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    mobile_number = models.CharField(max_length=15, db_index=True)
    code = models.CharField(max_length=6)  # 6-digit OTP
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    used = models.BooleanField(default=False)  # mark OTP used after signup/login

    class Meta:
        indexes = [
            models.Index(fields=["mobile_number"]),
        ]
        db_table = "OTPRequest"  # (optional) you can rename if you want a custom table name

    def is_expired(self, minutes=5):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=minutes)

    def __str__(self):
        return f"{self.mobile_number} - {self.code} - verified:{self.verified}"

    