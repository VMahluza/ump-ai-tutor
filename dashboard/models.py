from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator


# START OF COURSE MODEL
class Course(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name

# ./END OF COURSE MODEL

# Create your models here.
# START OF USER MODEL
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STUDENT = "STUDENT", "Student"
        LECTURE = "LECTURE", "LECTURE"
        TUTOR = "TUTOR", "TUTOR"

    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
    auth_key = models.CharField(unique=True, null=True, blank=True,max_length=9)

    

    base_role = Role.ADMIN
    role = models.CharField(max_length=50, choices=Role.choices)
    groups = models.ManyToManyField(
        Group,
        blank=True,
        related_name="user_set",
        related_query_name="user",
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    gender = models.CharField(max_length=50, default=Gender.MALE, choices=Gender.choices)
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)
        else:
          return super().save(*args, **kwargs)
# ./END OF USER MODEL

# START OF REGISTRATION MODEL
class Registration(models.Model):
    class Level(models.TextChoices):
        FIRST_YEAR =  "1", "First Year"
        SECOND_YEAR = "2", "Second Year"
        THIRD_YEAR =  "3","Third Year"
        FORTH_YEAR =  "4", "4th Year"
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, blank=True, null=True, on_delete=models.SET_NULL)
    documents = models.FileField(blank=True, null=True, upload_to="media/user/documents")
    level_of_study = models.CharField(max_length=50, default=Level.FIRST_YEAR, choices=Level.choices)

# ./END OF REGISTRATION MODEL


# START OF STUDENT MODEL
class StudentManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.STUDENT)
class Student(User):
    base_role = User.Role.STUDENT
    student = StudentManager()

    class Meta:
        proxy = True

    def welcome(self):
        return "Only for Students"
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
# This function automatically create a new student profile when a student is created
@receiver(post_save, sender=Student)
def create_student_profile(sender, instance, created, **kwargs):
    if created and instance.role == "STUDENT":
        student_group = Group.objects.get(name='Student')
        instance.groups.add(student_group)
        StudentProfile.objects.create(user=instance)
# ./END OF STUDENT MODEL

# START OF LECTURE MODEL
class LectureManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.LECTURE) 
class Lecture(User):
    base_role = User.Role.LECTURE
    lecture = LectureManager()
    class Meta:
        proxy = True
    def welcome():
        return "Only for Students"
class LectureProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
# This function automatically create a new student profile when a student is created
@receiver(post_save, sender=Lecture)
def create_lecture_profile(sender, instance, created, **kwargs):
    if created and instance.role == "LECTURE":
        lecture_group = Group.objects.get(name='Lecture')
        instance.groups.add(lecture_group)
        LectureProfile.objects.create(user=instance)  
# ./END OF LECTURE MODEL

# START OF TUTOR MODEL
class TutorManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.TUTOR) 
class Tutor(User):
    base_role = User.Role.TUTOR
    tutor = TutorManager()
    class Meta:
        proxy = True
    def welcome():
        return "Only for Students"
class TutorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
# This function automatically create a new student profile when a student is created
@receiver(post_save, sender=Tutor)
def create_tutor_profile(sender, instance, created, **kwargs):
    if created and instance.role == "TUTOR":
        tutor_group = Group.objects.get(name='Tutor')
        instance.groups.add(tutor_group)
        TutorProfile.objects.create(user=instance)  
# ./END OF TUTOR MODEL


class AuthKeys(models.Model):
    class Role(models.TextChoices):
        LECTURE = "LECTURE", "LECTURE"
        TUTOR = "TUTOR", "TUTOR"
    role = models.CharField(max_length=50, blank=True, choices=Role.choices)
    authkey = models.CharField(unique=True, null=True, blank=True,max_length=9)
    available = models.BooleanField(default=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)

    
