from django import template

from brain.models import StudentRoster, CurrentClass, Teacher
from amc.models import AMCTestResult, AMCTest
from ixl.models import IXLSkill
from nwea.models import NWEASkill, NWEAScore, RITBand

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


@register.filter(name='recommended_skills_list')
def recommended_skills_list(value):
    student = value
    student = StudentRoster.objects.all().get(last_name="Boyd")
    #recent_nwea_scores = NWEAScore.objects.all().filter(student=student).order_by(NWEAScore.test_period).first()



# Get student list
# For student in student list:
#
# If student has IXL exercise scores:
# 	Get those
#
# If student has NWEA test scores:
# Get the most recent scores for each of the 7 domains.
# Else:
# 	Assume student is 141 in all domains. (New students won’t have NWEA data until a month into the year)
#
# If student has CBA + ENI Scores
# get those too.
# Else:
# 	Assume they know nothing.

# Find highest NWEA subdomain level that you know a student has passed (either from NWEA results or IXL),
# Have NWEA RIT Level scores for each student
# Can compute if they’ve passed a RIT Band from IXL
# Start with NWEA Rit band as a floor in each subdomain
# Then check IXL for the next level - have they passed? If so go to next level
#
# In the teacher report - what NWEA subdomain level they’re working, and do you think they’ve passed the previous level because of NWEA test (w/date) or IXL.
#
# Result of this calculation =
# Student → Set of NWEA RIT bands they should be working on (in each subdomain)
# Sort by RIT band number, return top 10
#
# Add another column for CBA with the mapping of NWEA and IXL. If the CBA column is yes (or an upcoming date) Move to top of list of ten.
#
#
# Add fields to IXL Test objects -> CBA Spring | CBA Fall
# CBA Test objects, IXL Tests can map to a CBA test
#
# Randomness - if more than 10 are perfect matches, random among the extra; random on the printed out page
# Struggling check - if they’ve failed multiple weeks in a row - “if they’ve failed 2 times in the last 2 weeks, or 3 times in the last 3 weeks”
# Skip the test on the kid’s page
# Flag it on the teacher’s page
#
#
# Teacher page - X kids need skill Y
# Work off of full set of IXL skills for each kid, not the top 10
# Iterate all kids, their sets, count up the # that need each skill, take the top X skills with more than Y kids
# Max 1+ per subdomain?
# Bubble up CBA things here too?
# Print out everything, group by subdomain
#
# Check progress later - I taught in groups these skills  - how have students progressed on them recently?
# Query most recent test results, look for pass->fail transitions
# Dump entire class for one skill
# If they passed, when did they pass?
# Color codes for passed long ago, recently passed, almost there, etc?












# Desired Outputs:
# List of IXL tests for each student (+more detail on teacher page)
# List of IXL tests that many students need + lists of those students for each test (some # of these)
# Secondary:
# Test-centric view (Text X is coming up, what do students need to work on for it)



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
