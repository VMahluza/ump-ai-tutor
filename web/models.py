from django.db import models


# Create your models here.
class UserRequest(models.Model):
    email = models.CharField(max_length=50, null=False, blank=False)
    phone = models.CharField(max_length=10, null=False, blank=False)
    id_document = models.ImageField(upload_to='images/user_requests/', null=True, blank=True)
    proof_of_employment = models.FileField(upload_to='images/user_requests/', null=True, blank=True)

    def __str__(self):
        return self.email
    
