from django.urls import path

from .views import (
    MarksEntryView,
    BulkMarksEntryView,
    MarksEntryView,
    BulkMarksEntryView,
    MyResultView,
    SectionResultView,
    MeritListView,
    PublishResultView,
)

urlpatterns = [

    path(
        'marks/',
        MarksEntryView.as_view()
    ),

    path(
        'marks/bulk/',
        BulkMarksEntryView.as_view()
    ),
      path(
        'marks/',
        MarksEntryView.as_view()
    ),

    path(
        'marks/bulk/',
        BulkMarksEntryView.as_view()
    ),

    path(
        'results/<int:exam_id>/my/',
        MyResultView.as_view()
    ),

    path(
        'results/<int:exam_id>/section/<int:class_level>/<str:section>/',
        SectionResultView.as_view()
    ),

    path(
        'results/<int:exam_id>/merit-list/',
        MeritListView.as_view()
    ),

    path(
        'exams/<int:exam_id>/publish/',
        PublishResultView.as_view()
    ),

]