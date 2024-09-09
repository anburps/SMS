from django.urls import path
from .views import *



urlpatterns = [
    path('student_detail/',StudentDetailCreate.as_view()),
    path('student_detail/<int:pk>/',StudentDetailUpdate.as_view()),
    path('student_detail/<int:pk>/delete/',StudentDetailDelete.as_view()),
    path('student_detail_list/',StudentDetailList.as_view()),
    
]
