from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.mail import send_mail


class LoggedTicket(models.Model):
    guest_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=150)
    resolve = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

@receiver(post_save, sender=LoggedTicket)
def broadcast_logged_ticket_success(sender, instance, created, **kwargs):
    if created:
        from_email = 'binarybendits@gmail.com'
        recipient_list = [instance.email]
        subject = f'#{instance.id}Ticket: {instance.subject}'
        message = f"""
            Hi {instance.guest_name},

            Thank you for reaching out to BinaryBendits.
            We have received your ticket and our team members are actively working on it. Please be patient while we address your query.
            
            You can revisit the following link for updates and further information:
            https://ump-ai-tutor-production.up.railway.app/

            Reference Number: #{instance.id}

            If you have any additional questions or concerns, please don't hesitate to contact us. \n\n

            Best regards, \n
            The BinaryBendits Team
            """

        admin_message = f"""
            Hi All Administrators,
            
            A new ticket has been logged by {instance.guest_name} with email {instance.email}.
            
            Reference Number: #{instance.id}
            
            Please visit the admin panel to attend to this ticket:
            https://ump-ai-tutor-production.up.railway.app/admin
            
            Thank you for your attention.
            
            Best regards,
            BinaryBendits Support Team
            """

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        admins = User.objects.filter(is_staff=True)
        admin_email_list = [admin.email for admin in admins]
        send_mail(subject, admin_message, from_email, admin_email_list, fail_silently=False)

        print("Query received")
# START OF COURSE MODEL
class Course(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self) -> str:
        return self.name

# ./END OF MODULE MODEL
class Module(models.Model):
    code = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(max_length=150, blank=True, null=True)
    course = models.ForeignKey(Course, blank=True, null=True, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.name
# ./END OF MODULE MODEL

def user_directory_path(instance, filename):
    return 'images/user_profile_pictures/{0}/{1}'.format(instance.id, filename)

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
    profile_pic = models.ImageField(upload_to=user_directory_path, null=True, blank=True)
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

    is_online = models.BooleanField(default=False)

    @property
    def get_full_name(self):
        return self.first_name + ' ' + self.last_name
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)
        else:
          return super().save(*args, **kwargs)
        
    def __str__(self):
        return f"{self.username}({self.email})"
        
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
    receive_emails = models.BooleanField(default=False)
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
    receive_emails = models.BooleanField(default=False)

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
    receive_emails = models.BooleanField(default=False)

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


# VOTE MODEL

# ./END OF MODULE MODEL


# ./END OF VOTE MODEL

# ./END OF MODULE MODEL
class Query(models.Model):
    question_text = models.TextField(max_length=1000, null=True, blank=False)
    pub_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # Other fields related to questions
   
    module = models.ForeignKey(Module, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text
    
    @property
    def short_question(self):
        # accesskey[:2] + "*" * 5 +  accesskey[7:]
        return self.question_text[:25] + "."*3
    
    @property
    def answers(self):
        print(self)
        return Answer.objects.filter(query_id=self.id)
    
    @property
    def votes(self):
        votes = Vote.objects.filter(query_id=self.id, vote_type=Vote.UPVOTE)
        print(votes.count())
        return votes.count()
    
    


@receiver(post_save, sender=Query)
def broadcast_question_to_everyone(sender, instance, created, **kwargs):
    if created:
        from_email = 'binarybendits@gmail.com'
        course = instance.course 
        registrations = Registration.objects.filter(course=course)
        recipient_list = [registration.user.email for registration in registrations]
        subject = f'Query for module {instance.module} Have been asked'
        message = f"""
        The question bellow was asked 
        {instance.question_text}
        if you wish to respond to the question please visit the our site 
        https://ump-ai-tutor-production.up.railway.app/
        """
        # send_mail(subject, message, from_email, recipient_list, fail_silently=False) 
        print("Broadcasting Question to everyone doing this module")  

# ./END OF MODULE MODEL
# ./END OF MODULE MODEL
class Answer(models.Model):
    answer_text = models.TextField(max_length=1000, null=True, blank=False)
    pub_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    # Other fields related to questions
    votes = models.IntegerField(default=0, null=True, blank=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE) 
    query = models.ForeignKey(Query, blank=True, null=True, on_delete=models.CASCADE, related_name='answers')

    def __str__(self):
        return self.answer_text
    
    @property
    def short_question(self):
        # accesskey[:2] + "*" * 5 +  accesskey[7:]
        return self.answer_text[:25]


@receiver(post_save, sender=Query)
def broadcast_answer_to_everyone(sender, instance, created, **kwargs):
    if created:
        print("Broadcasting Answer to everyone doing this module")  

# ./END OF MODULE MODEL
class Vote(models.Model):
    UPVOTE = 'UP'
    DOWNVOTE = 'DOWN'

    VOTE_CHOICES = [
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    ]

    vote_date = models.DateTimeField(auto_now=True, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="user_votes")
    query = models.ForeignKey(Query, blank=True, null=True, on_delete=models.CASCADE, related_name="query_votes")
    answer = models.ForeignKey(Answer, blank=True, null=True, on_delete=models.CASCADE, related_name="answer_votes")
    vote_type = models.CharField(max_length=4, choices=VOTE_CHOICES, default="UP")

    class Meta:
        unique_together = ('user', 'query', 'answer')  # Ensure a user can only vote once for a query or answer

    def __str__(self):
        return f"#{self.id}-Vote from {self.user.username}"
