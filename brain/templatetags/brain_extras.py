from django import template

from brain.models import StudentRoster, CurrentClass, Teacher
from amc.models import AMCTestResult, AMCTest
from ixl.models import IXLSkill
from nwea.models import NWEASkill, NWEAScore, RITBand
from brain.scripts.recommended_skills_list import recommended_skills_list

register = template.Library()


# TODO: Next IXL Skills to Master
# TODO: Current NWEA Approximation
# TODO: Student Status with ENI Skills
# TODO: Student Status with IXL Skills
# TODO: Student Status with NWEA Skills
# TODO: Student Status with CBA Skills

#=========================================================================================================
#                                           AMC
#=========================================================================================================
@register.filter(name='current_amc_test')
def current_amc_test(value):
    """Gets the current AMC test for a student"""
    if AMCTestResult.objects.all().filter(student_id=value):
        last_test_taken = AMCTestResult.objects.all().filter(student_id=value).order_by('-date_tested')[0]
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
    output = AMCTest.objects.get(test_number=value)
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


@register.filter(name='amc_badges_earned')
def amc_badges_earned(value):
    test_list = AMCTestResult.objects.all().filter(student=value)
    x = 0
    for test in test_list:
        passed = test.passing_score()
        if passed:
            x += 1
    return x


@register.filter(name='amc_teacher_badges_earned')
def amc_teacher_badges_earned(value):
    x = 0
    for student in value:
        test_list = AMCTestResult.objects.all().filter(student=student)
        for test in test_list:
            passed = test.passing_score()
            if passed:
                x += 1
    return x



#=========================================================================================================
#                                              IXL
#=========================================================================================================


@register.filter(name='get_ixl_url')
def get_ixl_url(value):
    skill_id = value.upper()
    skill = IXLSkill.objects.all().get(skill_id=skill_id)
    description_string = skill.skill_description.replace('-', '').replace("'", '').replace(",", "").replace('/', '') \
        .replace('?', '').replace('.', '').replace(':', '').replace('$1', 'one dollar').replace("$5", "five dollars")
    description_string = description_string.replace('   ', ' ').replace('  ', ' ')
    description_string = description_string.replace(' ', '-')
    url = str("https://www.ixl.com/math/level-" + skill.skill_id[0] + '/' + description_string).lower()
    return url




#=========================================================================================================
#                                              NWEA
#=========================================================================================================


@register.filter(name='nwea_recommended_skills_list')
def nwea_recommended_skills_list(value, arg):
    '''Gets back list of next skills for student. value is a student object'''
    actual_nwea_scores, estimated_nwea_scores, recommended_skill_list, subdomain_percentage_complete =  recommended_skills_list(value)
    if arg == "actual_nwea_scores":
        return actual_nwea_scores
    elif arg == "estimated_nwea_scores":
        return estimated_nwea_scores
    elif arg == "recommended_skill_list" or arg == "":
        return recommended_skill_list
    elif arg == "subdomain_percentage_complete":
        return subdomain_percentage_complete
    else:
        return None















#=========================================================================================================
#                                           NAVIGATION
#=========================================================================================================


@register.inclusion_tag('brain/classes_nav.html')
def nav_teachers_list():
    teachers = Teacher.objects.all()
    return {'teachers': teachers}


@register.inclusion_tag('amc/classes_nav.html')
def nav_amc_teachers_list():
    teachers = Teacher.objects.all()
    return {'teachers': teachers}

@register.inclusion_tag('ixl/ixl_nav.html')
def nav_ixl_list():
    return


    # @register.inclusion_tag('brain/students')
