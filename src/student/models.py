from django.db import models
from django.contrib.auth.models import User


GENDER_CHOICE = [
        ('--', '--'),
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
        ('TRANSGENDER', 'TRANSGENDER'),
    ]

class StudentDetials(models.Model):
    user            =   models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name="student_name")
    phone_no        =   models.CharField(max_length=12, null=True, blank=True)
    profile_photo   = models.FileField(
                        upload_to="student/profile-photo/",
                        null=True,
                        blank=True,
                    )
    gender          = models.CharField(max_length=12, choices=GENDER_CHOICE, default="--")
    date_of_birth   = models.DateField(null=True, blank=True)
    mother_name     = models.CharField(max_length=60, null=True, blank=True)
    father_name     = models.CharField(max_length=60, null=True, blank=True)
    spouse_name     = models.CharField(max_length=60, null=True, blank=True)
    city            = models.CharField(max_length=50, null=True, blank=True) 
    nationality     = models.CharField(max_length=35, null=True, blank=True)
    religion        = models.CharField(max_length=35, null=True, blank=True)
    physically_challenged = models.BooleanField(default=False)
    created_date    = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_date']    
    
    def __str__(self) -> str:
        return "{}--{}".format(self.pk, self.user)