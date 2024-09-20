from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Student

@receiver(post_save, sender=Student)
def send_email_after_student_creation(sender, instance, created, **kwargs):
    if created:  
        subject = "Welcome to Our Service"
        message = f"Dear {instance.first_name}{instance.last_name},\n\nWelcome to our service! Your details have been successfully registered."
        from_email = settings.DEFAULT_FROM_EMAIL 
        recipient_list = [instance.email] 
        send_mail(subject, message, from_email, recipient_list)
