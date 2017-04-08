from django.db import models
import datetime
import re

# Create your models here.

class Video(models.Model):
    WRIT = "WRITING"
    READ = "READING"
    MATH = "MATH"
    CORE = "CORE"

    SUBJECT_CHOICES = (
        (WRIT, "Writing"),
        (READ, "Reading"),
        (MATH, "Math"),
        (CORE, "Core Knowledge"),
    )

    subject = models.CharField(max_length=256, verbose_name='Subject', blank=False,
                               choices=SUBJECT_CHOICES, default=MATH)
    title = models.CharField(max_length=256, verbose_name='Title of Video', blank=False)
    shareurl = models.CharField(max_length=500,  verbose_name='URL', blank=False,
                                help_text="The Google Drive Share Link URL")
    lesson_date = models.DateField(blank=True, default=datetime.date.today, verbose_name="Lesson Date",
                                   help_text="The date the lesson is scheduled for.")

    #videoid = models.CharField(default=getvideoid)
    def getvideoid(self):
        videoIDregex = re.compile(r'[a-zA-Z0-9\-\_]{28}[^/]*$')
        id = videoIDregex.search(self.shareurl)
        return str(id.group())