from django.urls import path

from .views import (
    MarkAttendanceView,
    MyAttendanceView,
    ChildAttendanceView,
    SectionAttendanceView,
    AttendanceReportView
)

urlpatterns = [

    path(
        'attendance/mark/',
        MarkAttendanceView.as_view()
    ),

    path(
        'attendance/my/',
        MyAttendanceView.as_view()
    ),

    path(
        'attendance/children/<int:child_id>/',
        ChildAttendanceView.as_view()
    ),

    path(
        'attendance/section/<int:class_level>/<str:section>/',
        SectionAttendanceView.as_view()
    ),

    path(
        'attendance/report/',
        AttendanceReportView.as_view()
    ),
]