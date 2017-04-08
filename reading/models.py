from django.db import models
from brain.models import StudentRoster
#
# # Create your models here.
# class ReadingStats(models.Model):
#     student = models.ForeignKey(StudentRoster, on_delete=models.CASCADE)
#     starting_lexile = models.IntegerField(blank=True, null=True, verbose_name='Starting Lexile')
#     current_lexile = models.IntegerField(blank=True, null=True, verbose_name='Current Lexile')
#     goal_lexile = models.IntegerField(blank=True, null=True, verbose_name='Goal Lexile')
#     myon_tests_taken = models.IntegerField(blank=True,null=True, verbose_name='myON Tests Taken')
#     current_dra = models.CharField(max_length=10, blank=True, verbose_name='Current DRA')
#     goal_dra = models.CharField(max_length=10, blank=True, verbose_name='Goal DRA')
#     myon_time_spent = models.IntegerField(blank=True, null=True, verbose_name="myON Time Spent")
#     myon_books_finished = models.IntegerField(blank=True, null=True, verbose_name="myON Books Finished")
#     myon_books_opened = models.IntegerField(blank=True, null=True, verbose_name="myON Books Opened")
#
#     class Meta:
#         verbose_name = "Reading Statistic"
#         verbose_name_plural = "Reading Statistics"
#
#
#
# class DRAScore(models.Model):
#     student = models.ForeignKey(StudentRoster, on_delete=models.CASCADE)
