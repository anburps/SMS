from django.urls import path
from .views import *

urlpatterns = [
    path('student/create/', StudentCreateView.as_view(), name='student-create'),
    path('course/create/', CourseCreateView.as_view(), name='course-create'),
    path('enrollment/create/', EnrollmentCreateView.as_view(), name='enrollment-create'),
    path('grade/create/', GradeCreateView.as_view(), name='grade-create'),
    path('attendance/create/', AttendanceCreateView.as_view(), name='attendance-create'),
]
