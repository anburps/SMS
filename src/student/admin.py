from django.contrib import admin
from .models import *

class StudentAdmin(admin.ModelAdmin):
    list_display    = ('full_name', 'gender', 'date_of_birth', 'email', 'phone_number', 'address', 'enrollment_date', 'profile_picture')
    search_fields   =  ('full_name', 'email')

class CourseAdmin(admin.ModelAdmin):
    list_display    = ('course_name', 'course_code', 'description', 'credits', 'duration_weeks', 'start_date', 'end_date')
    search_fields   =  ('course_name', 'course_code')

class EnrollmentAdmin(admin.ModelAdmin):
    list_display    = ('student', 'course', 'enrollment_date', 'grade', 'status')
    search_fields   =  ('student__full_name', 'course__course_name')

class GradeAdmin(admin.ModelAdmin):
    list_display    = ('student', 'course', 'assignment', 'score', 'grade_date')
    search_fields   =  ('student__full_name', 'assignment__title')


class TeacherAdmin(admin.ModelAdmin):
    list_display    = ('full_name', 'email', 'phone_number', 'department', 'hire_date', 'profile_picture')
    search_fields   =  ('full_name', 'email')

class AttendanceAdmin(admin.ModelAdmin):
    list_display    = ('student', 'date', 'status')
    search_fields   =  ('student__full_name', 'date')

class AssignmentAdmin(admin.ModelAdmin):
    list_display    = ('title', 'course', 'due_date', 'is_overdue')
    search_fields   =  ('title', 'course__course_name')

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Grade, GradeAdmin)
admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(Assignment, AssignmentAdmin)

admin.site_header = "SMS"
admin.site_title = "SMS"
admin.site_index_title = "SMS"
