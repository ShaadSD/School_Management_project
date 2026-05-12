from django.contrib import admin
from .models import Subject, SubjectAssignment,Exam


admin.site.register(Subject)
admin.site.register(SubjectAssignment)
admin.site.register(Exam)