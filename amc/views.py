import datetime

from django.core.urlresolvers import reverse
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


def school_roster(request, year="16-17"):
    # url: /brain/16-17
    student_list = StudentRoster.objects.filter(current_class__year=year)#.order_by('current_class__grade')#.order_by('current_class__teacher__last_name').order_by('current_class__studentroster__last_name')
    teacher_list = CurrentClass.objects.filter(year=year)
    return render(request, 'amc/index.html', {'student_list': student_list, 'year': year, 'teacher_list':teacher_list,})


def grade_list(request, year="16-17", grade="2nd"):  # List of the full student roster
    # url: /brain/16-17/2nd/
    student_list = StudentRoster.objects.filter(current_class__grade=grade).filter(current_class__year=year)
    return render(request, 'brain/grade_list.html', {'student_list': student_list, 'year': year, 'grade': grade,})


def class_list(request, year="16-17", grade="2nd", teacher="Trost"):
    # url: /brain/16-17/2nd/trost
    student_list = StudentRoster.objects.filter(current_class__grade=grade)\
        .filter(current_class__year=year).filter(current_class__teacher__last_name=teacher)
    amc_tests = AMCTestResult.objects.all()

    return render(request, 'amc/class_list.html', {'student_list': student_list, 'year': year, 'grade': grade,
                                                     'teacher': teacher, 'amc_tests':amc_tests})







@login_required
def input_amc_scores(request, year="16-17", grade="2nd", teacher="Trost"):
    if request.method == 'POST':
        TestListFormSet = formset_factory(forms.InputAMCScores, extra=0)
        formset = TestListFormSet(request.POST)
        has_errors = False
        for form in formset:
            # Seems like it should be possible to have the form know the instance it was created from, and update
            # that rather than go through this manual process
            if form.is_valid():
                form.save()
            else:
                existing_results = AMCTestResult.objects.filter(student=form.instance.student,
                                                                date_tested=form.instance.date_tested)
                if form.instance.score and existing_results.count():
                    instance = existing_results.first()
                    instance.score = form.instance.score
                    instance.save()
                else:
                    has_errors = True
                    print(form.errors)
        messages.add_message(request, messages.SUCCESS, "American Math Challenges Recorded!")
        if not has_errors:
            url = reverse('amc:classlist', kwargs={'year': year, 'grade': grade, 'teacher': teacher})
            return HttpResponseRedirect(url)
    else:
        student_list = StudentRoster.objects.filter(current_class__grade=grade) \
            .filter(current_class__year=year).filter(current_class__teacher__last_name=teacher)

        form_count = student_list.count()
        TestListFormSet = formset_factory(forms.InputAMCScores, extra=form_count)
        formset = TestListFormSet()
        # Would be nice to create forms from the instances rather than manually set initial, but that did not seem
        # to work correctly
        for i in range(form_count):
            today = datetime.date.today()
            existing_results = AMCTestResult.objects.filter(student=student_list[i], date_tested=today)
            initial_test = brain_extras.current_amc_test(student_list[i])
            if existing_results.count():
                instance = existing_results.first()
                formset.forms[i].instance = instance
                initial_student = instance.student
                initial_score = instance.score
            else:
                initial_student = student_list[i]
                initial_score = None
            formset.forms[i].fields['student'].initial = initial_student
            formset.forms[i].fields['test'].initial = initial_test
            formset.forms[i].fields['score'].initial = initial_score

    context = {
        'formset': formset,
        'teacher': teacher,
        'grade':grade,
        'year':year,
    }
    return render(request, 'amc/input_amc_scores_form.html', context=context)


def amc_index(request):
    return HttpResponse("You're at the AMC index!")
