import datetime

from django.db import models

from brain.models import StudentRoster, CurrentClass
# Create your models here.


class AMCTest(models.Model):
    test_number = models.IntegerField(unique=True)
    topic = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100, unique=True)
    grade_equivalent = models.CharField(max_length=100)
    total_questions = models.IntegerField(default=20)
    minimum_passing_grade = models.IntegerField(default=18)

    def __str__(self):
        return '%s -- %s' % (self.topic, self.name)

    class Meta:
        verbose_name = "AMC Test"
        verbose_name_plural = "AMC Tests"


class AMCTestDay(models.Model):
    current_class = models.ForeignKey(CurrentClass, blank=True, null=True,)
    date_taken = models.DateField(default=datetime.datetime.now, verbose_name='Date Taken')


    def __str__(self):
        return '%s' % (self.date_taken,)
    class Meta:
        verbose_name = "AMC Test Day"
        verbose_name_plural = "AMC Test Days"


class AMCTestResult(models.Model):
    student = models.ForeignKey(StudentRoster, blank=False, null=False)
    test = models.ForeignKey(AMCTest)
    date_taken = models.ForeignKey(AMCTestDay, blank=False, null=False,)
    score = models.IntegerField(blank=False, null=False)

    def passing_score(self):
        if self.score >= self.test.minimum_passing_grade:
            return True
        elif self.score < self.test.minimum_passing_grade:
            return False
        else:
            return "Error"
    #pass_or_fail = models.BooleanField(default=passing_score())

    def __str__(self):
        return '%s -- %s Pass: %s' % (self.student, self.test, self.passing_score(), )
    class Meta:
        verbose_name = "AMC Test Score"
        verbose_name_plural = "AMC Test Scores"
        ordering = ['-date_taken', 'student']


