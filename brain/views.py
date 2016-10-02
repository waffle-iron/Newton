from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, inch, portrait
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from datetime import date
import random

from .models import StudentRoster, Teacher, CurrentClass, AccountInfo
from amc.models import AMCTestResult
from ixl.models import IXLSkillScores
from libs.functions import nwea_recommended_skills_list, class_skills_list

from .pdf_utils import PdfPrint

GREETINGS = ['Hello', 'Hola', 'Hey there', 'Welcome back', 'Great to see you', "Let's do it", 'Bonjour', 'Guten tag',
             'You rock', "You've got this", "Work hard, get smart", "Rock it"]

def inches_to_points(inches):
    return inches * 72


def create_ixl_pdf(request):
    if 'pdf' in request.POST:
                student = StudentRoster.objects.get(last_name="Boyd")
                response = HttpResponse(content_type='application/pdf') # Tell the client the response will be an attachment
                today = date.today() # Set today's date
                filename = 'ixl_list' + today.strftime('%Y-%m-%d') # Set the filename
                response['Content-Disposition'] = 'attachment; filename={0}.pdf'.format(filename)
                buffer = BytesIO() # Create BytesIO instance as a temporary file
                report = PdfPrint(buffer, 'Letter') # Creates an instance of PDFPrint in report.
                pdf = report.recommendation_list(student, 'Recommendation List for {} {}'.format(student.first_name, student.last_name[0])) # args=Weather History/Title
                response.write(pdf) # Adds the PDF contents to the response
                return response # Returns the response.



# TODO: Teacher List (Sort: Teacher, Incl. Most Recent Grade taught)
# TODO: Grade Roster (Sort: LastName, Incl.: First, Last, Teacher, Grade, Gender, Age)
# TODO: Class List (Sort: Lastname, Incl.: Teacher, Grade: First, Last, Gender, Age)
# TODO: Individual Student Detail (Sort: Custom, Incl.: Teacher, Grade, Gender, Age, All Test Details, Next Skills)


def school_roster(request, year="16-17"):
    # url: /brain/16-17
    student_list = StudentRoster.objects.filter(
        current_class__year=year)  # .order_by('current_class__grade')#.order_by('current_class__teacher__last_name').order_by('current_class__studentroster__last_name')
    return render(request, 'brain/year_list.html', {'student_list': student_list, 'year': year,})


def grade_list(request, year="16-17", grade="2nd"):  # List of the full student roster
    # url: /brain/16-17/2nd/
    student_list = StudentRoster.objects.filter(current_class__grade=grade).filter(current_class__year=year)
    return render(request, 'brain/grade_list.html', {'student_list': student_list, 'year': year, 'grade': grade,})


def class_list(request, year="16-17", grade="2nd", teacher="Trost"):
    # url: /brain/16-17/2nd/trost
    teacher_object = Teacher.objects.get(last_name=teacher)
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__year=year).filter(current_class__teacher__last_name=teacher)
    recommendation_list = class_skills_list(student_list, "recommended_skill_list")[:10]
    return render(request, 'brain/class_list.html', {'student_list': student_list, 'year': year, 'grade': grade,
                                                     'teacher': teacher,'teacher_object':teacher_object,
                                                     'recommendation_list': recommendation_list,})


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

def portal_school(request): # Portal that lists all the teachers in the school
    class_list = CurrentClass.objects.filter(year="16-17").order_by('teacher',)
    color_list = ["#2c9676", "#3079AB",  "#c25975", "#9e4d83", "#e15258", "#53BBB4", "#5cb860", "#7D669E",
                  "#F9845B", "#f092b0", "#2c9676", "#3079AB", "#9e4d83", "#c25975", "#9e4d83", "#e15258", "#53BBB4", "#5cb860", "#7D669E",
                  "#F9845B", "#f092b0", "#2c9676", "#3079AB", "#9e4d83", "#c25975", "#9e4d83", "#e15258", "#53BBB4", "#5cb860", "#7D669E",
                  "#F9845B", "#f092b0", "#2c9676", "#3079AB", "#9e4d83", "#c25975", "#9e4d83", "#e15258", "#53BBB4", "#5cb860", "#7D669E",
                  "#F9845B", "#f092b0", ]
    icon_list = ['fa-heart','fa-globe','fa-rocket','fa-car', 'fa-bolt',  'fa-paw','fa-graduation-cap',
                 'fa-bicycle','fa-paint-brush', 'fa-leaf','fa-money',
                 'fa-key', 'fa-lightbulb-o',  'fa-paper-plane', 'fa-pencil', 'fa-moon-o',
                 'fa-futbol-o', 'fa-gamepad', 'fa-dribbble', 'fa-diamond', 'fa-truck', 'fa-tree', 'fa-heart', 'fa-trophy',
                 'fa-star', 'fa-smile-o',  'fa-motorcycle',  'fa-check-square', 'fa-scissors',
                 'fa-apple', 'fa-cloud', 'fa-sun-o', 'fa-shopping-cart', 'fa-magic',
                 'fa-space-shuttle', 'fa-gift', 'fa-cog', 'fa-flag']
    return render(request, 'brain/portal_school.html', {'class_list': class_list, 'color_list':color_list,
                                                        'icon_list':icon_list})

def portal_class(request, teacher="Trost", grade="2nd"): # Portal that lists all the students in that class
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__year="16-17").filter(current_class__teacher__last_name=teacher).order_by('first_name')
    teacher = Teacher.objects.get(last_name=teacher)
    color_list = ["#2c9676", "#3079AB",  "#c25975", "#9e4d83", "#e15258", "#53BBB4", "#5cb860", "#7D669E",
                  "#F9845B", "#f092b0", "#2c9676", "#3079AB", "#9e4d83", "#c25975", "#9e4d83", "#e15258", "#53BBB4", "#5cb860", "#7D669E",
                  "#F9845B", "#f092b0", "#2c9676", "#3079AB", "#9e4d83", "#c25975", "#9e4d83", "#e15258", "#53BBB4", "#5cb860", "#7D669E",
                  "#F9845B", "#f092b0", "#2c9676", "#3079AB", "#9e4d83", "#c25975", "#9e4d83", "#e15258", "#53BBB4", "#5cb860", "#7D669E",
                  "#F9845B", "#f092b0", ]
    icon_list = ['fa-car', 'fa-bolt', 'fa-graduation-cap', 'fa-bicycle','fa-paint-brush', 'fa-leaf','fa-money',
                 'fa-key', 'fa-lightbulb-o', 'fa-globe', 'fa-paper-plane', 'fa-pencil', 'fa-paw', 'fa-moon-o',
                 'fa-futbol-o', 'fa-gamepad', 'fa-dribbble', 'fa-diamond', 'fa-truck', 'fa-tree', 'fa-heart', 'fa-trophy',
                 'fa-star', 'fa-smile-o', 'fa-rocket', 'fa-motorcycle',  'fa-check-square', 'fa-scissors',
                 'fa-apple',  'fa-cloud', 'fa-sun-o', 'fa-shopping-cart', 'fa-magic',
                 'fa-space-shuttle', 'fa-gift', 'fa-cog', 'fa-flag', 'fa-heart',]

    return render(request, 'brain/portal_class.html', {'student_list': student_list, 'teacher':teacher, 'grade':grade,  'color_list':color_list, 'icon_list':icon_list})

def portal_student(request, teacher, grade, studentid): # Portal that lists the student's information and provides links to the sites
    student = get_object_or_404(StudentRoster, student_id=studentid)
    try:
        accountinfo = get_object_or_404(AccountInfo, student=student)
    except:
        accountinfo = False
    greeting = random.choice(GREETINGS)
    return render(request, 'brain/portal_student.html', {'student': student, 'accountinfo': accountinfo,
                                                         'teacher': teacher, 'grade': grade , 'greeting': greeting,})

