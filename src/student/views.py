from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.generics import GenericAPIView
from student import serializers as StudentSerializers
from rest_framework import status
from .models import *
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
from .tasks import cache_student_list 

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 2  
    page_size_query_param = 'page_size'  
    max_page_size = 100  



class StudentListCreateView(generics.ListCreateAPIView):
    serializer_class = StudentSerializers.StudentDetailSerializer
    queryset = Student.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'phone_number', 'email']
    ordering_fields = ['first_name', 'last_name', 'phone_number', 'email', '-id']
    pagination_class = CustomPageNumberPagination

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            self.authentication_classes = [BasicAuthentication, TokenAuthentication]
            self.permission_classes = [IsAuthenticated]
        elif request.method == 'GET':
            self.authentication_classes = []
            self.permission_classes = [AllowAny]
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            cache.delete('student_list')

            content_data = {
                'provided_by': "SMS API services",
                'success': True,
                'status': 200,
                'data': serializer.data,
            }
            return Response(content_data, status=status.HTTP_201_CREATED)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': serializer.errors,
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        cached_students = cache.get('student_list')
        if cached_students is None:
            cache_student_list.delay()  
            # queryset = self.filter_queryset(self.get_queryset())

            # if queryset.exists():
            #     pass
            # else:
            #     content_data = {
            #         'provided_by': "SMS API services",
            #         'success': False,
            #         'status': 400,
            #         'error': "No data found",
            #     }
            #     return Response(content_data, status=status.HTTP_400_BAD_REQUEST)
        # else:
        #     queryset = cached_students

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            content_data = {
                'provided_by': "SMS API service per page 2 data here.",
                'success': True,
                'status': 200,
                'data': serializer.data,
            }
            return self.get_paginated_response(content_data)

        serializer = self.get_serializer(queryset, many=True)
        content_data = {
            'provided_by': "SMS API service per page 2 data here.",
            'success': True,
            'status': 200,
            'data': serializer.data,
            'count': queryset.count(),
        }
        return Response(content_data, status=status.HTTP_200_OK)

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializers.StudentDetailSerializer
    authentication_classes = [BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    def get_object(self):
        try:
            return Student.objects.get(id=self.kwargs['id'])
        except Student.DoesNotExist:
            raise Http404("Student not found.")

    def get(self, request, *args, **kwargs):
        student = self.get_object()
        serializer = self.get_serializer(student)
        content_data = {
            'provided_by': "SMS API services",
            'success': True,
            'status': 200,
            'data': serializer.data
        }
        return Response(content_data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        student = self.get_object()
        serializer = self.get_serializer(student, data=request.data)

        if serializer.is_valid():
            serializer.save()
            content_data = {
                'provided_by': "SMS API services",
                'success': True,
                'status': 200,
                'data': serializer.data
            }
            return Response(content_data, status=status.HTTP_200_OK)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': serializer.errors
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
                'data': serializer.data
            }
            return Response(content_data, status=status.HTTP_200_OK)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': serializer.errors
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

class CourseListCreateView(generics.ListCreateAPIView):
    serializer_class = StudentSerializers.CourseDetailSerializer
    filter_backends = [SearchFilter]
    search_fields = ['course_name', 'course_code']
    ordering_fields = ['id', 'course_name', 'course_code', 'description', 'credits', 'duration_weeks', 'start_date', 'end_date']

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            self.authentication_classes = [BasicAuthentication,TokenAuthentication]
            self.permission_classes = [IsAuthenticated]
        elif request.method == 'GET':
            self.authentication_classes = []
            self.permission_classes = [AllowAny]
        return super().dispatch(request, *args, **kwargs)

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
        course_details_list=cache.get("course_details")
        if course_details_list:
            return Response(course_details_list)
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
    authentication_classes = [BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

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
    def delete(self, request, *args, **kwargs):
        course=self.get_object()
        course.delete()
        content_data = {
            'provided_by': "SMS API services",
            'success': True,
            'status': 204,
            'message': "Course successfully deleted."
        }
        return Response(content_data, status=status.HTTP_204_NO_CONTENT)

class EnrollmentCreateView(generics.ListCreateAPIView):
    serializer_class = StudentSerializers.EnrollmentSerializer
    data = Enrollment.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ['course_name', 'course_code']
    ordering_fields = ['id', 'course_name', 'course_code', 'description', 'credits', 'duration_weeks', 'start_date', 'end_date']

    

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            self.authentication_classes = [BasicAuthentication,TokenAuthentication]
            self.permission_classes = [IsAuthenticated]
        elif request.method == 'GET':
            self.authentication_classes = []
            self.permission_classes = [AllowAny]
        return super().dispatch(request, *args, **kwargs)
    
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
class EntrollmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enrollment.objects.all()
    serializer_class =  StudentSerializers.EnrollmentSerializer
    authentication_classes = [BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        try:
            return Enrollment.objects.get(id=self.kwargs['id'])
        except Enrollment.DoesNotExist:
            raise Http404("Enrollment not found.")

    def put(self, request, *args, **kwargs):
        enrollment = self.get_object()  
        serializer = self.get_serializer(enrollment, data=request.data)

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
        enrollment = self.get_object() 
        serializer = self.get_serializer(enrollment, data=request.data, partial=True)

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
        enrollment=self.get_object()
        enrollment.delete()
        content_data = {
            'provided_by': "SMS API services",
            'success': True,
            'status': 204,
            'message': "Enrollment successfully deleted."
        }
        return Response(content_data, status=status.HTTP_204_NO_CONTENT)


class GradeCreateView(generic.CreateAPIView):
    serializer_class = StudentSerializers.GradeSerializer
    data = Enrollment.objects.all()
    
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            self.authentication_classes = [BasicAuthentication,TokenAuthentication]
            self.permission_classes = [IsAuthenticated]
        elif request.method == 'GET':
            self.authentication_classes = []
            self.permission_classes = [AllowAny]
        return super().dispatch(request, *args, **kwargs) 

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

class GradeListView(generic.ListAPIView):
    serializer_class = StudentSerializers.AttendanceSerializer
    queryset = Attendance.objects.all()
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter]
    search_fields = ['student__name']
    ordering_fields = ['student__name']
    pagination_class = pagination.PageNumberPagination

    def get(self, request, *args, **kwargs):
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

class GradeDetailView(generic.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializers.GradeSerializer
    
    def put(self, request, *args, **kwargs):
        grade = self.get_object()
        serializer = self.get_serializer(grade, data=request.data)

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
        grade = self.get_object() 
        serializer = self.get_serializer(grade, data=request.data, partial=True)

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
        grade = self.get_object()
        grade.delete()
        content_data = {
            'provided_by': "SMS API services",
            'success': True,
            'status': 204,
            'message': "Grade successfully deleted."
        }
        return Response(content_data, status=status.HTTP_204_NO_CONTENT)
        
class AttendanceCreateView(generic.CreateAPIView):
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
class AttendanceListView(generic.ListAPIView):
    serializer_class = StudentSerializers.AttendanceSerializer
    queryset = Attendance.objects.all()
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cache_data = cache.get("attendance")
        if cache_data:
            return Response(cache_data)

        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            content_data = {
                'provided_by': "SMS API services",
                'success': True,
                'status': 200,
                'data': serializer.data,
                'count': queryset.count(),
            }
            cache.set("attendance", content_data,timeout=300)
            return Response(content_data, status=status.HTTP_200_OK)
        else:
            content_data = {
                'provided_by': "SMS API services",
                'success': False,
                'status': 400,
                'error': "No data found",
            }
            return Response(content_data, status=status.HTTP_400_BAD_REQUEST)

class AttendanceDetailUpdateView(generic.RetrieveUpdateDestroyAPIView):
    serializer_class = StudentSerializers.AttendanceSerializer
    queryset = Attendance.objects.all()
    authentication_classes = [BasicAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    search_fields = ['student']
    

    def patch(self,request, *args, **kwargs):
        attendance = self.get_object()
        serializer = self.get_serializer(attendance, data=request.data, partial=True)
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
        grade = self.get_object()
        grade.delete()
        content_data = {
            'provided_by': "SMS API services",
            'success': True,
            'status': 204,
            'message': "Grade successfully deleted."
        }
        return Response(content_data, status=status.HTTP_204_NO_CONTENT)
        