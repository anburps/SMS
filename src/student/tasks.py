from celery import shared_task
from django.core.cache import cache
from .models import Student

@shared_task
def cache_student_list():
    students = Student.objects.all()
    if students.exists():
        cache.set('student_list', students, timeout=60*15) 
    return "Cached students list"
