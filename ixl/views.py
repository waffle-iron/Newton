from django.shortcuts import render

from .models import IXLSkill, IXLSkillScores


# Create your views here.

def ixl_skill_detail(request, ixlskill_id):
    response = "You're looking at IXL Skill %s."
    return HttpResponse(response % ixlskill_id)


def ixl_skill_scores(request, ixlskillscores_id):
    return HttpResponse("You're looking at IXL score %s." % ixlskillscores_id)
