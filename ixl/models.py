import datetime

from django.db import models
from django.core.validators import RegexValidator

from brain.models import StudentRoster


class IXLSkill(models.Model):
    ixl_format = RegexValidator(r'^\w+\-\w+\.\d+$', 'Pattern must match IXL format: D-A.12')
    skill_id = models.CharField(max_length=7, validators=[ixl_format], blank=False,verbose_name='Skill ID')
    skill_description = models.CharField(max_length=200, blank=True, verbose_name='Skill Description')
    ixl_url = models.CharField(max_length=300, blank=True,verbose_name='IXL URL', default="")
    category = models.CharField(max_length=100, null=True)

    def __str__(self):
        return '%s - %s - %s' % (self.category, self.skill_id, self.skill_description)

    class Meta:
        verbose_name = 'IXL Skill'
        verbose_name_plural = 'IXL Skills'
        ordering = ['skill_id']


class IXLSkillScores(models.Model): # Intersection of IXLSkill and Student Roster
    student_id = models.ForeignKey(StudentRoster, on_delete=models.CASCADE,)
    ixl_skill_id = models.ForeignKey(IXLSkill, on_delete=models.CASCADE,verbose_name='IXL Skill ID',)
    date_recorded = models.DateField(default=datetime.date.today, verbose_name='Date Recorded')
    score = models.IntegerField()

    def passing_score(self):
        if self.score >= 80:
            return True
        elif self.score < 80:
            return False
        else:
            raise ValueError

    def __str__(self):
        return '%s - %s - %s' % (self.student_id, self.ixl_skill_id, self.score)

    class Meta:
        verbose_name = 'IXL Score'
        verbose_name_plural = 'IXL Scores'
        unique_together = ("student_id", "ixl_skill_id")
        ordering = ['student_id', 'ixl_skill_id']


class Challenge(models.Model): # The saved recommendation sheet to check for completion
    #student_id = models.ForeignKey(StudentRoster, on_delete=models.CASCADE,)
    title = models.CharField(max_length=250, default="Challenge", verbose_name="Challenge Title")
    date = models.DateField(default=datetime.date.today, verbose_name='Date Created')
    exercise1 = models.ForeignKey(IXLSkill,blank=True, null=True,   related_name="exercise_1")
    exercise2 = models.ForeignKey(IXLSkill,blank=True, null=True,  related_name="exercise_2")
    exercise3 = models.ForeignKey(IXLSkill,blank=True, null=True,  related_name="exercise_3")
    exercise4 = models.ForeignKey(IXLSkill,blank=True, null=True,  related_name="exercise_4")
    exercise5 = models.ForeignKey(IXLSkill,blank=True, null=True,  related_name="exercise_5")
    exercise6 = models.ForeignKey(IXLSkill,blank=True, null=True,  related_name="exercise_6")
    exercise7 = models.ForeignKey(IXLSkill,blank=True, null=True,  related_name="exercise_7")
    exercise8 = models.ForeignKey(IXLSkill,blank=True, null=True,  related_name="exercise_8")
    exercise9 = models.ForeignKey(IXLSkill,blank=True, null=True,  related_name="exercise_9")
    exercise10 = models.ForeignKey(IXLSkill,blank=True, null=True,  related_name="exercise_10")
    exercise11 = models.ForeignKey(IXLSkill,blank=True, null=True,  related_name="exercise_11")
    exercise12 = models.ForeignKey(IXLSkill,blank=True, null=True,  related_name="exercise_12")
    exercise13 = models.ForeignKey(IXLSkill,blank=True, null=True,  related_name="exercise_13")
    exercise14 = models.ForeignKey(IXLSkill,blank=True, null=True,  related_name="exercise_14")
    exercise15 = models.ForeignKey(IXLSkill,blank=True, null=True,  related_name="exercise_15")

    def __str__(self):
        return '%s' % (self.title,)

    class Meta:
        verbose_name = 'IXL Challenge'
        verbose_name_plural = 'IXL Challenges'
        ordering = ['date', 'title']

class ChallengeAssignment(models.Model):
    student_id = models.ForeignKey(StudentRoster, on_delete=models.CASCADE, )
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    date_assigned = models.DateField(default=datetime.date.today, verbose_name='Date Assigned')
    current_challenge = models.BooleanField(default=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return '%s : %s' % (self.challenge, self.student_id)

    class Meta:
        verbose_name = 'IXL Challenge Assignment'
        verbose_name_plural = 'IXL Challenge Assignmentss'
        ordering = ['date_assigned', 'challenge', 'student_id']



class IXLStats(models.Model):
    student = models.ForeignKey(StudentRoster, on_delete=models.CASCADE,)
    last_practiced = models.IntegerField(verbose_name="Last Practiced", blank=True)
    questions_answered = models.IntegerField(verbose_name="Questions Answered", blank=True)
    time_spent = models.IntegerField( verbose_name="Time Spent", blank=True)

    class Meta:
        verbose_name = 'IXL Stat'
        verbose_name_plural = 'IXL Stats'
        #unique_together = ("student", "ixl_skill_id")