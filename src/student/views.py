from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from student import serializers as StudentSerializers
from rest_framework import status
from .models import *

class StudentListCreateView(generics.ListCreateAPIView):
    serializer_class = StudentSerializers.StudentDetailSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content_data = {
                'provided_by': "SMS API services",
                'success': True,
                'status': 200,
                'data': serializer.data,
            }
            return Response(content_data, status=status.HTTP_200_OK)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': serializer.errors,
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)

    def get(self,request,*args,**kwargs):
        queryset        = Student.objects.all()

        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            content_data = {
                'provided_by': "SMS API services",
                'success': True,
                'status': 200,
                'data': serializer.data,
                'count': queryset.count(),
            }
            return Response(content_data, status=status.HTTP_200_OK)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': "No data found",
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)


class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class =  StudentSerializers.StudentDetailSerializer

    def get_object(self):
        try:
            return Student.objects.get(id=self.kwargs['id'])
        except Student.DoesNotExist:
            raise Http404("Student not found.")

    def put(self, request, *args, **kwargs):
        student = self.get_object()  
        serializer = self.get_serializer(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            content_data = {
                'provided_by': "SMS API services",
                'success': True,
                'status': 200,
                'data': serializer.data,
            }
            return Response(content_data, status=status.HTTP_200_OK)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': serializer.errors,
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        student = self.get_object() 
        serializer = self.get_serializer(student, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            content_data = {
                'provided_by': "SMS API services",
                'success': True,
                'status': 200,
                'data': serializer.data,
            }
            return Response(content_data, status=status.HTTP_200_OK)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': serializer.errors,
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        student = self.get_object() 
        student.delete()
        content_data = {
            'provided_by': "SMS API services",
            'success': True,
            'status': 204,
            'message': "Student successfully deleted."
        }
        return Response(content_data, status=status.HTTP_204_NO_CONTENT)

class CourseListCreateView(generic.ListCreateAPIView):
    serializer_class = StudentSerializers.CourseSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content_data = {
                'provided_by': "SMS API services",
                'success': True,
                'status': 200,
                'data': serializer.data,
            }
            return Response(content_data, status=status.HTTP_200_OK)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': serializer.errors,
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)
    def get(self, request, *args, **kwargs):
        queryset = Course.objects.all()

        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            content_data = {
                'provided_by': "SMS API services",
                'success': True,
                'status': 200,
                'data': serializer.data,
                'count': queryset.count(),
            }
            return Response(content_data, status=status.HTTP_200_OK)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': "No data found",
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)


class CourseDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Course.objects.all()
    serializer_class =  StudentSerializers.CourseDetailSerializer

    def get_object(self):
        try:
            return Course.objects.get(id=self.kwargs['id'])
        except Course.DoesNotExist:
            raise Http404("Course not found.")
    def put(self, request, *args, **kwargs):
        course = self.get_object()  
        serializer = self.get_serializer(course, data=request.data)

        if serializer.is_valid():
            serializer.save()
            content_data = {
                'provided_by': "SMS API services",
                'success': True,
                'status': 200,
                'data': serializer.data,
            }
            return Response(content_data, status=status.HTTP_200_OK)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': serializer.errors,
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, *args, **kwargs):
        course = self.get_object() 
        serializer = self.get_serializer(course, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            content_data = {
                'provided_by': "SMS API services",
                'success': True,
                'status': 200,
                'data': serializer.data,
            }
            return Response(content_data, status=status.HTTP_200_OK)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': serializer.errors,
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)

class EnrollmentCreateView(GenericAPIView):
    serializer_class = StudentSerializers.EnrollmentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content_data = {
                'provided_by': "SMS API services",
                'success': True,
                'status': 200,
                'data': serializer.data,
            }
            return Response(content_data, status=status.HTTP_200_OK)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': serializer.errors,
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)


class GradeCreateView(GenericAPIView):
    serializer_class = StudentSerializers.GradeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content_data = {
                'provided_by': "SMS API services",
                'success': True,
                'status': 200,
                'data': serializer.data,
            }
            return Response(content_data, status=status.HTTP_200_OK)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': serializer.errors,
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)


class AttendanceCreateView(GenericAPIView):
    serializer_class = StudentSerializers.AttendanceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            content_data = {
                'provided_by': "SMS API services",
                'success': True,
                'status': 200,
                'data': serializer.data,
            }
            return Response(content_data, status=status.HTTP_200_OK)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': serializer.errors,
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)