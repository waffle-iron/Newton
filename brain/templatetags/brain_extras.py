from django import template

from brain.models import StudentRoster, CurrentClass, Teacher


register = template.Library()


@register.simple_tag
def current_amc_test():
    #Gets the current AMC test for a student#
    pass


@register.inclusion_tag('brain/classes_nav.html')
def nav_teachers_list():
    teachers = Teacher.objects.all()
    return {'teachers': teachers}

#@register.inclusion_tag('brain/students')