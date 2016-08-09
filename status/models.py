from django.db import models

from brain.models import StudentRoster
from amc.models import AMCTestResult
# Create your models here.

# TODO: Current AMC test
# TODO: Next IXL Skills to Master
# TODO: Current NWEA Approximation
# TODO: Student Status with ENI Skills
# TODO: Student Status with IXL Skills
# TODO: Student Status with NWEA Skills
# TODO: Student Status with CBA Skills
# TODO:


class CurrentAMCTest(models.Model):
    student=models.ForeignKey(StudentRoster)
    current_amc_test = models.IntegerField(default="1")

    def find_current_amc_level(self):
        last_test_taken = AMCTestResult.objects.all().filter(student_id=self.student).order_by('-date_taken')[0]
        if last_test_taken.passing_score():
            self.current_amc_test = last_test_taken.test.test_number + 1
        if not last_test_taken.passing_score():
            self.current_amc_test = last_test_taken.test.test_number

