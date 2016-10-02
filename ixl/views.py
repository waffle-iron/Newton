import re

from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404


from ixl.models import IXLSkill, IXLSkillScores
from brain.models import StudentRoster, CurrentClass
from brain.templatetags import brain_extras


def skill_detail(request, skill_id):
    skill_id = skill_id.upper()
    skill = IXLSkill.objects.all().get(skill_id=skill_id)
    return render(request, 'ixl/skill_detail.html', {'skill': skill})


def level_detail(request, level):
    skill_list = IXLSkill.objects.all().filter(skill_id__startswith=level)
    return render(request, 'ixl/level_detail.html', {'level':level, 'skill_list': skill_list})


def class_list(request, year="16-17", grade="2nd", teacher="Trost"):
    # url: /brain/16-17/2nd/trost
    student_list = StudentRoster.objects.filter(current_class__grade=grade)\
        .filter(current_class__year=year).filter(current_class__teacher__last_name=teacher)
    return render(request, 'ixl/class_list.html', {'student_list': student_list, 'year': year, 'grade': grade,
                                                     'teacher': teacher})


def generate_recommendation_list(request, year="16-17", grade="2nd", teacher="WHOLE"):
    if teacher != "WHOLE":
        return # Create a sheet for an individual class
    else:
        pass

    # Go through the class list and get first student
    # Get recommendation files from that student, sorted by date.
    # If recommendation has been created in last 5 days, use that one and don't create a new one.
    # Otherwise, create a new one.





'''
def school_roster(request, year="16-17"):
    # url: /brain/16-17
    student_list = StudentRoster.objects.filter(current_class__year=year)#.order_by('current_class__grade')#.order_by('current_class__teacher__last_name').order_by('current_class__studentroster__last_name')
    teacher_list = CurrentClass.objects.filter(year=year)
    return render(request, 'amc/index.html', {'student_list': student_list, 'year': year, 'teacher_list':teacher_list,})




def grade_list(request, year="16-17", grade="2nd"):  # List of the full student roster
    # url: /brain/16-17/2nd/
    student_list = StudentRoster.objects.filter(current_class__grade=grade).filter(current_class__year=year)
    return render(request, 'brain/grade_list.html', {'student_list': student_list, 'year': year, 'grade': grade,})


def input_amc_scores(request, year="16-17", grade="2nd", teacher="Trost"):
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__year=year).filter(current_class__teacher__last_name=teacher)

    form_count = student_list.count()
    TestListFormSet = formset_factory(forms.InputAMCScores, extra=form_count)
    formset = TestListFormSet()
    for i in range(form_count):
        formset.forms[i].fields['student'].initial = student_list[i]
        formset.forms[i].fields['test'].initial = brain_extras.current_amc_test(student_list[i])

    if request.method == 'POST':
        print('POST')
        formset = TestListFormSet(request.POST)
        if formset.is_valid():
            print('formset is valid')
            for form in formset:
                form.save()
            messages.add_message(request, messages.SUCCESS, "American Math Challenges Recorded!")
        else:
            print('formset is invalid')
            print(formset.errors)

    context = {
        'formset': formset,
        'teacher': teacher,
        'student_list': student_list,
    }
    return render(request, 'amc/input_amc_scores_form.html', context=context)

'''