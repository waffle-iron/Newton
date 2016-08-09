from django.shortcuts import render, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404


from . import forms
from brain.models import StudentRoster

# Create your views here.

@login_required
def input_amc_scores(request, year="2016", grade="2nd", teacher="Trost"):
    form = forms.InputAMCScores()
    student_list = StudentRoster.objects.filter(current_class__grade=grade) \
        .filter(current_class__year=year).filter(current_class__teacher__last_name=teacher)

    if request.method == 'POST':
        form= forms.InputAMCScores(request.POST)
        if form.is_valid():
            test = form.save(commit=False)
            test.student_list = student_list
            test.save()
            messages.add_message(request, messages.SUCCESS, "American Math Challenges Recorded! Great going!")
        return render(request, 'amc/input_amc_scores_form.html', {'form':form,})


    return render(request, 'amc/input_amc_scores_form.html', {'form': form, 'teacher':teacher, 'student_list':student_list,})


def amc_index(request):
    return HttpResponse("You're at the AMC index!")