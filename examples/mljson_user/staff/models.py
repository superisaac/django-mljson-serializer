from __future__ import unicode_literals

from django.db import models

class Staff(models.Model):
    name = models.CharField(max_length=200, unique=True)
    boss = models.ForeignKey('self', related_name='subordinates', null=True, blank=True)

    def __unicode__(self):
        return self.name

    
