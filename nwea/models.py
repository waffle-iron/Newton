from django.db import models

from brain.models import StudentRoster

# Create your models here.

# TODO: Add official test results here. Scores on the 7 domains, date(fall/winter/spring),


class NWEADomain(models.Model):
    ALGEBRA = 1
    NUMBER = 2
    MEASUREMENT = 3
    GEOMETRY = 4

    DOMAIN_CHOICES = (
        (ALGEBRA, 'Operations and Algebraic Thinking'),
        (NUMBER, 'Number and Operations'),
        (MEASUREMENT, 'Measurement and Data'),
        (GEOMETRY, 'Geometry'),
    )

    domain = models.IntegerField(choices=DOMAIN_CHOICES, default=ALGEBRA, verbose_name="Domain")

    def __str__(self):
        print_domain = str(self.DOMAIN_CHOICES[int(self.domain- 1)][1])
        return '%s' % print_domain

    class Meta:
        verbose_name = 'NWEA Domain'
        verbose_name_plural = 'NWEA Domains'


class NWEASubDomain(models.Model):
    PROBLEM= 1
    OPERATION = 2
    PLACEVALUE = 3
    NUMBER = 4
    MEASUREMENT = 5
    DATA = 6
    SHAPES = 7

    SUBDOMAIN_CHOICES = (
    (PROBLEM, 'Represent and Solve Problems'),
    (OPERATION, 'Properties of Operations'),
    (PLACEVALUE, 'Understand Place Value, Counting, and Cardinality'),
    (NUMBER, 'Number and Operations: Base Ten and Fractions'),
    (MEASUREMENT, 'Solve Problems Involving Measurement'),
    (DATA, 'Represent and Interpret Data'),
    (SHAPES, 'Reason with Shapes and Their Attributes'),
    )
    domain = models.ForeignKey(NWEADomain, on_delete=models.CASCADE, verbose_name='Domain')
    sub_domain = models.IntegerField(choices=SUBDOMAIN_CHOICES, default=PROBLEM, verbose_name='Sub-Domain')

    def __str__(self):
        print_subdomain = str(self.SUBDOMAIN_CHOICES[int(self.sub_domain-1)][1])
        return '%s --- %s' % (self.domain, print_subdomain,)

    class Meta:
        verbose_name = 'NWEA Sub-Domain'
        verbose_name_plural = 'NWEA Sub-Domains'


class NWEARITBand(models.Model):
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

    sub_domain = models.ForeignKey(NWEASubDomain, on_delete=models.CASCADE, )
    rit_band = models.IntegerField(choices=RIT_CHOICES, default=151)

    def __str__(self):
        return ' %s  RIT Band: %s' % (self.sub_domain, self.rit_band,)

    class Meta:
        verbose_name = 'NWEA RIT Band'
        verbose_name_plural = 'NWEA RIT Bands'


class NWEATestResults(models.Model):
    # The test results from official NWEA assessments. 7 subdomains, integer fields, all 3 digits.
    # Student, Each Subdomain
    #student = models.ForeignKey(StudentRoster, on_delete=models.CASCADE, blank=False, null=False,)
    # Need 7 boxes with each of the subdomains
    #sub1 = models.ForeignKey(NWEASubDomain)
    pass