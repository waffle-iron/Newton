from django.db import models

# Create your models here.


class Teacher(models.Model):
    MS = 'Ms.'
    MRS = 'Mrs.'
    MR = 'Mr.'
    DR = 'Dr.'
    TITLE_CHOICES = (
        (MS, 'Ms.'), (MRS, 'Mrs.'), (MR, 'Mr.'),
        (DR, 'Dr.'),
    )
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50, choices=TITLE_CHOICES, default=MS)
    first_name =models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)


    def __str__(self):
        return '%s %s' % (self.title, self.last_name)

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
        ordering = ['last_name']


class CurrentClass(models.Model):
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

    id = models.AutoField(primary_key=True)
    year = models.IntegerField()
    grade = models.CharField(max_length=50, choices=GRADE_CHOICES, default=SECOND)
    teacher = models.ForeignKey(Teacher, on_delete=models.PROTECT)

    def __str__(self):
        return '%s, %s Grade, %s' % (self.teacher, self.grade, self.year)

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'
        ordering = ['year', 'grade', 'teacher']


class StudentRoster(models.Model):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),)

    student_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    current_class = models.ForeignKey(CurrentClass, on_delete=models.CASCADE, default=1)
    date_of_birth = models.DateField(blank=True,)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, blank=False, default=MALE,)
    email = models.EmailField(blank=True, verbose_name='Parent Email')

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['current_class', 'last_name']






'''
class AMCData(models.Model):
    student_id = models.ForeignKey(StudentRoster, on_delete=models.CASCADE,)
    # test_id = # The unique number of the challenge. (Addition A = 1, Fractions = 13 or something) Foreign Key?
    date_taken = models.DateField()


class CBADetails(models.Model):
    # question ID, assessments (spring1, fall2, winter 2, spring2), Question # within each test,
    # skill assessed by that question, IXL/CBA equivalents
    pass


class CBAData(models.Model):
    # The Scores each student has gotten on the different CBA tests
    pass

'''