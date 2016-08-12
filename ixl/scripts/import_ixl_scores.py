# scripts/load_ixl_skills.py

# Full path and name to your csv file
csv_filepathname="/Users/alexandertrost/PycharmProjects/newton/ixl/scripts/ixl-gradebook-example.csv"

# Full path to your django project directory
your_djangoproject_home="/Users/alexandertrost/PycharmProjects/newton/"
import django
import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()
from ixl.models import IXLSkillScores

import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

# Start execution
def run():
    # Go through and replace student names with their Newton IDs.



    #Find eligible scores
    for row in dataReader:
        if row[0] == 'Skill code':
            skill_codes = row
        if row[0] not in ['Category', 'Skill code', "Skill name"]: # Ignore the header row, import everything else
            i = 0
            for column in row:
                linenum = dataReader.line_num
                try:
                    if int(column) <= 100 and int(column) > 20:
                        print("Score: {}  Row:: {} Student: {}  Skill ID: {}".format(column, linenum, row[0], skill_codes[i]))
                except ValueError:
                    pass
                i+=1

'''for row in dataReader:
    if row[0] != 'Category':  # Ignore the header row, import everything else
        skill = IXLSkill()
        skill.category = row[0]
        skill.skill_id = row[1]
        skill.skill_description = row[2]
        skill.save()'''