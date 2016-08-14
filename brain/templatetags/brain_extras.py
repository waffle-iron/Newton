from django import template

from brain.models import StudentRoster, CurrentClass, Teacher
from amc.models import AMCTestResult, AMCTest
from ixl.models import IXLSkill, IXLSkillScores
from nwea.models import NWEASkill, NWEAScore, RITBand

register = template.Library()


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


@register.simple_tag(name='nwea_recommended_skills_list')
def nwea_recommended_skills_list(student, arg):
    '''Gets back list of next skills for student. value is a student object'''
    try:
        #student = StudentRoster.objects.get() # Temporary example for development.
        if NWEAScore.objects.filter(student=student).count() > 0:  # If student has NWEA Test Scores
            recent_nwea_scores = NWEAScore.objects.all().get(
                student=student)  # .order_by(NWEAScore.test_period).first()
            sub1 = recent_nwea_scores.subdomain1
            sub2 = recent_nwea_scores.subdomain2
            sub3 = recent_nwea_scores.subdomain3
            sub4 = recent_nwea_scores.subdomain4
            sub5 = recent_nwea_scores.subdomain5
            sub6 = recent_nwea_scores.subdomain6
            sub7 = recent_nwea_scores.subdomain7
            subdomain_scores = [sub1, sub2, sub3, sub4, sub5, sub6, sub7]

        else:  # Otherwise, assume student is at RIT 141 and build from there with IXL.
            subdomain_scores = [141, 141, 141, 141, 141, 141, 141]
    except:
        raise ValueError

    # Get skills that match their RIT bands
    recommended_skill_list = [] # Create blank list of recommended skills for this student
    estimated_nwea_scores = []
    subdomain_percentage_complete =[]
    for x in range(0,7): # Iterate through the 7 subdomains, 1 at a time.
        # This is where the IXL Changes need to take place. We can't continue this loop until we find the student's
        loop = True
        additional_rit_score = 0
        while loop:
            count_of_passed_skills_in_band = 0 # Reset passed Skill counter
            current_rit_band = subdomain_scores[x]+ additional_rit_score
            skills_from_current_rit_band = NWEASkill.objects.filter(rit_band__subdomain=(x+1), rit_band__rit_band=current_rit_band)
            number_of_skills_from_current_rit_band = NWEASkill.objects.filter(rit_band__subdomain=(x+1), rit_band__rit_band=current_rit_band).count()
            for skill in skills_from_current_rit_band:
                if skill.ixl_match:  # if skill has the field ixl_match filled out, then look and see if that match has been passed
                    try:  # Try to get the student's score for this IXL Skill
                        ixl_pass = IXLSkillScores.objects.get(
                            ixl_skill_id__skill_id=skill.ixl_match, student_id__student_id=student.student_id)  # Add Student to narrow down
                        ixl_score = ixl_pass.score
                    except:  # Else, assume score is 0
                        ixl_score = 0
                    if ixl_score >= 80:
                        count_of_passed_skills_in_band += 1
                    else:
                        recommended_skill_list.append((skill.ixl_match, skill.skill))

            if count_of_passed_skills_in_band == number_of_skills_from_current_rit_band:
                additional_rit_score += 10
                continue
            elif count_of_passed_skills_in_band < number_of_skills_from_current_rit_band:
                break
        estimated_nwea_scores.append(current_rit_band)
        try: # Catches if there are no NWEA Skills in the DB.
            complete_percentage = percentage(count_of_passed_skills_in_band, number_of_skills_from_current_rit_band)
        except:
            complete_percentage = 0
        subdomain_percentage_complete.append(str(complete_percentage))

    actual_nwea_scores = subdomain_scores

    if arg == "actual_nwea_scores":
        return actual_nwea_scores
    elif arg == "estimated_nwea_scores":
        return estimated_nwea_scores
    elif arg == "recommended_skill_list" or arg == "":
        return recommended_skill_list
    elif arg == "subdomain_percentage_complete":
        return subdomain_percentage_complete
    elif arg == 'all':
        return actual_nwea_scores, estimated_nwea_scores, recommended_skill_list, subdomain_percentage_complete
    else:
        return None




def percentage(part, whole):
    return 100 * float(part) / float(whole)

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
