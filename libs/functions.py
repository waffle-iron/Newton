from collections import Counter

from ixl.models import IXLSkill, IXLSkillScores
from nwea.models import NWEASkill, NWEAScore, RITBand





# Find highest NWEA subdomain level that you know a student has passed (either from NWEA results or IXL),
# Have NWEA RIT Level scores for each student
# Can compute if they've passed a RIT Band from IXL
# Start with NWEA Rit band as a floor in each subdomain
# Then check IXL for the next level - have they passed? If so go to next level
#
# In the teacher report - what NWEA subdomain level they're working, and do you think they've passed the previous level because of NWEA test (w/date) or IXL.
#
# Result of this calculation =
# Student -> Set of NWEA RIT bands they should be working on (in each subdomain)
# Sort by RIT band number, return top 10
#
# Add another column for CBA with the mapping of NWEA and IXL. If the CBA column is yes (or an upcoming date) Move to top of list of ten.
#
#
# Add fields to IXL Test objects -> CBA Spring | CBA Fall
# CBA Test objects, IXL Tests can map to a CBA test
#
# Randomness - if more than 10 are perfect matches, random among the extra; random on the printed out page
# Struggling check - if they've failed multiple weeks in a row - "if they've failed 2 times in the last 2 weeks, or 3 times in the last 3 weeks"
# Skip the test on the kid's page
# Flag it on the teacher's page
#
#
# Teacher page - X kids need skill Y
# Work off of full set of IXL skills for each kid, not the top 10
# Iterate all kids, their sets, count up the # that need each skill, take the top X skills with more than Y kids
# Max 1+ per subdomain?
# Bubble up CBA things here too?
# Print out everything, group by subdomain


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








# TODO: Sort list by most occurring skills, trim at top 10 items.
# TODO: include specific students in the list, so you know who to teach.

def class_skills_list(student_list, arg):
    class_skill_list = []
    for student in student_list:
        single_skill_list = nwea_recommended_skills_list(student, "recommended_skill_list")
        for item in single_skill_list:
            class_skill_list.append(item)
    count = Counter(class_skill_list)
    class_skill_list = count.most_common()
    return class_skill_list


def nwea_recommended_skills_list(student, arg):

    '''Gets back list of next skills for student. value is a student object
    '''
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
            sub8 = recent_nwea_scores.subdomain8
            subdomain_scores = [sub1, sub2, sub3, sub4, sub5, sub6, sub7, sub8]

        else:  # Otherwise, assume student is at RIT 141 and build from there with IXL.
            subdomain_scores = [151, 151, 151, 151, 151, 151, 151, 151]
    except:
        raise IndexError

    # TODO: If student has CBA + ENI Scores get those too.
    # Else:
    # 	Assume they know nothing.


    # Get skills that match their RIT bands
    recommended_skill_list = [] # Create blank list of recommended skills for this student
    estimated_nwea_scores = []
    subdomain_percentage_complete =[]
    for x in range(0, 8):  # Iterate through the 8 subdomains, 1 at a time.
        loop = True
        additional_rit_score = 0
        while loop:
            count_of_passed_skills_in_band = 0  # Reset passed Skill counter
            current_rit_band = subdomain_scores[x] + additional_rit_score
            skills_from_current_rit_band = NWEASkill.objects.filter(rit_band__subdomain=(x+1),
                                                                    rit_band__rit_band=current_rit_band)
            number_of_skills_from_current_rit_band = skills_from_current_rit_band.count()
            for skill in skills_from_current_rit_band:
                if skill.ixl_match:  # if skill has the field ixl_match filled out, then look and see if that match has been passed
                    try:  # Try to get the student's score for this IXL Skill
                        ixl_pass = IXLSkillScores.objects.get(
                            ixl_skill_id__skill_id=skill.ixl_match, student_id__student_id=student.student_id)
                        ixl_score = ixl_pass.score
                    except:  # Else, assume score is 0
                        ixl_score = 0
                    if ixl_score >= 80:
                        count_of_passed_skills_in_band += 1
                    else:
                        dupe = False
                        if len(recommended_skill_list) > 0: # Check if the list has anything at all
                            for j in recommended_skill_list: # Pull out a tuple of 3 things
                                for i in j:
                                    if skill.ixl_match == i:
                                        dupe = True
                        if dupe == False:
                            subdomain = x
                            recommended_skill_list.append((skill.ixl_match, skill.skill, current_rit_band, subdomain))
            insufficient_skills_passed = count_of_passed_skills_in_band < number_of_skills_from_current_rit_band
            if number_of_skills_from_current_rit_band == 0 or insufficient_skills_passed:
                break
            elif count_of_passed_skills_in_band == number_of_skills_from_current_rit_band:
                additional_rit_score += 10
                continue
        estimated_nwea_scores.append(current_rit_band)
        try:  # Catches if there are no NWEA Skills in the DB.
            complete_percentage = percentage(count_of_passed_skills_in_band, number_of_skills_from_current_rit_band)
        except ZeroDivisionError:
            complete_percentage = 0
        subdomain_percentage_complete.append(str(complete_percentage))
    recommended_skill_list.sort(key=lambda tup: tup[2])
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
    answer = 100 * float(part) / float(whole)
    answer = int(round(answer))
    return answer
