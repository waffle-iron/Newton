# scripts/load_ixl_skills.py

# Full path and name to your csv file
csv_filepathname="/Users/alexandertrost/PycharmProjects/newton/scripts/IXLMaster.csv"

# Full path to your django project directory
your_djangoproject_home="/Users/alexandertrost/PycharmProjects/newton/"
import django

import sys,os
sys.path.append(your_djangoproject_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
django.setup()
from ixl.models import IXLSkill


import csv
dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

# Start execution
def run():
    for row in dataReader:
        if row[0] != 'Category': # Ignore the header row, import everything else
            skill = IXLSkill()
            skill.category = row[0]
            skill.skill_id = row[1]
            skill.skill_description = row[2]
            skill.save()