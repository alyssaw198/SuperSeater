from django.db import models

# Create your models here.

class Student(models.Model):
    fname = models.CharField(max_length=50) #text
    lname = models.CharField(max_length=50) #text
    teachername = models.CharField(max_length=50) #text
    socialrank = models.CharField(max_length=50) #range
    focus = models.CharField(max_length=50) #range
    sound_env = models.CharField(max_length=50) #radio
    friend = models.CharField(max_length=50) #text
    board_distance = models.CharField(max_length=50)

    def __str__(self):
        return (self.fname + " " + self.lname)
 