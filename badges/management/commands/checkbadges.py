your_djangoproject_home="/home/alex/newton/"
import django
from datetime import date
import sys,os
from os import listdir
import re

sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")

django.setup()
import random
from django.core.management.base import BaseCommand, CommandError

from brain.models import StudentRoster, ReadingStats, CurrentClass
from ixl.models import IXLSkillScores, IXLStats, ChallengeAssignment
from badges.models import StickerAssignment, Sticker
from mathcgi.models import CGIResult


BOOKS_READ = [(50, 'read-50-books'), (100, 'read-100-books'), (200, 'read-200-books'), (300, 'read-300-books'),
              (400, 'read-400-books'), (500, 'read-500-books'), ]

MYON_TIME = [(200, 'read-200-minutes'), (400, 'read-400-minutes'), (600, 'read-600-minutes'),
             (800, 'read-800-minutes'), (1000, 'read-1000-minutes'), (2000, 'read-2000-minutes'),
             (3000, 'read-3000-minutes'), (4000, 'read-4000-minutes'), (5000, 'read-5000-minutes'),
             ]

MYON_GROWTH = [
    (10, 'grow-10-lexile'), (20, 'grow-20-lexile'), (30, 'grow-30-lexile'), (40, 'grow-40-lexile'),
    (50, 'grow-50-lexile'),
    (75, 'grow-75-lexile'), (100, 'grow-100-lexile'), (150, 'grow-150-lexile'), (200, 'grow-200-lexile'),
    (250, 'grow-250-lexile'), (300, 'grow-300-lexile'), (350, 'grow-350-lexile'), (400, 'grow-400-lexile'),
    ]

LEXILE_LEVEL = [
    (100, 'lexile-100'), (200, 'lexile-200'), (300, 'lexile-300'), (400, 'lexile-400'), (500, 'lexile-500'),
    (600, 'lexile-600'), (700, 'lexile-700'), (800, 'lexile-800'),
    ]

IXL_CHALLENGES = [
    (1, '1-ixl-challenges'), (2, '2-ixl-challenges'), (3, '3-ixl-challenges'), (4, '4-ixl-challenges'),
    (5, '5-ixl-challenges'), (10, '10-ixl-challenges'), (15, '15-ixl-challenges'), (20, '20-ixl-challenges'),
    (25, '25-ixl-challenges'), (30, '30-ixl-challenges'),
    ]

IXL_TIME = [(200, 'ixl-200-minutes'), (400, 'ixl-400-minutes'), (600, 'ixl-600-minutes'), (800, 'ixl-800-minutes'),
            (1000, 'ixl-1000-minutes'), (1200, 'ixl-1200-minutes'), (1400, 'ixl-1400-minutes'),
            (1600, 'ixl-1600-minutes'), (1800, 'ixl-1800-minutes'), (2000, 'ixl-2000-minutes'),
            ]

# This one is different, because I can pass cgi 5 without passing cgi 4
CGI_PASSED = {1: 'cgi-1-passed', 2: 'cgi-2-passed', 3: 'cgi-3-passed', 4: 'cgi-4-passed', 5: 'cgi-5-passed',
              6: 'cgi-6-passed', 7: 'cgi-7-passed', 8: 'cgi-8-passed', 9: 'cgi-9-passed',
              10: 'cgi-10-passed', 11: 'cgi-11-passed', 12: 'cgi-12-passed', 13: 'cgi-13-passed',
              14: 'cgi-14-passed', 15: 'cgi-all-passed',
              }


class Command(BaseCommand):
    help = 'Makes sticker objects for achievements'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass

    def handle(self, *args, **options):
        checkbadges("2nd")



def checkbadges(grade):
    # Get student_list
    student_list = StudentRoster.objects.filter(current_class__grade=grade)
    for student in student_list:
        reading_stats = ReadingStats.objects.get(student=student)
        ixl_stats = IXLStats.objects.get(student=student)
        cgiresults = CGIResult.objects.filter(student=student)
        completed_challenges = 0
        ixl_challenges = ChallengeAssignment.objects.filter(student_id=student)
        for challenge in ixl_challenges:
            complete = challenge.completed()
            #print("Challenge {} is {}".format(challenge,complete))
            if complete == "COMPLETE":
                completed_challenges += 1
                #print("Completed Challenges = {}".format(completed_challenges))

        for benchmark in MYON_GROWTH:
            if reading_stats.lexile_progress >= benchmark[0]:
                sticker = Sticker.objects.get(slug=benchmark[1])
                obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
            else:
                break

        for benchmark in MYON_TIME:
            if reading_stats.myon_time_spent >= benchmark[0]:
                sticker = Sticker.objects.get(slug=benchmark[1])
                obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
            else:
                break

        for benchmark in BOOKS_READ:
            if reading_stats.myon_books_finished >= benchmark[0]:
                sticker = Sticker.objects.get(slug=benchmark[1])
                obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
            else:
                break

        for benchmark in IXL_TIME:
            if ixl_stats.time_spent >= benchmark[0]:
                sticker = Sticker.objects.get(slug=benchmark[1])
                obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
            else:
                break

        for benchmark in LEXILE_LEVEL:
            if reading_stats.current_lexile >= benchmark[0]:
                sticker = Sticker.objects.get(slug=benchmark[1])
                obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
            else:
                break

        for benchmark in IXL_CHALLENGES:
            if completed_challenges >= benchmark[0]:
                #print("For {} Completed Challenges ( {} ) is more than the Benchmark {}".format(student.first_name, completed_challenges, benchmark[0]))
                sticker = Sticker.objects.get(slug=benchmark[1])
                obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)
            else:
                break

        if len(cgiresults)==13:
            all_finished = True
            for result in cgiresults:
                if result.progress == '3' or result.progress =='M':
                    pass
                else:
                    all_finished = False
            if all_finished:
                sticker = Sticker.objects.get(slug='cgi-all-passed')
                obj,created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)

            for result in cgiresults:
                if result.progress == '3' or result.progress =='M':
                    sticker = Sticker.objects.get(slug='cgi-{}-passed'.format(result.cgi.cgi_number))
                    obj, created = StickerAssignment.objects.get_or_create(student=student, sticker=sticker)




