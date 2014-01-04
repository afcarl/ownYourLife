from django.db import models

class Tag(models.Model):
    """ Tags for each Category or additionally for each Entry """
    name = models.CharField(max_length=63)
    details = models.TextField()

    def __str__(self):
        return self.name

class Category(models.Model):
    """ Hierarchical categories """
    name = models.CharField(max_length=255)
    details = models.TextField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class Entry(models.Model):
    """ Each time stamped log entry """
    timestamp = models.DateTimeField('date published')
    cat = models.ForeignKey(Category)
    value = models.FloatField(default=0)
    note = models.TextField()
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return '[' + str(self.cat) + '] ' + str(self.value) + ' (' + str(self.timestamp) + ')'
