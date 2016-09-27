#! scripts/create_rit_bands.py

# Full path and name to your csv file
#csv_filepathname="/Users/alexandertrost/PycharmProjects/newton/ixl/scripts/IXLMaster.csv"

# Full path to your django project directory
your_djangoproject_home="/Users/alexandertrost/PycharmProjects/newton/"
import django
import sys,os
sys.path.append(your_djangoproject_home)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newton.settings")
django.setup()
from nwea.models import NWEASkill, NWEAScore, RITBand





def make_rit_bands():
    SUBDOMAINS = [(1, 1), (1, 2), (2, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8)]
    RIT_CHOICES = (
        (111, '111'),
        (121, '121'),
        (131, '131'),
        (141, '141'),
        (151, '151'),
        (161, '161'),
        (171, '171'),
        (181, '181'),
        (191, '191'),
        (201, '201'),
        (211, '211'),
        (221, '221'),
        (231, '231'),
        (241, '241'),
    )

    for item in SUBDOMAINS:
        current_domain = item[0]
        current_sub = item[1]
        for rit_choice, _ in RIT_CHOICES:
            new_rit_band = RITBand(subdomain=current_sub, domain=current_domain, rit_band=rit_choice)
            print("The new rit band is: %s" % new_rit_band)
            new_rit_band.save()

#all_sub = RITBand.DOMAIN_CHOICES
# def make_rit():
#     for x in range(1, 8):
#         current_subdomain = all_sub.get(sub_domain=x)
#         #print(current_subdomain)
#         for rit_choice, _ in NWEARITBand.RIT_CHOICES:
#             new_rit_band = NWEARITBand(sub_domain=current_subdomain, rit_band=rit_choice)
#             #print("The new rit band is: %s" % new_rit_band)
#             #new_rit_band.save()
#
# make_rit_bands()
