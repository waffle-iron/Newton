from django import template

from brain.models import StudentRoster, CurrentClass, Teacher
from amc.models import AMCTestResult, AMCTest
from ixl.models import IXLSkill, IXLSkillScores
from nwea.models import NWEASkill, NWEAScore, RITBand

from libs.functions import nwea_recommended_skills_list as nwea_skills

register = template.Library()


# TODO: Student Status with ENI Skills
# TODO: Student Status with IXL Skills
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

# TODO: Sort list by lowest RIT Band


@register.simple_tag(name='nwea_recommended_skills_list')
def nwea_recommended_skills_list(student, arg):
    return nwea_skills(student, arg)


@register.simple_tag(name='class_recommendation_list')
def class_recommendation_list(student_list):
    skill_list=[]
    for student in student_list:
        skill_list.append(nwea_skills(student, "recommended_skill_list"))
    return skill_list


def percentage(part, whole):
    answer = 100 * float(part) / float(whole)
    answer = int(round(answer))
    return answer

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
