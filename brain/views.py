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

from .models import StudentRoster, Teacher
from amc.models import AMCTestResult
from ixl.models import IXLSkillScores
from libs.functions import nwea_recommended_skills_list, class_skills_list

from .pdf_utils import PdfPrint


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
