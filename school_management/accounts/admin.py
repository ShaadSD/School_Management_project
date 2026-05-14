from django.contrib import admin
from .models import (
    User,
    StudentProfile,
    TeacherProfile,
    ParentStudentLink
)


# =========================
# USER ADMIN
# =========================
@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'username',
        'email',
        'role',
        'phone',
        'is_staff'
    )

    list_filter = (
        'role',
        'is_staff',
        'is_superuser'
    )

    search_fields = (
        'username',
        'email',
        'phone'
    )



# =========================
# STUDENT PROFILE ADMIN
# =========================
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'roll_number',
        'class_level',
        'section',
        'group'
    )

    list_filter = (
        'class_level',
        'section',
        'group'
    )

    search_fields = (
        'user__username',
        'roll_number'
    )



# =========================
# TEACHER PROFILE ADMIN
# =========================
@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'employee_id',
        'department',
        'designation'
    )

    list_filter = (
        'department',
        'designation'
    )

    search_fields = (
        'user__username',
        'employee_id'
    )



# =========================
# PARENT STUDENT LINK ADMIN
# =========================
@admin.register(ParentStudentLink)
class ParentStudentLinkAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'parent',
        'student',
        'relationship',
        'access_code'
    )

    list_filter = (
        'relationship',
    )

    search_fields = (
        'parent__username',
        'student__username'
    )