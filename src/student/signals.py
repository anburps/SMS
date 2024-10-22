from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Student
from django.contrib.auth.models import User

@receiver(post_save, sender=Student)
def send_email_after_student_creation(sender, instance, created, **kwargs):
    if created:
        password = instance.date_of_birth.strftime('%Y-%m-%d') 

        user = User.objects.create_user(
            username=instance.email,  
            email=instance.email,
            password=password,  
        )
        user.save()
        subject = "Welcome to Our Service"
        message = f"Dear {instance.first_name}{instance.last_name},\n\nWelcome to our service! Your details have been successfully registered.\n\n Username: {instance.email}\nPassword: {password}\n\nThank you for choosing our service." 
        from_email = settings.DEFAULT_FROM_EMAIL 
        recipient_list = [instance.email] 
        send_mail(subject, message, from_email, recipient_list)

@receiver(post_save,sender=Teacher)
def send_email_employee_creation(sender,instance,created, **kwargs):
    if created:
        subject = "Welcome to Our Service"
        message = f"Dear {instance.first_name}{instance.last_name},\n\nWelcome to our service! Your details have been successfully registered.\n\n employee_id: {instance.employee_id}\hire_date: {instance.hire_date}\n\nThank you for choosing our service." 
        from_email = settings.DEFAULT_FROM_EMAIL 
        recipient_list = [instance.email] 
        send_mail(subject, message, from_email, recipient_list)
        