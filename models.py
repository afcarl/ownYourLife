from django.db import models

class Category(models.Model):
    """ Hierarchical categories """
    name = models.CharField(max_length=255)
    details = models.TextField()

class Entry(models.Model):
    """ Each time stamped log entry """
    timestamp = models.DateTimeField('date published')
    cat = models.ForeignKey(Category)
    value = models.FloatField(default=NaN)
    note = models.TextField()
