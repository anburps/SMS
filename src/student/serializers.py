from rest_framework import serializers
from .models import *
class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentDetailSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    student = StudentDetailSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    assignment = AssignmentSerializer(read_only=True)

    class Meta:
        model = Grade
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentDetailSerializer(read_only=True)
    course = CourseSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'
