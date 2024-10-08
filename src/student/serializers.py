from rest_framework import serializers
from .models import *
from datetime import date 

class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'
    
    def validate_full_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Full name must contain only letters.")

        return value
    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Last name must contain only letters.")

        return value
    
    def validate_date_of_birth(self, value):
        today = date.today()
        
        if value > today:
            raise serializers.ValidationError("Date of birth cannot be in the future.")
        
        age = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        
        if age < 18:
            raise serializers.ValidationError("User must be at least 18 years old.")
        
        return value
    def validate_phone_number(self, value):
        if len(value) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits long.")
        
        return value
   
class CourseDetailSerializer(serializers.ModelSerializer):
    studentcourse = StudentDetailSerializer(many=True)
    class Meta:
        model = Course
        fields = '__all__'
    
    def validate_course_name(self,value):
        if not value.isalpha():
            raise serializers.ValidationError("Full name must contain only letters.")

        return value
    def validate_start_date(self, value):
        today = date.today()
        
        if value > today:
            raise serializers.ValidationError("Start date cannot be in the future.")
        
        return value

class EnrollmentSerializer(serializers.ModelSerializer):
    student = StudentDetailSerializer(read_only=True)
    course = CourseDetailSerializer(read_only=True)

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
    course = CourseDetailSerializer(read_only=True)
    assignment = AssignmentSerializer(read_only=True)

    class Meta:
        model = Grade
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentDetailSerializer(read_only=True)
    course = CourseDetailSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = '__all__'
