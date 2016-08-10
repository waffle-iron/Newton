from django import template

from brain.models import StudentRoster, CurrentClass, Teacher
from amc.models import AMCTestResult, AMCTest


register = template.Library()


# TODO: Next IXL Skills to Master
# TODO: Current NWEA Approximation
# TODO: Student Status with ENI Skills
# TODO: Student Status with IXL Skills
# TODO: Student Status with NWEA Skills
# TODO: Student Status with CBA Skills


@register.filter(name='current_amc_test')
def current_amc_test(value):
    """Gets the current AMC test for a student"""
    if AMCTestResult.objects.all().filter(student_id=value).count() > 0:
        last_test_taken = AMCTestResult.objects.all().filter(student_id=value).order_by('-date_taken')[0]
        if last_test_taken.passing_score():
            amc_test = last_test_taken.test.test_number + 1
        elif not last_test_taken.passing_score():
            amc_test = last_test_taken.test.test_number
        else:
            amc_test = "Error"

        return amc_test
    else:
        return 1


@register.filter(name='amc_number_to_text')
def amc_number_to_text(value):
    output = AMCTest.objects.get(test_number= value)
    return output

@register.filter(name='amc_number_of_test_attempts')
def amc_number_of_test_attempts(value, test):
    student = value
    if AMCTestResult.objects.all().filter(student_id=student).filter(test=test):
        count = AMCTestResult.objects.all().filter(student_id=student).filter(test=test).count()
        return count
    else:
        return 0


@register.filter(name='amc_grade_equivalent')
def amc_grade_equivalent(value):
    """Turns a current AMC test number into the grade equivalent."""
    output = AMCTest.objects.get(test_number=value)
    return output.grade_equivalent


@register.inclusion_tag('brain/classes_nav.html')
def nav_teachers_list():
    teachers = Teacher.objects.all()
    return {'teachers': teachers}

#@register.inclusion_tag('brain/students')