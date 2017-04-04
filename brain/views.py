from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
import random
from datetime import date, timedelta, datetime, timezone
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib import messages

from .models import StudentRoster, Teacher, CurrentClass, AccountInfo, MorningMessage, MorningMessageSettings, Schedule
from amc.models import AMCTestResult
from ixl.models import IXLSkillScores, IXLStats, Challenge, ChallengeAssignment, ChallengeExercise, IXLSkill
from libs.functions import nwea_recommended_skills_list, class_skills_list
from brain.models import ReadingStats
from .forms import PasswordForm
from videos.models import Video
from badges.models import Sticker, StickerAssignment, Avatar
from brain.forms import MorningMessageForm
from brain.templatetags.brain_extras import challenges_completed

GREETINGS = ['Hola', 'Hey there', 'Welcome back', 'Great to see you', "Let's do it", 'Bonjour',
             'You rock', "You've got this", "Work Hard, Get Smart", "Rock it", "Get ready to learn", "Power up",
             "Train your brain", "Push yourself today", "Learn something new", "Keep moving forward"]

COLORS = ["#51B46D", "#F9845B", "#9e4d83", "#3079AB", "#eb7728", "#E0AB18", "#c38cd4", "#20898c",
          "#39ADD1", "#53BBB4", "#2C9676", "#C25975", "#7D669E", "#F092B0", "#E15258", "#838CC7",
          "#51B46D", "#F9845B", "#9e4d83", "#3079AB", "#eb7728", "#E0AB18", "#c38cd4", "#20898c",
          "#39ADD1", "#53BBB4", "#2C9676", "#C25975", "#7D669E", "#F092B0", "#E15258", "#838CC7",
          ]
ICONS = ['fa-bolt', 'fa-bicycle', 'fa-graduation-cap', 'fa-paint-brush', 'fa-gift', 'fa-money',
         'fa-lightbulb-o', 'fa-globe', 'fa-paper-plane', 'fa-sun-o', 'fa-pencil', 'fa-paw', 'fa-moon-o',
         'fa-futbol-o', 'fa-gamepad', 'fa-dribbble', 'fa-diamond', 'fa-truck', 'fa-tree', 'fa-heart', 'fa-trophy',
         'fa-star', 'fa-car', 'fa-smile-o', 'fa-rocket', 'fa-motorcycle', 'fa-scissors', 'fa-heart',
         'fa-key', 'fa-shopping-cart', 'fa-magic', 'fa-leaf',
         'fa-space-shuttle', 'fa-cog', 'fa-flag', 'fa-check-square', ]

STYLEDICT = {
    'Spanish': ['globe', "#F092B0"
                ],
    'Art': ['paint-brush', "#F9845B"
            ],

    'Gym': ['dribbble', "#3079AB"
            ],

    'Dance': ['music', "#c38cd4"
              ],

    'Science': ['flask', "#2C9676"
                ],

    'Reading': ['book', "#39ADD1"
                ],

    'Math': ['plus', "#E15258"
             ],

    'Writing': ['pencil', "#E0AB18"
                ],

    'Core Knowledge': ['university', "#51B46D"
                       ],

    'Reading Mastery': ['comments', "#eb7728"
                        ],

}


def school_roster(request, year="16-17"):
    # url: /brain/16-17
    student_list = StudentRoster.objects.filter(
        current_class__year=year)  # .order_by('current_class__grade')#.order_by('current_class__teacher__last_name').order_by('current_class__studentroster__last_name')
    return render(request, 'brain/year_list.html', {'student_list': student_list, 'year': year, })


def grade_list(request, year="16-17", grade="2nd"):  # List of the full student roster
    # url: /brain/16-17/2nd/
    student_list = StudentRoster.objects.filter(current_class__grade=grade).filter(current_class__year=year)
    return render(request, 'brain/grade_list.html', {'student_list': student_list, 'year': year, 'grade': grade, })


def class_list(request, year="16-17", grade="2nd", teacher="Trost"):
    # url: /brain/16-17/2nd/trost
    teacher_object = Teacher.objects.get(last_name=teacher)

    current_date = date.today() - timedelta(hours=5)
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__year=year).filter(current_class__teacher__last_name=teacher)

    ## Start Reading Statistics ##
    reading_list = ReadingStats.objects.filter(student__current_class__teacher=teacher_object).order_by(
        'student__last_name')

    total_starting_lexile, total_current_lexile, total_lexile_progress, total_myon_time_spent, total_lexile_goal = 0, 0, 0, 0, 0
    for item in reading_list:
        total_starting_lexile += item.starting_lexile
        total_current_lexile += item.current_lexile
        total_lexile_progress += item.lexile_progress
        total_lexile_goal += item.goal_lexile
        total_myon_time_spent += item.myon_time_spent

    classsize = len(reading_list)
    reading_averages = [round(total_starting_lexile / classsize), round(total_current_lexile / classsize),
                        round(total_lexile_progress / classsize), round(total_lexile_goal / classsize),
                        round(total_myon_time_spent / classsize)]

    ixl_priority = IXLStats.objects.filter(student__current_class__teacher=teacher_object).order_by('time_spent')
    myon_priority = reading_list.order_by('myon_time_spent')

    ## End Reading Statistics

    ## Start IXL Challenge ##
    challenge_list = []
    for student in student_list:
        challenge = ChallengeAssignment.objects.filter(student_id=student).latest('date_assigned')
        progress = challenge.completed()
        challenge_list.append((challenge, progress))

    ## End IXL Challenge ##

    ##-------------------------START CBA GRID-----------------------##
    spring_cba_descriptions = ['Add/Sub 10,20,30',
                               'Expanded Notation',
                               'Fractions',
                               'Half of a Group',
                               'Round to Tens',
                               'Read Tables',
                               'Write Story Prob.',
                               '2-Digit minus 1-Digit',
                               '2-Digit Addition',
                               '2-Digit Subtraction',
                               'Word Prob.',
                               'Word Prob./ Get to 100',
                               'Estimate Sums',
                               'Estimate Sums Word Prob.',
                               'Clocks: 45 minutes',
                               'Coins',
                               'Draw 3 inch line',
                               'Read Bar Graph',
                               'Create Pictograph',
                               'Sort Shapes',
                               ]
    spring_cba_ixl_match = ['D-G.5',
                            'D-M.6',
                            'D-W.2',
                            None,
                            'D-N.2',
                            'D-B.6',
                            None,
                            'D-H.4',
                            'D-G.6',
                            'D-H.6',
                            'D-L.10',
                            'D-L.9',
                            'D-N.5',
                            'D-N.5',
                            'D-Q.5',
                            'D-P.4',
                            'D-S.2',
                            'D-R.2',
                            'D-R.8',
                            'D-R.12',
                            ]

    report_card_description = [
    "Uses addition and subtraction within 100 to solve word problems",
    "Adds and subtracts fluently within 20",
    "Determines whether a group of objects has an odd or even number of members",
    "Uses addition to find the total number of objects arranged in rectangular arrays",
    "Measures the length of an object",
    "Tells and writes time to the nearest 5 minutes",
     "Reads a Bar Graph",
     "Draws a Bar Graph",
     "Reads a Picture Graph",
     "Creates a Picture Graph",
     "Counts within 1000; skip counts by 5’s, 10’s and 100’s",
     "Reads and writes numbers to 1000 (words to digits)",
     "Reads and writes numbers to 1000 (digits to words)",
     "Compares two three-digits numbers",
     "Fluently adds and subtracts within 100",
     "Mentally adds 10 o 100 to/from a given number 100-900",
     "Recognizes and draws shapes with specified attributes",
    ]
    report_card_ixl_match = [
        'D-L.10',
        None,
        'D-A.9',
        'D-E.23',
        None,
        'D-Q.5',
        'D-R.2',
        'D-R.4',
        'D-R.7',
        'D-R.8',
        "D-A.4",
        'D-C.4',
        'D-C.5',
        'D-B.2',
        None,
        'D-I.2',
        'D-T.3',
    ]



    spring_cba_student_grid = []
    for student in student_list:
        studentname = "{} {}.".format(student.first_name, student.last_name[0])
        ixl_score_list = [studentname, ]
        for i in range(17): # Go through each exercise and get the score
            if report_card_ixl_match[i] != None:
                try:
                    score = IXLSkillScores.objects.get(student_id=student, ixl_skill_id__skill_id=report_card_ixl_match[i])
                    score = score.score
                except:
                    score = 0
            else:
                score = None
            ixl_score_list.append(score)# Append the score on the score list
        spring_cba_student_grid.append(ixl_score_list) #when all done, append the score list and go to next student
        # report_card_ixl_match.insert(0, "IXL:")
    #spring_cba_student_grid.append(report_card_ixl_match)

##-------------------------END CBA GRID-----------------------##




    return render(request, 'brain/class_list.html', {'student_list': student_list, 'year': year, 'grade': grade,
                                                     'teacher': teacher, 'teacher_object': teacher_object,
                                                     'reading_list': reading_list,
                                                     'challenge_list': challenge_list,
                                                     'reading_averages': reading_averages, 'ixl_priority': ixl_priority,
                                                     'myon_priority': myon_priority,
                                                     'spring_cba_student_grid': spring_cba_student_grid,
                                                     'report_card_description': report_card_description,
                                                     'report_card_ixl_match': report_card_ixl_match,

                                                     })


def student_detail(request, studentid, ):  # Look at a single student's record
    # url: /student/83
    amc_tests = AMCTestResult.objects.all().filter(student_id=studentid)[:5]
    ixl_scores = IXLSkillScores.objects.all().filter(student_id=studentid)
    student = get_object_or_404(StudentRoster, student_id=studentid)
    actual_nwea_scores, estimated_nwea_scores, recommended_skill_list, subdomain_percentage_complete = nwea_recommended_skills_list(
        student, "all")
    return render(request, 'brain/student_detail.html', {'student': student, 'amc_tests': amc_tests,
                                                         'ixl_scores': ixl_scores,
                                                         "actual_nwea_scores": actual_nwea_scores,
                                                         "estimated_nwea_scores": estimated_nwea_scores,
                                                         "recommended_skill_list": recommended_skill_list,
                                                         "subdomain_percentage_complete": subdomain_percentage_complete})


def index(request):
    return render(request, 'brain/index.html', )


def portal_school(request):  # Portal that lists all the teachers in the school
    class_list = CurrentClass.objects.filter(year="16-17").order_by('teacher', )
    school_ixl_time_spent = IXLStats.objects.all().order_by('-time_spent')[:10]
    reading_stats = ReadingStats.objects.all()
    school_myon_time_spent = reading_stats.order_by('-myon_time_spent')[:10]
    school_myon_lexile_progress = reading_stats.order_by('-lexile_progress').exclude(lexile_progress__isnull=True)[:10]

    return render(request, 'brain/portal_school.html', {'class_list': class_list, 'color_list': COLORS,
                                                        'icon_list': ICONS, 'school_ixl_time_spent':
                                                            school_ixl_time_spent,
                                                        'school_myon_time_spent': school_myon_time_spent,
                                                        'school_myon_lexile_progress': school_myon_lexile_progress, })


def portal_class(request, teacher="Trost", grade="2nd"):  # Portal that lists all the students in that class
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__year="16-17").filter(current_class__teacher__last_name=teacher).order_by('first_name')
    teacher = Teacher.objects.get(last_name=teacher)
    # Sort the student list by their number of IXL minutes spent [:5]
    class_ixl_time_spent = IXLStats.objects.filter(student__current_class__teacher=teacher).order_by('-time_spent')[:5]
    class_ixl_questions_answered = IXLStats.objects.filter(student__current_class__teacher=teacher).order_by(
        '-questions_answered')[:5]
    reading_stats = ReadingStats.objects.all()
    class_myon_time_spent = reading_stats.filter(student__current_class__teacher=teacher).order_by(
        '-myon_time_spent')
    for x in range(len(class_myon_time_spent)):
        if not class_myon_time_spent[x].myon_time_spent:
            class_myon_time_spent[x].myon_time_spent = 0
    class_myon_lexile_progress = reading_stats.filter(student__current_class__teacher=teacher).order_by(
        '-lexile_progress').exclude(lexile_progress__isnull=True)[:5]
    class_myon_time_spent = class_myon_time_spent[:5]
    # class_myon_books_read = class_myon_books_read[:5]
    leaderboardteachers = ['Trost', 'Cyphers', 'Mackinnon', 'DaSilva', "Berrie", "Stein", 'Garrett', 'Stella', ]
    myon_leaderboardteachers = ['Trost', 'Cyphers', 'Berrie', 'Mackinnon', 'Stein', "DaSilva", "Stella"]
    avatar_list = []
    if grade == "2nd":
        for student in student_list:
            try:
                current_avatar = Avatar.objects.filter(student=student).latest('date_selected')
                avatar_list.append(current_avatar.sticker.image)
            except:
                avatar_list.append('static/images/stickers/blanksticker.png')

    if teacher.last_name in leaderboardteachers:
        leaderboard_display = True
    else:
        leaderboard_display = False
    if teacher.last_name in myon_leaderboardteachers:
        myon_leaderboard_display = True
    else:
        myon_leaderboard_display = False
    return render(request, 'brain/portal_class.html', {'student_list': student_list, 'teacher': teacher, 'grade': grade,
                                                       'color_list': COLORS, 'icon_list': ICONS,
                                                       'class_ixl_time_spent': class_ixl_time_spent,
                                                       'leaderboard_display':
                                                           leaderboard_display, 'class_ixl_questions_answered':
                                                           class_ixl_questions_answered, 'class_myon_time_spent':
                                                           class_myon_time_spent,
                                                       'class_myon_lexile_progress': class_myon_lexile_progress,
                                                       'myon_leaderboard_display': myon_leaderboard_display,
                                                       'avatar_list': avatar_list

                                                       })


def portal_student(request, teacher, grade,
                   studentid):  # Portal that lists the student's information and provides links to the sites
    student = get_object_or_404(StudentRoster, student_id=studentid)
    try:
        accountinfo = AccountInfo.objects.get(student=student)
    except:
        accountinfo = False
    try:
        readingstats = ReadingStats.objects.get(student=student)
    except:
        readingstats = False
    try:
        ixlstats = IXLStats.objects.get(student=student)
        if ixlstats.last_practiced == -1:
            ixlstats = False
        elif ixlstats.last_practiced == 0:
            ixlstats.last_practiced = "Today"
        elif ixlstats.last_practiced == 1:
            ixlstats.last_practiced = "Yesterday"
        elif ixlstats.last_practiced > 1:
            ixlstats.last_practiced = "{} Days Ago".format(ixlstats.last_practiced)
    except:
        ixlstats = False

    ####---------------------IXL CHALLENGE-------------------------------####

    try:
        ixl_challenge_assignment = ChallengeAssignment.objects.filter(student_id=student).latest('date_assigned')
    except:
        ixl_challenge_assignment = False

    if ixl_challenge_assignment:  # get challenge
        challenge_exercise_list = []  # [(id, description, score), ]
        current_ixl_challenge = ixl_challenge_assignment.challenge
        exercise_list = ChallengeExercise.objects.filter(challenge=current_ixl_challenge).order_by(
            '-required_score')  # Get the related exercises
        for exercise in exercise_list:
            try:
                exercise_score = IXLSkillScores.objects.get(student_id=student,
                                                            ixl_skill_id__skill_id=exercise.exercise_id).score
            except:
                exercise_score = 0
            exercise_description = IXLSkill.objects.get(skill_id=exercise.exercise_id)
            challenge_exercise_list.append(
                (exercise.exercise_id, exercise_description, exercise_score, exercise.required_score))
            # Get scores for each challenge
    else:
        challenge_exercise_list = None
        current_ixl_challenge = None
    extra_challenge_threshold = []
    extra_skill_list = []
    if ixl_challenge_assignment:  # Find out if Challenge Complete and get Extra Skills
        extra_challenge_threshold = ['2/5', '3/5', '4/5', '5/5', 'COMPLETE']
        ixl_challenge_status = ixl_challenge_assignment.completed()
        skill_list = nwea_recommended_skills_list(student, 'recommended_skill_list')
        skill_counter = 0
        for skill in skill_list:  # Check if this skill is already being used
            used = False
            skill_id = skill[0].upper()
            for exercise in exercise_list:  # Cycle through the exercises
                if skill_id == exercise.exercise_id:
                    used = True
            if not used:
                try:
                    skill_category = IXLSkill.objects.get(skill_id=skill_id).category
                    try:
                        skill_score = IXLSkillScores.objects.get(student_id=student,
                                                                 ixl_skill_id__skill_id=skill_id).score
                    except:
                        skill_score = 0
                    extra_skill_list.append((skill_id, skill_category, skill_score))
                    skill_counter += 1
                except:
                    pass

    else:
        ixl_challenge_status = False

    ####---------------------END IXL CHALLENGE-------------------------------####
    ####---------------------GET VIDEOS-------------------------------####
    # Start a list for the videos you're getting
    video_list = []
    try:
        if accountinfo.videos:
            # Get the start and end of the current week
            dt = date.today()
            start = dt - timedelta(days=dt.weekday())
            for x in range(5):
                current_day = start + timedelta(days=x)
                videos = Video.objects.filter(lesson_date=current_day)
                current_day = current_day.strftime("%A, %B %d")
                video_list.append((current_day, videos))

    except:
        pass

    ####---------------------END GET VIDEOS-------------------------------####
    ####---------------------START LEXILE COUNTDOWN-------------------------------####
    lexile_challenge_dates = ['2017/01/26', '2017/02/09', '2017/02/23', '2017/03/09', '2017/03/23', '2017/01/26',
                              '2017/04/06', '2017/04/20', '2017/05/04', '2017/05/18', '2017/06/01', '2017/06/15', ]
    lexile_countdown = False
    for x in lexile_challenge_dates:
        scheduled_date = datetime.strptime(x, "%Y/%m/%d").day
        todays_date = datetime.today().day
        if todays_date > scheduled_date:
            continue
        else:
            lexile_countdown = abs(scheduled_date - todays_date)
            break

    ####---------------------END LEXILE COUNTDOWN-------------------------------####

    ####---------------------STICKERS-------------------------------####
    # Get Current Avatar
    try:
        current_avatar = Avatar.objects.filter(student=student).latest('date_selected')
    except:
        current_avatar = False
    # See if Avatar was set more than 6 days ago
    if current_avatar:
        if abs(datetime.now(timezone.utc) - current_avatar.date_selected) >= timedelta(days=5):
            new_avatar_choice = True
        else:
            new_avatar_choice = False
    else:
        new_avatar_choice = True

    # Get full list of Stickers in a clean order
    # Get list of stickers this student has earned
    full_sticker_list = Sticker.objects.all()
    sticker_list = []
    current_category = ''
    category_list = []
    has_earned = True
    try:
        earned_sticker_list = StickerAssignment.objects.filter(student=student, earned=True)  # Get earned stickers
        for sticker in full_sticker_list:  # Iterate through all stickers
            if sticker.category == current_category:  # If the category hasn't changed from the last sticker
                if sticker.category == "Citizenship" or sticker.category == "CGI" or sticker.category == "Assessment Awards":
                    pass
                elif not has_earned:
                    continue
            else:
                current_category = sticker.category
                sticker_list.append(['title', sticker.category])
                has_earned = True
            try:
                earned_sticker = StickerAssignment.objects.get(student=student, sticker=sticker)
                sticker_list.append([sticker.name, sticker.slug, sticker.description, sticker.image, sticker.alt_text])
            except:
                sticker_list.append(
                    [sticker.name, sticker.slug, sticker.description, 'static/images/stickers/blanksticker.png', ''])
                has_earned = False


    except:
        earned_sticker_list = []

    ####---------------------END STICKERS-------------------------------####

    second_teachers = ['Trost', 'Mackinnon', 'Cyphers', 'DaSilva']
    second_and_third_teachers = ['Berrie', 'Stein', 'DaSilva', 'Cyphers', 'Trost', 'Mackinnon']
    if teacher in second_and_third_teachers:
        myon_display = True
    else:
        myon_display = False
    try:
        if readingstats.current_lexile <= 0:
            readingstats.current_lexile = "BR"
    except:
        pass
    try:
        if readingstats.starting_lexile and readingstats.current_lexile and readingstats.goal_lexile:
            lexile_goal_percentage = round((readingstats.current_lexile - readingstats.starting_lexile) / (
                readingstats.goal_lexile - readingstats.starting_lexile) * 100)
            lexile_goal_percentage = int(lexile_goal_percentage)
        else:
            lexile_goal_percentage = 0
    except:
        lexile_goal_percentage = 0
    lexile_goal_float = str(lexile_goal_percentage) + "%"

    greeting = random.choice(GREETINGS)

    return render(request, 'brain/portal_student.html', {'student': student, 'accountinfo': accountinfo,
                                                         'teacher': teacher, 'grade': grade, 'greeting': greeting,
                                                         'readingstats': readingstats, 'ixlstats': ixlstats,
                                                         'myon_display': myon_display,
                                                         'lexile_goal_percentage': lexile_goal_percentage,
                                                         'lexile_goal_float': lexile_goal_float,
                                                         'challenge_exercise_list': challenge_exercise_list,
                                                         'current_ixl_challenge': current_ixl_challenge,
                                                         'ixl_challenge_assignment': ixl_challenge_assignment,
                                                         'second_teachers': second_teachers,
                                                         'ixl_challenge_status': ixl_challenge_status,
                                                         'video_list': video_list,
                                                         'extra_challenge_threshold': extra_challenge_threshold,
                                                         'extra_skill_list': extra_skill_list,
                                                         'earned_sticker_list': earned_sticker_list,
                                                         'sticker_list': sticker_list,
                                                         'new_avatar_choice': new_avatar_choice,
                                                         'current_avatar': current_avatar,
                                                         'lexile_countdown': lexile_countdown

                                                         })


def email_challenge_results(request):
    send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        ['to@example.com'],
        fail_silently=False,
    )


def make_groups(request, grade, teacher):
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__year="16-17").filter(current_class__teacher__last_name=teacher)
    partner_list = []
    for student in student_list:
        partner_list.append(student.first_name)
    random.shuffle(partner_list)
    final_list = []
    teacher = Teacher.objects.get(last_name=teacher)
    if len(partner_list) % 2 == 0:  # Even
        while len(partner_list) > 0:
            try:
                partnership = partner_list.pop(0) + " + " + partner_list.pop(0)
                final_list.append(partnership)
            except:
                break
    else:  # Odd
        partnership = partner_list.pop(0) + " + " + partner_list.pop(0) + " + " + partner_list.pop(0)
        final_list.append(partnership)
        while len(partner_list) > 0:
            try:
                partnership = partner_list.pop(0) + " + " + partner_list.pop(0)
                final_list.append(partnership)
            except:
                break
    return render(request, 'brain/make_groups.html',
                  {'partner_list': final_list, 'color_list': COLORS, 'teacher': teacher})


def random_student(request, grade, teacher):
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__year="16-17").filter(current_class__teacher__last_name=teacher)
    student = random.choice(student_list)
    color = random.choice(COLORS)
    return render(request, 'brain/random_student.html',
                  {'student': student, 'color_list': COLORS, 'teacher': teacher, 'color': color})


def morning_message(request, grade, teacher):
    date_object = date.today()  # Set the date to today
    try:  # See if there is a morning message for today.
        message = MorningMessage.objects.all().get(teacher__last_name=teacher, date=date_object)
    except:  # If not, just leave it as ""
        message = ""
    todays_date = date_object.strftime("%A, %B %e, %Y")  # Format the date
    try:  # Get the Morning Message settings for that teacher
        all_morning_message_settings = MorningMessageSettings.objects.get(teacher__last_name=teacher)
        if date_object.strftime("%A") == "Monday":
            specials = all_morning_message_settings.specialsmonday
            box1 = all_morning_message_settings.box1monday
        elif date_object.strftime("%A") == "Tuesday":
            specials = all_morning_message_settings.specialstuesday
            box1 = all_morning_message_settings.box1tuesday

        elif date_object.strftime("%A") == "Wednesday":
            specials = all_morning_message_settings.specialswednesday
            box1 = all_morning_message_settings.box1wednesday

        elif date_object.strftime("%A") == "Thursday":
            specials = all_morning_message_settings.specialsthursday
            box1 = all_morning_message_settings.box1thursday

        elif date_object.strftime("%A") == "Friday":
            specials = all_morning_message_settings.specialsfriday
            box1 = all_morning_message_settings.box1friday
        else:
            specials = None
            box1 = None
    except:
        specials = None
        box1 = None

    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__teacher__last_name=teacher)

    challenge_list = []
    for student in student_list:
        challenge = ChallengeAssignment.objects.filter(student_id=student).latest('date_assigned')
        progress = challenge.completed()
        challenge_list.append((challenge, progress))


    return render(request, 'brain/morning_message.html', {'teacher': teacher, 'grade': grade,
                                                          'todays_date': todays_date, 'message': message,
                                                          'specials': specials, 'box1': box1,
                                                          'all_morning_message_settings': all_morning_message_settings,
                                                          'challenge_list':challenge_list,})


def password(request, grade, teacher, studentid):
    # if this is a POST request we need to process the form data
    pass_on_file = AccountInfo.objects.get(student__student_id=studentid).myonpass
    student = StudentRoster.objects.get(student_id=studentid)
    current_class = student.current_class
    grade = current_class.grade
    teacher = current_class.teacher
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PasswordForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required

            if form.cleaned_data['password'] == pass_on_file or form.cleaned_data['password'] == 'admin':
                return HttpResponseRedirect(reverse('brain:portalstudent',
                                                    kwargs={'teacher': teacher.last_name, 'grade': grade,
                                                            'studentid': studentid, }))
            else:  # Go back to teacher page with a reverse
                # messages.add_message(request,messages.ERROR,"Password was Incorrect!")
                return HttpResponseRedirect(reverse('brain:portalclass',
                                                    kwargs={'grade': grade, 'teacher': teacher.last_name}
                                                    ))


    # if a GET (or any other method) we'll create a blank form
    else:
        form = PasswordForm()

    return render(request, 'brain/password.html', {'form': form, 'grade': grade, 'teacher': teacher,
                                                   'studentid': studentid, 'student': student, })
