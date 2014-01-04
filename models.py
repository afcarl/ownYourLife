from django.db import models

class Tag(models.Model):
    """ Tags for each Category or additionally for each Entry """
    name = models.CharField(max_length=63)
    details = models.TextField()

    def __str__(self):
        return self.name

class Category(models.Model):
    """ Hierarchical categories """
    name = models.CharField(max_length=255, unique=True)
    details = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)
    defaultValue = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Entry(models.Model):
    """ Each time stamped log entry """
    timestamp = models.DateTimeField('date published')
    cat = models.ForeignKey(Category)
    value = models.FloatField(blank=True)
    note = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return '[' + str(self.cat) + '] ' + str(self.value) + ' (' + str(self.timestamp) + ')'
