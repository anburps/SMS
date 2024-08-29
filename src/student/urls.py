from django.urls import path
from .views import *



urlpatterns = [
    path('student_detail/',StudentDetailCreate.as_view()),
    
]
