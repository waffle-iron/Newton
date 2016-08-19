# populate_rit_bands.py

from django.core.management.base import BaseCommand, CommandError

from nwea.models import NWEAScore, NWEASkill, RITBand

class Command(BaseCommand):
    help = 'Creates database entries for all permutations of (NWEADomain, NWEASubDomain, NWEARITBand)'

    def add_arguments(self, parser):
        # add arguments here if you need some customization
        pass


# For each of the 7 subdomains that are created already,
    # Make the 14 RIT band options available and save them


    def handle(self, *args, **options):
        all_sub = RITBand
        for x in range(1, 8):
            current_subdomain = all_sub.subdomain.
            print(current_subdomain)
            for rit_choice, _ in RITBand.RIT_CHOICES:
                new_rit_band = RITBand(sub_domain=current_subdomain, rit_band=rit_choice)
                #print("The new rit band is: %s" % new_rit_band)
                new_rit_band.save()

        #for sub_domain in all_sub:
            #print(sub_domain)


        '''
        for sub_domain, _ in NWEASubDomain.SUBDOMAIN_CHOICES:
            # create your Sub Domains
            print(sub_domain)
            print(_)

        all_rit = NWEARITBand.objects.all()
        print(all_rit)
        print("RIT CHOICES")


        '''
