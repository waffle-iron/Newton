from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from .models import StudentRoster
from amc.models import AMCTestResult
from status.models import CurrentAMCTest

# TODO: Teacher List (Sort: Teacher, Incl. Most Recent Grade taught)
# TODO: Grade Roster (Sort: LastName, Incl.: First, Last, Teacher, Grade, Gender, Age)
# TODO: Class List (Sort: Lastname, Incl.: Teacher, Grade: First, Last, Gender, Age)
# TODO: Individual Student Detail (Sort: Custom, Incl.: Teacher, Grade, Gender, Age, All Test Details, Next Skills)


def school_roster(request, year="2016"):
    # url: /brain/2016
    student_list = StudentRoster.objects.filter(current_class__year=year)#.order_by('current_class__grade')#.order_by('current_class__teacher__last_name').order_by('current_class__studentroster__last_name')
    return render(request, 'brain/year_list.html', {'student_list': student_list, 'year': year, })


def grade_list(request, year="2016", grade="2nd"):  # List of the full student roster
    # url: /brain/2016/2nd/
    student_list = StudentRoster.objects.filter(current_class__grade=grade).filter(current_class__year=year)
    return render(request, 'brain/grade_list.html', {'student_list': student_list, 'year': year, 'grade': grade,})


def class_list(request, year="2016", grade="2nd", teacher="Trost"):
    # url: /brain/2016/2nd/trost
    student_list = StudentRoster.objects.filter(current_class__grade=grade)\
        .filter(current_class__year=year).filter(current_class__teacher__last_name=teacher)
    return render(request, 'brain/class_list.html', {'student_list': student_list, 'year': year, 'grade': grade,
                                                     'teacher': teacher,})


def student_detail(request, studentid,): # Look at a single student's record
    # url: /student/83
    amc_tests = AMCTestResult.objects.all().filter(student_id=studentid)[:5]
    #current_amc_test = CurrentAMCTest.objects.all().get_or_create(student__student_id=studentid)
    student = get_object_or_404(StudentRoster, student_id= studentid)
    return render(request, 'brain/student_detail.html', {'student': student, 'amc_tests': amc_tests,})


def index(request):
    return render(request, 'brain/index.html', )


def test(request):
    return HttpResponse("This is the sample page for 'test'! Good job!")


'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
'''