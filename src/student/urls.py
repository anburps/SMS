from django.urls import path
from .views import *

urlpatterns = [
    path('student/create/', StudentListCreateView.as_view(), name='student-create'),
    path('student/detail/<int:id>/',StudentDetailView.as_view(),name='student-detail'),
    path('course/create/', CourseListCreateView.as_view(), name='course-create'),
    path('course/detail/', CourseDetailView.as_view(), name='course-create'),
    path('enrollment/create/', EnrollmentCreateView.as_view(), name='enrollment-create'),
    path('grade/create/', GradeCreateView.as_view(), name='grade-create'),
    path('attendance/create/', AttendanceCreateView.as_view(), name='attendance-create'),
]
