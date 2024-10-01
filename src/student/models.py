from django.db import models
from django.utils import timezone


GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
STUDENT_DETAIL = [('Active', 'Active'), ('Completed', 'Completed')]


class Student(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, unique= True,blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    enrollment_date = models.DateField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    class Meta():
        ordering = ['-id']

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()

class Course(models.Model):
    course_name     = models.CharField(max_length=100)
    course_code     = models.CharField(max_length=10, unique=True)
    description     = models.TextField(blank=True, null=True)
    credits         = models.IntegerField(default=0)
    duration_weeks  = models.IntegerField(default=12)
    start_date      = models.DateField()

    def end_date(self):
        return self.start_date + timezone.timedelta(weeks=self.duration_weeks)

    def __str__(self):
        return self.course_name

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    grade = models.CharField(max_length=2, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STUDENT_DETAIL)

    def __str__(self):
        return f"{self.student.full_name()} enrolled in {self.course.course_name}"


class Teacher(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100)
    hire_date = models.DateField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='teacher_pics/', blank=True, null=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name()


class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    due_date = models.DateField()
    assigned_date = models.DateField(auto_now_add=True)
    max_score = models.DecimalField(max_digits=5, decimal_places=2, default=100.00)

    def is_overdue(self):
        return timezone.now().date() > self.due_date

    def __str__(self):
        return self.title

class Grade(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    grade_date = models.DateField(auto_now_add=True)

    def percentage(self):
        return (self.score / self.assignment.max_score) * 100

    def __str__(self):
        return f"{self.student.full_name()} - {self.assignment.title}: {self.score}"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('Present', 'Present'), ('Absent', 'Absent')])

    def __str__(self):
        return f"{self.student.full_name()} - {self.date}: {self.status}"
