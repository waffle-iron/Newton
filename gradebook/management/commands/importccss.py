# populate_ixl_skills.py

from django.core.management.base import BaseCommand, CommandError

from gradebook.models import CommonCoreStateStandard

class Command(BaseCommand):
    help = 'Imports the Common Core State Standards'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass

    import csv
    csv_filepathname = "/home/alex/newton/gradebook/management/grade2ccss.csv"

    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')

    def handle(self, *args, **options):
        for row in self.dataReader:
            if row[0] != 'grade':  # Ignore the header row, import everything else
                grade = row[0]
                domain = row[1]
                subdomain = row[2]
                topic = row[3]
                code = row[4]
                description = row[5]
                obj, created = CommonCoreStateStandard.objects.get_or_create(
                    grade=grade, domain=domain, subdomain=subdomain, topic=topic, code=code, description=description
                )