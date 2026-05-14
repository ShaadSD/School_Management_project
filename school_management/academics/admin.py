from django.contrib import admin
from .models import Subject, SubjectAssignment, Exam


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    search_fields = ('name',)


admin.site.register(SubjectAssignment)