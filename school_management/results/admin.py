from django.contrib import admin

from .models import (
    StudentMark,
    StudentResult
)


# ====================================
# STUDENT MARK ADMIN
# ====================================
@admin.register(StudentMark)
class StudentMarkAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'student',
        'exam',
        'subject',
        'total_marks',
        'letter_grade',
        'grade_point',
        'is_absent',
        'created_at'
    )

    list_filter = (
        'exam',
        'subject',
        'letter_grade',
        'is_absent'
    )

    search_fields = (
        'student__username',
        'subject__name',
        'exam__name'
    )

    ordering = (
        '-created_at',
    )

    readonly_fields = (
        'total_marks',
        'letter_grade',
        'grade_point',
        'created_at',
        'updated_at'
    )

    autocomplete_fields = (
        'student',
        'exam',
        'subject'
    )



# ====================================
# STUDENT RESULT ADMIN
# ====================================
@admin.register(StudentResult)
class StudentResultAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'student',
        'exam',
        'gpa',
        'total_marks',
        'class_position',
        'is_passed',
        'created_at'
    )

    list_filter = (
        'exam',
        'is_passed'
    )

    search_fields = (
        'student__username',
        'exam__name'
    )

    ordering = (
        'class_position',
        '-gpa',
        '-total_marks'
    )

    readonly_fields = (
        'gpa',
        'total_marks',
        'total_grade_points',
        'number_of_subjects',
        'created_at',
        'updated_at'
    )

    autocomplete_fields = (
        'student',
        'exam'
    )