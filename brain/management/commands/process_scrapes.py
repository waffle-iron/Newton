# scripts/import_students.py


student_csv="brain/management/commands/studentroster2016.csv"

# Full path to your django project directory
your_djangoproject_home="/home/alex/newton/"
import django
import datetime
import sys,os
from os import listdir
import re
sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")

django.setup()

from django.core.management.base import BaseCommand, CommandError
from brain.models import StudentRoster, CurrentClass, Teacher
from brain.scripts.webscrape import run_all_teachers
from ixl.models import IXLSkill, IXLStats, IXLSkillScores
from brain.models import ReadingStats

import csv

class Command(BaseCommand):
    help = 'Scrapes IXL and myON for our data'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass


    def handle(self, *args, **options):
        csv_list = listdir('brain/scripts/csvdownloads')  # Gets the downloaded file list from the directory
        lexile_files = []
        score_grid_files = []
        ixl_stats_files = []
        myon_book_files = []
        myon_time_files = []
        for x in range(len(csv_list)):  # Starts to sort all the data into 1 csv for each data type
            current_file = csv_list[x]
            # Figure out which file we're working with (lexile, Score-Grid, or ixlstats)
            if 'lexile' in current_file:
                lexile_files.append(current_file)
            elif 'booksReadByStudent' in current_file:
                myon_book_files.append(current_file)
            elif 'timeSpentByStudent' in current_file:
                myon_time_files.append(current_file)
            elif 'Score-Grid' in current_file:
                score_grid_files.append(current_file)
            elif 'ixlstats' in current_file:
                ixl_stats_files.append(current_file)
            else:
                print("File {} Not Recognized".format(current_file))




        for file in ixl_stats_files:
            self.import_ixl_stats(file)
            os.remove('brain/scripts/csvdownloads/' + file)

        for file in lexile_files:
            self.import_lexile_stats(file)
            os.remove('brain/scripts/csvdownloads/' + file)

        for file in myon_time_files:
            self.import_myontime_stats(file)
            os.remove('brain/scripts/csvdownloads/' + file)

        for file in myon_book_files:
            self.import_myonbook_stats(file)
            os.remove('brain/scripts/csvdownloads/' + file)

        for file in score_grid_files:
            self.import_ixl_scores(file)
            os.remove('brain/scripts/csvdownloads/' + file)


    def import_ixl_scores(self, file_name):
        indexed = False
        print("Starting Import of IXL Grid")
        dataReader = csv.reader(open('brain/scripts/csvdownloads/' + file_name), delimiter=',', quotechar='"')
        if self.check_exercise_accuracy(dataReader):
            # print("All Exercises match.")
            dataReader = csv.reader(open('brain/scripts/csvdownloads/' + file_name), delimiter=',', quotechar='"')
            for row in dataReader:
                if row[0] == 'Category':  # Go through and replace student names with their Newton IDs.
                    if not indexed:
                        count = 3
                        for column in row:
                            #print(column)
                            if column in ['Category', 'Skill code', 'Skill name', ]:
                                continue
                            elif column not in ['Category', 'Skill code', 'Skill name', ]:
                                namesRegex = re.compile(r'([a-zA-Z\'-]+)\s([a-zA-Z\'-]+)')
                                mo = namesRegex.search(column)

                                first_name=mo.group(1)
                                last_name=mo.group(2)
                                student_id = StudentRoster.objects.get(first_name__icontains=first_name,
                                                                last_name__icontains = last_name)
                                row[count] = student_id.student_id
                            count += 1
                        names_list = row
                        print(names_list)
                        indexed = True

                # For the rest of the rows:
                else:
                    current_skill_id = row[1]
                    count = 0
                    for column in row:
                        print("{} is the column. The skill ID is {}".format(column, current_skill_id))
                        if self.is_number(column):
                            score = int(column)
                            student_id = StudentRoster.objects.get(student_id=names_list[count])
                            try:
                                skill_id = IXLSkill.objects.get(skill_id=current_skill_id)
                                print("Found a number. The number is {}".format(column))
                                # ixl_skill_id = skill_id.pk
                                #todays_date = datetime.date.today()
                                #print("Today's Date:{}".format(todays_date))
                                print("Score: {}  Student: {}  IXL: {}".format(score, student_id, skill_id))
                                defaults = {'score': score,}
                                obj, created = IXLSkillScores.objects.update_or_create(
                                    student_id=student_id,
                                    ixl_skill_id=skill_id,
                                    defaults=defaults)
                                print("Saved)")
                            except:
                                pass
                        else:
                            #print("{} is not a number".format(column))
                            pass
                        count += 1
        else:
            print("Exercises have changed!")

    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def check_exercise_accuracy(self, dataReader):
        # 1. Check all exercises are the same, if so, go to the rest of the script.
        output = True
        for row in dataReader:
            if row[0] == 'Category':
                pass
            else:
                try:
                    skill = IXLSkill.objects.get(category=row[0], skill_id=row[1])
                except:
                    output = False
                    print("There was no IXL Skill found with Category {}, ID {}, and Description {}".format(row[0],
                                                                                                            row[1],
                                                                                                            row[2]))
                    # Raise the alarm.
                    # Start fixing what has been changed.
                    # fix_changed_skills()
        return output

    def import_ixl_stats(self, file):
        print("Importing IXL Stats")
        dataReader = csv.reader(open('brain/scripts/csvdownloads/' + file), delimiter=',', quotechar='"')
        for row in dataReader:
            full_name = row[0]
            first_name, last_name = full_name.split(" ")
            practiced_string = row[1]
            if 'days ago' in practiced_string:
                number, delete1, delete2 = practiced_string.split(" ")
            elif 'yesterday' in practiced_string.lower():
                number = 1
            elif 'today' in practiced_string.lower():
                number = 0
            elif '-' in practiced_string.lower():
                number = -1
            else:
                number = -1
            last_practiced = int(number)
            questions_answered = row[2].replace(',', '')
            questions_answered = int(questions_answered)
            time_string = row[3]
            if 'hr' in time_string:
                timeRegex = re.compile(r'(\d+) hr (\d+) min')
                result = timeRegex.search(time_string)
                hours = int(result.group(1))
                minutes = int(result.group(2))
                total_time = hours * 60 + minutes
                time_spent = int(total_time)
            elif 'hr' not in time_string:
                timeRegex = re.compile(r'(\d+) min')
                result = timeRegex.search(time_string)
                time_spent = int(result.group(1))
            try:
                student = StudentRoster.objects.get(first_name__icontains=first_name,
                                                    last_name__icontains=last_name)
                updated_values = {'last_practiced': last_practiced, 'questions_answered': questions_answered, 'time_spent':
                            time_spent}
                obj, created = IXLStats.objects.update_or_create(
                    student=student,
                    defaults=updated_values,)
            except:
                pass




    def import_lexile_stats(self,file):
        print("Importing Lexile Stats")
        dataReader = csv.reader(open('brain/scripts/csvdownloads/' + file), delimiter=',', quotechar='"')
        for row in dataReader:
            if row[0] == 'student_user_id':
                continue
            elif row[0] != 'student_user_id':
                last_name = str(row[2])
                first_name = str(row[3])
                starting_lexile = row[6]
                try:
                    starting_lexile = int(starting_lexile)
                    if starting_lexile < 0:
                        starting_lexile = 0
                except:
                    starting_lexile = 0
                test_count = row[12]
                lexile_score = row[8]
                try:
                    student = StudentRoster.objects.get(first_name__icontains=first_name,
                                                        last_name__icontains=last_name)
                    defaults = {'current_lexile': lexile_score, 'myon_tests_taken': test_count,
                                'starting_lexile':starting_lexile}
                    obj, created = ReadingStats.objects.update_or_create(
                        student=student,
                        defaults=defaults)
                except:
                    pass


    def import_myontime_stats(self,file):
        print("Importing Myon Time Stats")
        dataReader = csv.reader(open('brain/scripts/csvdownloads/' + file), delimiter=',', quotechar='"')
        for row in dataReader:
            if row[0] == 'student_user_id':
                continue
            elif row[0] != 'student_user_id':
                last_name = str(row[2])
                first_name = str(row[3])
                try:
                    myon_time_spent = round(float(row[6]) * 60)
                except:
                    myon_time_spent = 0
                try:
                    student = StudentRoster.objects.get(first_name__icontains=first_name,
                                                        last_name__icontains=last_name)
                    defaults = {'myon_time_spent': myon_time_spent, }
                    obj, created = ReadingStats.objects.update_or_create(
                        student=student,
                        defaults=defaults)
                except:
                    pass

    def import_myonbook_stats(self, file):
        print("Importing myon book Stats")
        dataReader = csv.reader(open('brain/scripts/csvdownloads/' + file), delimiter=',', quotechar='"')
        for row in dataReader:
            if row[0] == 'student_user_id':
                continue
            elif row[0] != 'student_user_id':
                last_name = str(row[2])
                first_name = str(row[3])
                myon_books_finished = row[6]
                myon_books_opened = row[8]
                try:
                    student = StudentRoster.objects.get(first_name__icontains=first_name,
                                                        last_name__icontains=last_name)
                    defaults = {'myon_books_finished': myon_books_finished, 'myon_books_opened': myon_books_opened,}
                    obj, created = ReadingStats.objects.update_or_create(
                        student=student,
                        defaults=defaults)
                except:
                    pass



                    #       myon_time_spent