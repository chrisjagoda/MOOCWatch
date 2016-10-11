from django.db import models

class CourseProvider(models.Model):
    provider = models.CharField(max_length = 25)
    url = models.CharField(max_length = 100)
    def __str__(self):
        return self.provider
    
COURSE_STATUSES = (
    ('a', 'Active'),
    ('i', 'Inactive'),
)

class Course(models.Model):
    url = models.URLField(max_length = 550, blank=True)
    course = models.TextField(max_length = 200)
    image = models.URLField(max_length = 300, blank=True)
    description = models.TextField(max_length = 1000)
    provider = models.CharField(max_length = 25)
    status = models.CharField(max_length = 1, choices = COURSE_STATUSES, default = 'a')
    def __str__(self):
        return self.course

COURSETAKER_STATUSES = (
    ('e', 'Enrolled'),
    ('c', 'Completed'),
    ('i', 'Inactive'),
)

class CourseTaker(models.Model):
    user = models.ForeignKey('auth.User', related_name='coursetakers')
    course = models.ForeignKey(Course)
    status = models.CharField(max_length = 1, choices = COURSETAKER_STATUSES, default = 'e')
    class Meta:
        unique_together = ['user', 'course']