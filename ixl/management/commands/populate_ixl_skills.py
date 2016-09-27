# populate_rit_bands.py

from django.core.management.base import BaseCommand, CommandError

from ixl.models import IXLSkillScores, IXLSkill

class Command(BaseCommand):
    help = 'Creates database entries for all IXL skills'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass

    import csv
    csv_filepathname = "/home/alex/newton/ixl/management/commands/IXLMaster.csv"

    dataReader = csv.reader(open(csv_filepathname), delimiter=',', quotechar='"')


# For each of the 7 subdomains that are created already,
    # Make the 14 RIT band options available and save them


    def handle(self, *args, **options):

        for row in self.dataReader:
            if row[0] != 'Category':  # Ignore the header row, import everything else
                category = row[0]
                skill_id = row[1]
                skill_description = row[2]
                obj, created = IXLSkill.objects.get_or_create(
                    category=category, skill_id=skill_id, skill_description=skill_description,
                )

