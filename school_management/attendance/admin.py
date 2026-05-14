from django.contrib import admin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'student',
        'date',
        'status',
        'class_level',
        'section',
        'marked_by',
        'created_at'
    )

    list_filter = (
        'status',
        'class_level',
        'section',
        'date'
    )

    search_fields = (
        'student__username',
        'marked_by__username'
    )

    ordering = (
        '-date',
        '-created_at'
    )

    readonly_fields = (
        'created_at',
    )