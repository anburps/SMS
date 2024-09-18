from rest_framework import serializers
from student import models as StudentModels


class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModels.Student
        fields =(
            'first_name',
            'email',
            'phone_number'
        )

class StudentDetailUpdateSerializer(serializers.ModelSerializer):
    student = StudentDetailSerializer()
    class Meta:
        model = StudentModels.Student
        fields =(
            'last_name',
            'gender',
            'date_of_birth',
            'address',
            'profile_picture'
        )

class CourceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModels.Course
        fields =(
            'course_name',
            'course_code',
            'description',
            'credits',
            'duration_weeks',
            'start_date'
        )
class EnrollmentSerializer(serializers.ModelSerializer):
    