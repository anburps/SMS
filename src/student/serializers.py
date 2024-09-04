from rest_framework import serializers
from student import models as StudentModels


class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentModels.Student
        fields ="__all__"
