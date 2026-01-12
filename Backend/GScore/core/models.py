from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField
from utilities import  choice
from utilities.models import BaseModel
from GScore import settings



class User(AbstractUser):
    user_type = models.CharField(
        max_length=20,
        choices=choice.UserType,
        default=choice.UserType.STUDENT,
        null=False
    )
    address = models.CharField(max_length=256, blank=True, null=True)
    date_joined=models.DateField(auto_now_add=True,null=True)
    dob = models.DateField(blank=True, null=True)
    email = models.EmailField(blank=False, null=False, unique=True)
    avatar = CloudinaryField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, unique=True, blank=True, null=True)

    class Meta:
        db_table = "user"

class Student(models.Model):
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    registration_number = models.CharField(
        max_length=20,
        unique=True
    )
    full_name = models.CharField(max_length=100)
    course = models.ForeignKey(
        'Course',
        on_delete=models.PROTECT,  
        related_name="students"
    )
    classroom = models.ForeignKey(
        'ClassRoom',
        on_delete=models.CASCADE,
        related_name="students"
    )

    foreign_language_code = models.CharField(
        max_length=5,
        null=True,
        blank=True
    )
    def __str__(self):
        return f"{self.full_name} ({self.course.code})"

class Lecturer(models.Model):
    user = models.OneToOneField(
        'User',
        on_delete=models.CASCADE,
        related_name="lecturer_profile"
    )
    lecturer_code = models.CharField(
        max_length=20,
        unique=True
    )
    full_name = models.CharField(
        max_length=100
    )
    department = models.CharField(
        max_length=100,
        help_text="Tổ / Khoa"
    )

    degree = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    position = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    hire_date = models.DateField(
        blank=True,
        null=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"{self.full_name} ({self.lecturer_code})"

class StudentExamResult(models.Model):
    user = models.OneToOneField(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_score"
    )
    registration_number = models.CharField(max_length=20, unique=True)

    math = models.FloatField(null=True, blank=True)
    literature = models.FloatField(null=True, blank=True)
    foreign_language = models.FloatField(null=True, blank=True)

    physics = models.FloatField(null=True, blank=True)
    chemistry = models.FloatField(null=True, blank=True)
    biology = models.FloatField(null=True, blank=True)

    history = models.FloatField(null=True, blank=True)
    geography = models.FloatField(null=True, blank=True)
    civic_education = models.FloatField(null=True, blank=True)

    foreign_language_code = models.CharField(
        max_length=5,
        null=True,
        blank=True
    )

    course = models.ForeignKey(
        'Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="student_results"
    )

    
class ClassRoom(models.Model):
    code = models.CharField(
        max_length=20,
        unique=True  
    )

    name = models.CharField(
        max_length=50  
    )

    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name="classes"
    )

    homeroom_teacher = models.ForeignKey(
        Lecturer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="homeroom_classes"
    )

    def __str__(self):
        return self.name

    
class Course(BaseModel):

    code = models.CharField(
        max_length=10,
        unique=True,
        help_text="Mã khóa, ví dụ: K2021"
    )
    name = models.CharField(
        max_length=100,
        help_text="Tên khóa, ví dụ: Khóa 2021–2024"
    )
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.code} ({self.start_year}-{self.end_year})"

    
