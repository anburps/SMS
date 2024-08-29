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
            content_data = {}
            content_data['provided_by'] = "Soundarya API services"
            content_data['success'] = True
            content_data['status'] = 200
            content_data['data'] = serializer.data
            return Response(content_data)
        else:
            content_data = {}
            content_data['provided_by'] = "Soundarya API services"
            content_data['success'] = False
            content_data['status'] = 400
            content_data['error'] = serializer.errors
            return Response(content_data)
