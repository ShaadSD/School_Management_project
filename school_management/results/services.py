from .models import StudentMark, StudentResult
from accounts.models import StudentProfile


def calculate_student_result(student, exam):

    marks = StudentMark.objects.filter(
        student=student,
        exam=exam
    ).select_related('subject')

    if not marks.exists():
        return None

    total_marks = 0

    total_grade_points = 0

    number_of_subjects = 0

    is_passed = True

    optional_subject_bonus = 0

    for mark in marks:

        total_marks += mark.total_marks

        subject = mark.subject

        gp = mark.grade_point

    
        if (
            subject.subject_type == 'compulsory'
            and gp == 0
        ):
            is_passed = False

      
        if subject.subject_type == 'optional_4th':

            if gp > 2:
                optional_subject_bonus = gp - 2

        else:
            total_grade_points += gp
            number_of_subjects += 1

  
    if number_of_subjects > 0:

        gpa = (
            total_grade_points +
            optional_subject_bonus
        ) / number_of_subjects

    else:
        gpa = 0

    gpa = min(round(gpa, 2), 5.0)

    # IF FAILED -> GPA 0
    if not is_passed:
        gpa = 0

    result, created = StudentResult.objects.update_or_create(
        student=student,
        exam=exam,

        defaults={
            'gpa': gpa,
            'total_marks': total_marks,
            'is_passed': is_passed,
            'total_grade_points': total_grade_points,
            'number_of_subjects': number_of_subjects,
        }
    )

    return result





def generate_merit_list(exam, class_level=None, section=None):

    results = StudentResult.objects.filter(
        exam=exam
    ).select_related(
        'student'
    )

    # FILTER BY CLASS
    if class_level:

        student_ids = StudentProfile.objects.filter(
            class_level=class_level
        ).values_list(
            'user_id',
            flat=True
        )

        results = results.filter(
            student_id__in=student_ids
        )

    # FILTER BY SECTION
    if section:

        student_ids = StudentProfile.objects.filter(
            section=section
        ).values_list(
            'user_id',
            flat=True
        )

        results = results.filter(
            student_id__in=student_ids
        )

    # SORTING
    results = results.order_by(
        '-gpa',
        '-total_marks'
    )

    current_position = 1

    for result in results:

        result.class_position = current_position

        result.save()

        current_position += 1

    return results
