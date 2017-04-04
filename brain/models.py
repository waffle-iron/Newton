from django.db import models
from datetime import date
from django.utils.timezone import now
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
    first_name =models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)


    def __str__(self):
        return '%s %s' % (self.title, self.last_name)

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
        ordering = ['last_name']


class CurrentClass(models.Model):
    FOURTEEN = '14-15'
    FIFTEEN = '15-16'
    SIXTEEN = '16-17'
    SEVENTEEN = '17-18'
    EIGHTEEN = '18-19'
    NINETEEN = '19-20'
    TWENTY = '20-21'
    TWENTYONE = '21-22'

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
    YEAR_CHOICES = (
        (FOURTEEN, '14-15'),
        (FIFTEEN, '15-16'),
        (SIXTEEN, '16-17'),
        (SEVENTEEN, '17-18'),
        (EIGHTEEN, '18-19'),
        (NINETEEN, '19-20'),
        (TWENTY, '20-21'),
        (TWENTYONE, '21-22'),
    )

    id = models.AutoField(primary_key=True)
    year = models.CharField(max_length=100, choices=YEAR_CHOICES)
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
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default=MALE,)
    email = models.EmailField(blank=True, verbose_name='Parent Email')
    # detail = models.

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['current_class', 'last_name']


class AccountInfo(models.Model):
    student = models.ForeignKey(StudentRoster, on_delete=models.CASCADE)
    ixluser = models.CharField(max_length=200, blank=True, verbose_name='IXL Username')
    ixlpass = models.CharField(max_length=200, blank=True, verbose_name='IXL Password')
    kidsazteacher = models.CharField(max_length=200, blank=True, verbose_name='Kids A-Z Teacher')
    kidsazuser = models.CharField(max_length=200, blank=True, verbose_name='Kids A-Z Username')
    kidsazpass = models.CharField(max_length=200, blank=True, verbose_name='Kids A-Z Password')
    myonuser = models.CharField(max_length=200, blank=True, verbose_name='myON Username')
    myonpass = models.CharField(max_length=200, blank=True, verbose_name='myON Password')
    videos = models.BooleanField(default=False, verbose_name="Video Access",help_text="Do 2nd Grade Videos appear on the student's portal page to view?")
    readworkscode = models.CharField(max_length=50,blank=True, verbose_name="Readworks Class Code")
    enrichmentreadworkscode = models.CharField(max_length=50,blank=True, verbose_name="Enrichment Readworks Class Code", help_text="Only for students in Enrichment")

    class Meta:
        verbose_name = 'Account Information'
        verbose_name_plural = 'Account Information'

    def __str__(self):
        return "%s's account info" % (self.student)


class ReadingStats(models.Model):
    student = models.ForeignKey(StudentRoster, on_delete=models.CASCADE)
    starting_lexile = models.IntegerField(blank=True, null=True, verbose_name='Starting Lexile')
    current_lexile = models.IntegerField(blank=True, null=True, verbose_name='Current Lexile')
    goal_lexile = models.IntegerField(blank=True, null=True, verbose_name='Goal Lexile')
    lexile_progress = models.IntegerField(blank=True, null=True, verbose_name="Lexile Progress")
    myon_tests_taken = models.IntegerField(blank=True,null=True, verbose_name='myON Tests Taken')
    starting_dra = models.CharField(max_length=10, blank=True, verbose_name='Starting DRA')
    current_dra = models.CharField(max_length=10, blank=True, verbose_name='Current DRA')
    goal_dra = models.CharField(max_length=10, blank=True, verbose_name='Goal DRA')
    myon_time_spent = models.IntegerField(blank=True, null=True, verbose_name="myON Time Spent")
    myon_books_finished = models.IntegerField(blank=True, null=True, verbose_name="myON Books Finished")
    myon_books_opened = models.IntegerField(blank=True, null=True, verbose_name="myON Books Opened")

    class Meta:
        verbose_name = "Reading Statistic"
        verbose_name_plural = "Reading Statistics"


class MorningMessage(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField(default=now,verbose_name='Date of Message')
    message = models.TextField(default="")
    class Meta:
        verbose_name = 'Morning Message'
        verbose_name_plural = 'Morning Messages'

    def __str__(self):
        return "{} {}".format(self.teacher, self.date)
    # Good Morning, Scholars!
    # Today is Tuesday, October 12th, 2016
    # We are going to learn about shapes and writing our small moments...(Message)
    # Our specials today are Art and Spanish. (Specials)
    # Let's have 'an amazing' day!
    # Love,
    # Mr. Trost and Ms. West
    # Weather
    # Upcoming Birthdays
    # Student of the Week


class MorningMessageSettings(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    greeting = models.CharField(max_length=100, default="Good Morning, Scholars!", verbose_name='Greeting')
    specialsmonday = models.CharField(max_length=255, default="Spanish and Art", verbose_name='Monday Specials')
    specialstuesday = models.CharField(max_length=255, default="Spanish and Art", verbose_name='Tuesday Specials')
    specialswednesday = models.CharField(max_length=255, default="Spanish and Art", verbose_name='Wednesday Specials')
    specialsthursday = models.CharField(max_length=255, default="Spanish and Art", verbose_name='Thursday Specials')
    specialsfriday = models.CharField(max_length=255, default="Spanish and Art", verbose_name='Friday Specials')
    box1heading = models.CharField(max_length=255, default="Library Students", verbose_name='Side Box Heading', help_text="Heading for the box at the top right. It can be used for anything and can have different information depending on the day of the week. I use mine to remind students to change out library books.")
    box1monday = models.CharField(max_length=255,default="Noel, Travis, Aniya, Zaire", verbose_name='Box Content: Mon')
    box1tuesday = models.CharField(max_length=255,default="Noel, Travis, Aniya, Zaire", verbose_name='Box Content: Tue')
    box1wednesday = models.CharField(max_length=255,default="Noel, Travis, Aniya, Zaire", verbose_name='Box Content: Wed')
    box1thursday = models.CharField(max_length=255,default="Noel, Travis, Aniya, Zaire", verbose_name='Box Content: Thu')
    box1friday = models.CharField(max_length=255,default="Noel, Travis, Aniya, Zaire", verbose_name='Box Content: Fri')
    endingcomment = models.CharField(max_length=255, default="Let's have a fantastic day!", verbose_name='Last Thought')
    signoffword = models.CharField(max_length=100, default="Love,", verbose_name='Salutation', help_text="Love, Sincerely, etc.")
    signoffteacher = models.CharField(max_length=255, default="Mr. Trost and Ms. West", verbose_name='Signature')
    moodmeter = models.BooleanField(default=True, verbose_name='Mood Meter', help_text="If you want a Mood Meter reminder to appear on your Morning Message Screen")
    weather = models.BooleanField(default=True, verbose_name='Weather', help_text="If you want a local weather box to appear on your Morning Message Screen")

    class Meta:
        verbose_name = 'Morning Message Settings'
        verbose_name_plural = 'Morning Message Settings'

    def __str__(self):
        return "{}'s Morning Message Settings".format(self.teacher)

class Subject(models.Model):
    title = models.CharField(max_length=200,verbose_name='Subject')

    def __str__(self):
        return "{}".format(self.title)


class Schedule(models.Model):
    DAY_CHOICES = (("MONDAY", 'Monday'),("TUESDAY", 'Tuesday'),("WEDNESDAY", 'Wednesday'),("THURSDAY", 'Thursday'),
                   ("FRIDAY", 'Friday'),)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    day = models.CharField(choices=DAY_CHOICES, max_length=200,)
    subject1 = models.ForeignKey(Subject,verbose_name='First Class',related_name='subject1')
    subject2 = models.ForeignKey(Subject,verbose_name='Second Class',related_name='subject2')
    subject3 = models.ForeignKey(Subject,verbose_name='Third Class',related_name='subject3')
    subject4 = models.ForeignKey(Subject,verbose_name='Fourth Class',related_name='subject4')
    subject5 = models.ForeignKey(Subject,verbose_name='Fifth Class',related_name='subject5')
    subject6 = models.ForeignKey(Subject,verbose_name='Sixth Class',related_name='subject6')
    subject7 = models.ForeignKey(Subject, verbose_name='Seventh Class', related_name='subject7')


    def __str__(self):
        return "{}'s {} Schedule".format(self.teacher, self.day)


class DataUpdate(models.Model):
    dateandtime = models.DateTimeField(default=now)

    class Meta:
        ordering = ['-dateandtime']