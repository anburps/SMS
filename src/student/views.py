from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from student import serializers as StudentSerializers

# Create your views here.

       
class StudentDetailCreate(APIView):
    
    serializer_class = StudentSerializers.StudentDetailSerializer

    def post(self, request, *args, **kwargs):
        post_data_qset = request.data
        serializer = StudentSerializers.StudentDetailSerializer(data=post_data_qset)

        if serializer.is_valid():
            serializer.save()
            content_data = {
                'provided_by': "SMS API services",
                'success': True,
                'status': 200,
                'data': serializer.data,
            }
            return Response(content_data)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': serializer.errors,
            }
            return Response(content_data)
