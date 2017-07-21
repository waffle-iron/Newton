from django.db import models
from django.core.validators import RegexValidator
from variables import GRADE_CHOICES, SECOND
from brain.models import StudentRoster, SchoolDay


# Create your models here.

class CommonCoreStateStandard(models.Model):

    ccss_format = RegexValidator(r'^CCSS\.(.*)$', 'Pattern must match IXL format: D-A.12')
    grade = models.CharField(max_length=50, choices=GRADE_CHOICES, default=SECOND)
    domain = models.CharField(max_length=50, null=False, blank=False, default="Reading")
    subdomain = models.CharField(max_length=100, blank=True, )
    topic = models.CharField(max_length=100, null=False, blank=False, default="Key Ideas and Details") # Bolded on CCSS
    code = models.CharField(max_length=100, validators=[ccss_format], blank=False, verbose_name="CCSS Code") # CCSS.ELA-LITERACY.RI.2.1
    description = models.CharField(max_length=1000,) # The standard's text.


    class Meta:
        verbose_name = 'Common Core Standard'
        verbose_name_plural = 'Common Core Standards'

    def __str__(self):
        return "{} {} - {}: {}".format(self.domain, self.subdomain, self.topic, self.code)



class HomeworkCompletion(models.Model): # Keeps data on whether or not a student handed in homework
    STATUS_CHOICES = (("COMPLETE", "Complete"),("INCOMPLETE","Incomplete"), ("NOT RECEIVED","Not Received"), ("LATE","Late"))
    student = models.ForeignKey(StudentRoster, on_delete=models.CASCADE, verbose_name="Student")
    school_day = models.ForeignKey(SchoolDay, on_delete=models.CASCADE, verbose_name="Date")
    status = models.CharField(choices=STATUS_CHOICES, max_length=50, default="NOT RECEIVED", verbose_name="Status")

    class Meta:
        ordering = ['school_day']
        verbose_name = 'Homework Status'
        verbose_name_plural = 'Homework Statuses'

    def __str__(self):
        return "{}'s Homework on {} is {}".format(self.student, self.school_day, self.status)