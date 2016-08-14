#! scripts/recommended_skills_list.py

# Full path to your django project directory
your_djangoproject_home="/Users/alexandertrost/PycharmProjects/newton/"
import django
import sys,os

sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")
django.setup()
from nwea.models import NWEASkill, NWEAScore, RITBand
from brain.models import StudentRoster, CurrentClass, Teacher
from ixl.models import IXLSkillScores


# TODO: Filter NWEA Scores by most recent

def recommended_skills_list(student): # Main Function
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
                        # ixl_pass = IXLSkillScores.objects.get(student_id__student_id=student.student_id)
                        ixl_pass = IXLSkillScores.objects.get(
                            ixl_skill_id__skill_id=skill.ixl_match, student_id__student_id=student.student_id)  # Add Student to narrow down
                        ixl_score = ixl_pass.score
                    except:  # Else, assume score is 0
                        ixl_score = 0
                    # IF ixl score is > 80, nullify this skill and continue.
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
        #print("Percent of SubDomain "+ str(x+1) + " RIT band "+str(current_rit_band)+ " complete: "+ str(complete_percentage))
        subdomain_percentage_complete.append(str(complete_percentage))

    #print("Actual NWEA Scores for {}: {}".format(student, subdomain_scores))
    #print("Estimated NWEA Scores for {}: {}".format(student, estimated_nwea_scores))

    actual_nwea_scores = subdomain_scores

    return actual_nwea_scores, estimated_nwea_scores, recommended_skill_list, subdomain_percentage_complete


def percentage(part, whole):
  return 100 * float(part)/float(whole)

def get_nwea_scores(student):
    if NWEAScore.objects.filter(student=student).count() > 0: # If student has NWEA Test Scores
        recent_nwea_scores = NWEAScore.objects.all().get(student=student)#.order_by(NWEAScore.test_period).first()
        sub1 = recent_nwea_scores.subdomain1
        sub2 = recent_nwea_scores.subdomain2
        sub3 = recent_nwea_scores.subdomain3
        sub4 = recent_nwea_scores.subdomain4
        sub5 = recent_nwea_scores.subdomain5
        sub6 = recent_nwea_scores.subdomain6
        sub7 = recent_nwea_scores.subdomain7
        subdomain_scores = [sub1, sub2, sub3, sub4, sub5, sub6, sub7]

    else: #Otherwise, assume student is at RIT 141 and build from there with IXL.
        subdomain_scores = [141, 141, 141, 141, 141, 141, 141]
    return subdomain_scores






#Run Program
#student = StudentRoster.objects.get(last_name="Boyd")

#recommended_skills_list(student)




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
