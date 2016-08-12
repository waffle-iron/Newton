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
    date_recorded = models.DateField(default=datetime.datetime.now, verbose_name='Date Recorded')
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
