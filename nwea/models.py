from django.db import models

from brain.models import StudentRoster

# 70+ RIT Bands
# 600 Skills
# NWEAScore ( 7 fields for 7 domains)

# domain1_rit = NWEAScore.domain1
# domain1_exercises = NWEASkills.objects.all().filter(domain=1,).filter(rit_band=domain1_rit)


# NWEA Subdomains
# NWEARITBand (Has: Subdomain(FK), RIT #)
# NWEASkill (Has: rit_band, skill, ixl_equivalent, cba)
# NWEAScore (Has: 1 number for each of the 7 subdomains)



class RITBand(models.Model):
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

    PROBLEM = 1
    OPERATION = 2
    PLACEVALUE = 3
    NUMBER_SUB = 4
    MEASUREMENT_SUB = 5
    DATA = 6
    SHAPES = 7

    SUBDOMAIN_CHOICES = (
        (PROBLEM, 'Represent and Solve Problems'),
        (OPERATION, 'Properties of Operations'),
        (PLACEVALUE, 'Understand Place Value, Counting, and Cardinality'),
        (NUMBER_SUB, 'Number and Operations: Base Ten and Fractions'),
        (MEASUREMENT_SUB, 'Solve Problems Involving Measurement'),
        (DATA, 'Represent and Interpret Data'),
        (SHAPES, 'Reason with Shapes and Their Attributes'),
    )
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

    domain = models.CharField(choices=DOMAIN_CHOICES,max_length=255 )
    subdomain = models.CharField(choices=SUBDOMAIN_CHOICES, max_length=255)
    rit_band = models.PositiveIntegerField(choices=RIT_CHOICES, default=151 )

    def __str__(self):
        return '{} {} {}'.format(self.domain, self.subdomain, self.rit_band)

    class Meta:
        verbose_name = 'RIT Band'
        verbose_name_plural = 'RIT Bands'


class NWEASkill(models.Model):
    rit_band = models.ForeignKey(RITBand, on_delete=models.CASCADE)
    skill = models.CharField(max_length=255, )
    ixl_match = models.CharField(max_length=7, blank=True)

    def __str__(self):
        output = '{} {} {}'.format(self.rit_band.domain, self.rit_band.subdomain, self.skill)
        if self.ixl_match:
            output = output + ', IXL Match: ' + self.ixl_match
        return output

    class Meta:
        verbose_name = 'NWEA Skill'
        verbose_name_plural = 'NWEA Skills'


class NWEAScore(models.Model):
    FK = 'Kindergarten, Fall'
    WK = 'Kindergarten, Winter'
    SK = 'Kindergarten, Spring'
    F1 = '1st Grade, Fall'
    W1 = '1st Grade, Winter'
    S1 = '1st Grade, Spring'
    F2 = '2nd Grade, Fall'
    W2 = '2nd Grade, Winter'
    S2 = '2nd Grade, Spring'
    F3 = '3rd Grade, Fall'
    W3 = '3rd Grade, Winter'
    S3 = '3rd Grade, Spring'
    F4 = '4th Grade, Fall'
    W4 = '4th Grade, Winter'
    S4 = '4th Grade, Spring'

    DATE_CHOICES = (
        (FK, 'Kindergarten, Fall'),
        (WK, 'Kindergarten, Winter'),
        (SK, 'Kindergarten, Spring'),
        (F1, '1st Grade, Fall'),
        (W1, '1st Grade, Winter'),
        (S1, '1st Grade, Spring'),
        (F2, '2nd Grade, Fall'),
        (W2, '2nd Grade, Winter'),
        (S2, '2nd Grade, Spring'),
        (F3, '3rd Grade, Fall'),
        (W3, '3rd Grade, Winter'),
        (S3, '3rd Grade, Spring'),
        (F4, '4th Grade, Fall'),
        (W4, '4th Grade, Winter'),
        (S4, '4th Grade, Spring'),
    )

    student = models.ForeignKey(StudentRoster, on_delete=models.CASCADE)
    test_period = models.CharField(choices=DATE_CHOICES, default=F2, max_length=255)
    subdomain1 = models.IntegerField(verbose_name="SubDomain 1")
    subdomain2 = models.IntegerField(verbose_name="SubDomain 2")
    subdomain3 = models.IntegerField(verbose_name="SubDomain 3")
    subdomain4 = models.IntegerField(verbose_name="SubDomain 4")
    subdomain5 = models.IntegerField(verbose_name="SubDomain 5")
    subdomain6 = models.IntegerField(verbose_name="SubDomain 6")
    subdomain7 = models.IntegerField(verbose_name="SubDomain 7")

    def __str__(self):
        print_date = str(self.test_period)
        scores = ("{}, {}, {}, {}, {}, {}, {}".format(self.domain1, self.domain2, self.domain3, self.domain4, self.domain5, self.domain6, self.domain7))
        return '{} {} {} {}'.format(self.student.first_name, self.student.last_name, print_date, scores )

    class Meta:
        verbose_name = 'NWEA Score'
        verbose_name_plural = 'NWEA Scores'


'''
class Domain(models.Model):
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
    pass'''
