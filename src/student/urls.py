from django.urls import path
from .views import *

urlpatterns = [
    path('student/list/', StudentListView.as_view(), name='student-list'),
    path('student/create', StudentCreateView.as_view(), name='student-create'),
    path('student/detail/<int:id>/',StudentDetailView.as_view(),name='student-detail'),
    path('course/create/', CourseCreateView.as_view(), name='course-create'),
    path('course/list', CourseListView.as_view(), name='course-list'),
    path('course/detail/', CourseDetailView.as_view(), name='course-detail'),
    path('enrollment/create/', EnrollmentCreateView.as_view(), name='enrollment-create'),
    path('enrollment/list/',EnrollmentListView.as_view(),name='enrollment_list'),
    path('enrollment/detail/', EnrollmentDetailView.as_view(), name='Enrollment-detail'),
    path('grade/create/', GradeCreateView.as_view(), name='grade-create'),
    path('grade/list/', GradelistView.as_view(), name='grade-list'),
    path('grade/detail/', GradeDetailView.as_view(), name='grade-detail'),

    path('attendance/create/', AttendanceCreateView.as_view(), name='attendance-create'),
   
]
