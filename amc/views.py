from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404


from . import forms
from brain.models import StudentRoster, CurrentClass
from brain.templatetags import brain_extras
from amc.models import AMCTestResult

def school_roster(request, year="2016"):
    # url: /brain/2016
    student_list = StudentRoster.objects.filter(current_class__year=year)#.order_by('current_class__grade')#.order_by('current_class__teacher__last_name').order_by('current_class__studentroster__last_name')
    teacher_list = CurrentClass.objects.filter(year=year)
    return render(request, 'amc/index.html', {'student_list': student_list, 'year': year, 'teacher_list':teacher_list,})


def grade_list(request, year="2016", grade="2nd"):  # List of the full student roster
    # url: /brain/2016/2nd/
    student_list = StudentRoster.objects.filter(current_class__grade=grade).filter(current_class__year=year)
    return render(request, 'brain/grade_list.html', {'student_list': student_list, 'year': year, 'grade': grade,})


def class_list(request, year="2016", grade="2nd", teacher="Trost"):
    # url: /brain/2016/2nd/trost
    student_list = StudentRoster.objects.filter(current_class__grade=grade)\
        .filter(current_class__year=year).filter(current_class__teacher__last_name=teacher)
    amc_tests = AMCTestResult.objects.all()

    return render(request, 'amc/class_list.html', {'student_list': student_list, 'year': year, 'grade': grade,
                                                     'teacher': teacher, 'amc_tests':amc_tests})






# TODO: Writing form to db
# TODO: Handling absent/blank student scores

@login_required
def input_amc_scores(request, year="2016", grade="2nd", teacher="Trost"):
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



def amc_index(request):
    return HttpResponse("You're at the AMC index!")
