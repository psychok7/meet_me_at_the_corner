from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Friend(models.Model):
    user1 = models.ForeignKey(User, related_name='user1')
    user2 = models.ForeignKey(User, related_name='user2')
    
    def __unicode__(self):
        return self.user1.username
        
    class Meta:
        db_table = u'friends'

class Zone(models.Model):
	user = models.ForeignKey(User)
	lat = models.DecimalField(max_digits=11, decimal_places=6)
	lng = models.DecimalField(max_digits=11, decimal_places=6)
	radious = models.DecimalField(max_digits=11, decimal_places=6)