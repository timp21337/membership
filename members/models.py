
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


def initialise():
    me = User.objects.create_superuser('timp', 'timp@paneris.org', 'admin')
    me.first_name = "Tim"
    me.last_name = "Pizey"
    me.save()


class Member(models.Model):
    user = models.OneToOneField(User)

    dob = models.DateField(help_text='Format: YYYY/MM/DD',
                           validators=[MinValueValidator(datetime.date(1900, 7, 22)),
                                       MaxValueValidator(datetime.date(2012, 12, 12))])

    gender = models.CharField(max_length=1,
                              choices=(('M', 'Male'), ('F', 'Female')),
                              default= 'F')
    role = models.CharField(max_length=1,
                            choices=(('Member', 'Member'),
                                     ('Carer', 'Carer'),
                                     ('Helper', 'Helper'),
                                     ('Leader', 'Leader'),
                                     ('Officer', 'Officer'),
                                     ),
                            default= 'Member')
    is_child = models.BooleanField(default=True)
    mobile_number = models.CharField(max_length=16, blank=True)
    landline_number = models.CharField(max_length=16, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.user.first_name, self.user.last_name)
