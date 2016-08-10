from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404


from . import forms
from brain.models import StudentRoster, CurrentClass
from brain.templatetags import brain_extras

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
    return render(request, 'brain/class_list.html', {'student_list': student_list, 'year': year, 'grade': grade,
                                                     'teacher': teacher,})






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

    form = forms.InputAMCScores()

    if request.method == 'POST':
        print('POST')
        form = forms.InputAMCScores(request.POST)
        if form.is_valid():
            print('form is valid')
            test = form.save(commit=False)
            test.student_list = student_list
            test.save()
            messages.add_message(request, messages.SUCCESS, "American Math Challenges Recorded!")
        else:
            print('form is invalid')
            print(form.errors)
        return render(request, 'amc/input_amc_scores_form.html', {'form': form})

    context = {
        'form': form,
        'formset': formset,
        'teacher': teacher,
        'student_list': student_list,
    }
    return render(request, 'amc/input_amc_scores_form.html', context=context)



def amc_index(request):
    return HttpResponse("You're at the AMC index!")
