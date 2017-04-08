from django.shortcuts import render
from brain.models import StudentRoster, CurrentClass, Teacher, Schedule, Subject
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Score, TeacherApproval
from .forms import ScoreForm
import datetime
from django.utils.timezone import now, timedelta
from brain.templatetags.brain_extras import add_total_score

# Create your views here.
SUBJECTDICT = {
    'Spanish': ["I raised my hand to speak", "I was in SLANT the whole time", "I transitioned well",
                "I always said please and thank you", "I followed teacher instructions the first time",
                "I respected the materials and used them appropriately", "I was respectful to my peers",
                ],
    'Art': ["I raised my hand to speak", "I was in SLANT the whole time", "I transitioned well",
            "I always said please and thank you", "I followed teacher instructions the first time",
            "I respected the materials and used them appropriately", "I was respectful to my peers",
            ],
    'Gym': ["I raised my hand to speak", "I was in SLANT the whole time", "I transitioned well",
            "I always said please and thank you", "I followed teacher instructions the first time",
            "I respected the gym materials and used them appropriately", "I was respectful to my peers",
            ],

    'Dance': ["I raised my hand to speak", "I stayed in my spot and tracked the teacher", "I transitioned well",
              "I always said please and thank you", "I followed teacher instructions the first time",
              "I respected the materials and dance studio", "I was respectful to my peers",
              ],

    'Science': ["I raised my hand to speak", "I was in SLANT the whole time", "I transitioned well",
                "I always said please and thank you", "I followed teacher instructions the first time",
                "I respected the materials and used them appropriately", "I was respectful to my peers",
                ],

    'Reading': ["I raised my hand to speak", "I was in SLANT the whole time", "I transitioned well",
                "I always said please and thank you", "I followed teacher instructions the first time",
                "I respected the materials and used them appropriately", "I was respectful to my peers",
                ],
    'Math': ["I raised my hand to speak", "I was in SLANT the whole time", "I transitioned well",
             "I always said please and thank you", "I followed teacher instructions the first time",
             "I respected the math materials and used them appropriately", "I was respectful to my peers",
             ],

    'Writing': ["I raised my hand to speak", "I was in SLANT the whole time", "I transitioned well",
                "I always said please and thank you", "I followed teacher instructions the first time",
                "I respected the materials and used them appropriately", "I was respectful to my peers",
                ],

    'Core Knowledge': ["I raised my hand to speak", "I was in SLANT the whole time", "I transitioned well",
                       "I always said please and thank you", "I followed teacher instructions the first time",
                       "I respected the materials and used them appropriately", "I was respectful to my peers",
                       ],
    'Reading Mastery': ["I raised my hand to speak", "I was in SLANT the whole time", "I transitioned well",
                        "I always said please and thank you", "I followed teacher instructions the first time",
                        "I respected the materials and used them appropriately", "I was respectful to my peers",
                        ],

}
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


# TODO: Add Individual Colors and icons to Subject buttons



def class_list(request, student_id):
    # Get the Day
    date_object = datetime.date.today()
    day = date_object.strftime("%A")
    # Get student
    student = StudentRoster.objects.get(student_id=student_id)
    # Get student's teacher
    teacher = student.current_class.teacher
    # Get student's teacher's schedule for this day
    grade = student.current_class.grade
    try:
        schedule = Schedule.objects.get(teacher=teacher, day=day.upper())
    except:
        schedule = Schedule.objects.get(teacher=teacher, day="MONDAY")
    # Get list of all classes on this day in order
    classes = [schedule.subject1, schedule.subject2, schedule.subject3, schedule.subject4, schedule.subject5,
               schedule.subject6, schedule.subject7]
    classesandstyles = []
    for item in classes:  # Item = reading or writing
        # Find out if there is a score for the subject yet, and if so, put the score. Otherwise return None.
        icon, color = STYLEDICT[item.title]
        classesandstyles.append((item, icon, color))

    return render(request, 'scoreit/class_list.html', {'classesandstyles': classesandstyles, 'student': student,
                                                       'teacher': teacher, 'day': day, 'schedule': schedule,

                                                       'grade': grade, 'date': date_object,
                                                       })


def log_subject(request, student_id, subject):
    '''For this I need to have the different criteria in order for that subject. At the top it will say "CHANZE'S SPANISH SCORE IT"
    and it'll have the criteria with yes/no going down, with a submit button at the bottom. If they have already submitted the form
    it will be the same scores from before. If this is the first time, they will get a blank form where they have to click yes/no
    When they hit submit, it either creates or updates the form. '''
    # Get the Day
    date_object = now()
    day = date_object.strftime("%A")
    # Get student
    student = StudentRoster.objects.get(student_id=student_id)
    subjectobj = Subject.objects.get(title=subject)
    descriptions = SUBJECTDICT[subject]
    obj, created = Score.objects.get_or_create(student=student, date=date_object, subject=subjectobj)

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ScoreForm(request.POST, instance=obj)
        score = form.save(commit=False)
        score.subject = subjectobj
        score.student = student
        score.date = date_object
        score.save()
        messages.add_message(request, messages.SUCCESS,
                             "{} score saved!".format(subject))
        return HttpResponseRedirect(score.get_absolute_url())

    # if a GET (or any other method) we'll create a blank form
    else:
        # Check to see if the student/subject/date object already exists. If so, get that data. Otherwise new form
        form = ScoreForm(instance=obj)

    return render(request, 'scoreit/log_subject.html', {
        'student_id': student_id, 'student': student,
        'subject': subject, 'form': form, 'descriptions': descriptions
    })


def grade_view(request):
    teacher_list = ["Trost", "Cyphers", "Mackinnon"]
    date_object = now() - timedelta(hours=5)
    day_of_week = date_object.strftime("%A")
    weekend = ['SATURDAY', 'SUNDAY']
    if day_of_week.upper() in weekend:
        day_of_week = "Friday"
    teacher_student_list = []
    for teacher in teacher_list:
        teacherobj = Teacher.objects.get(last_name=teacher)
        schedule = Schedule.objects.get(teacher=teacherobj, day=day_of_week.upper())

        classes = [schedule.subject1, schedule.subject2, schedule.subject3, schedule.subject4, schedule.subject5,
                   schedule.subject6, schedule.subject7]
        student_list = StudentRoster.objects.filter(current_class__teacher__last_name=teacher).order_by('first_name')
        teacher_student_list.append((teacher,student_list, classes))

    return render(request, 'scoreit/grade_view.html', {
        'teacher_student_list':teacher_student_list, 'date':date_object,
    })

def grade_view_yesterday(request):
    teacher_list = ["Trost", "Cyphers", "Mackinnon"]
    date_object = now() - timedelta(days=1) - timedelta(hours=5)
    day_of_week = date_object.strftime("%A")
    teacher_student_list = []
    for teacher in teacher_list:
        teacherobj = Teacher.objects.get(last_name=teacher)
        schedule = Schedule.objects.get(teacher=teacherobj, day=day_of_week.upper())

        classes = [schedule.subject1, schedule.subject2, schedule.subject3, schedule.subject4, schedule.subject5,
                   schedule.subject6, schedule.subject7]
        student_list = StudentRoster.objects.filter(current_class__teacher__last_name=teacher).order_by('first_name')
        teacher_student_list.append((teacher,student_list, classes))

    return render(request, 'scoreit/grade_view.html', {
        'teacher_student_list':teacher_student_list, 'date':date_object,
    })

def grade_view_twodays(request):
    teacher_list = ["Trost", "Cyphers", "Mackinnon"]
    date_object = now() - timedelta(days=2) - timedelta(hours=5)
    day_of_week = date_object.strftime("%A")
    teacher_student_list = []
    for teacher in teacher_list:
        teacherobj = Teacher.objects.get(last_name=teacher)
        schedule = Schedule.objects.get(teacher=teacherobj, day=day_of_week.upper())

        classes = [schedule.subject1, schedule.subject2, schedule.subject3, schedule.subject4, schedule.subject5,
                   schedule.subject6, schedule.subject7]
        student_list = StudentRoster.objects.filter(current_class__teacher__last_name=teacher).order_by('first_name')
        teacher_student_list.append((teacher,student_list, classes))

    return render(request, 'scoreit/grade_view.html', {
        'teacher_student_list':teacher_student_list, 'date':date_object,
    })
def grade_view_threedays(request):
    teacher_list = ["Trost", "Cyphers", "Mackinnon"]
    date_object = now() - timedelta(days=3) - timedelta(hours=5)
    day_of_week = date_object.strftime("%A")
    teacher_student_list = []
    for teacher in teacher_list:
        teacherobj = Teacher.objects.get(last_name=teacher)
        schedule = Schedule.objects.get(teacher=teacherobj, day=day_of_week.upper())

        classes = [schedule.subject1, schedule.subject2, schedule.subject3, schedule.subject4, schedule.subject5,
                   schedule.subject6, schedule.subject7]
        student_list = StudentRoster.objects.filter(current_class__teacher__last_name=teacher).order_by('first_name')
        teacher_student_list.append((teacher,student_list, classes))

    return render(request, 'scoreit/grade_view.html', {
        'teacher_student_list':teacher_student_list, 'date':date_object,
    })