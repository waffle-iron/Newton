from django.db import models
from django.core.validators import RegexValidator

# Create your models here.

class CommonCoreStateStandard(models.Model):

    KINDER = 'K'
    FIRST = '1st'
    SECOND = '2nd'
    THIRD = '3rd'
    FOURTH = '4th'
    FIFTH = '5th'
    SIXTH = '6th'
    SEVENTH = '7th'
    EIGHTH = '8th'

    GRADE_CHOICES = (
        (KINDER, 'Kindergarten'), (FIRST, '1st Grade'), (SECOND, '2nd Grade'),
        (THIRD, '3rd Grade'), (FOURTH, '4th Grade'), (FIFTH, '5th Grade'),
        (SIXTH, '6th Grade'), (SEVENTH, '7th Grade'), (EIGHTH, '8th Grade'),
    )
    ccss_format = RegexValidator(r'^CCSS\.(.*)$', 'Pattern must match IXL format: D-A.12')
    grade = models.CharField(max_length=50, choices=GRADE_CHOICES, default=SECOND)
    domain = models.CharField(max_length=50, null=False, blank=False, default="Reading")
    subdomain = models.CharField(max_length=100, blank=True, )
    topic = models.CharField(max_length=100, null=False, blank=False, default="Key Ideas and Details") # Bolded on CCSS
    code = models.CharField(max_length=100, validators=[ccss_format], blank=False, verbose_name="CCSS Code") # CCSS.ELA-LITERACY.RI.2.1
    description = models.CharField(max_length=1000,) # The standard's text.


    class Meta:
        verbose_name = 'Common Core Standard'
        verbose_name_plural = 'Common Core Standards'

    def __str__(self):
        return "{} {} - {}: {}".format(self.domain, self.subdomain, self.topic, self.code)