
import datetime

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


def initialise():
    admin = User.objects.create_superuser('admin', 'timp@paneris.org', 'admin')
    admin.first_name = "Adam"
    admin.last_name = "Admin"
    admin.save()

    florap = create_child('Flora', 'Pizey', 'F', '2004-08-22', 'Tim', 'Pizey')


def create_child(first_name, family_name, gender, dob,
                 carer_first_name, carer_family_name, **kwargs):
    carer_u = User.objects.create_user(username(carer_first_name, carer_family_name))
    carer_u.first_name = carer_first_name
    carer_u.family_name = carer_family_name
    carer_u.save()
    carer_m = Member()
    carer_m.user = carer_u
    carer_m.save()

    child_u = User.objects.create_user(username(first_name, family_name))
    child_u.first_name = first_name
    child_u.family_name = family_name
    child_u.save()
    child_m = Member()
    child_m.user = child_u
    child_m.gender = gender
    child_m.dob = dob
    child_m.save()
    child_c = Child()
    child_c.member = child_m
    child_c.carer = carer_m
    child_c.save()


def username(first_name, family_name):
    return "%s%s)" % (str(first_name).lower(), str(family_name).lower()[0])


class Member(models.Model):
    user = models.OneToOneField(User)

    gender = models.CharField(max_length=1,
                              choices=(('M', 'Male'), ('F', 'Female')),
                              default= 'F')
    role = models.CharField(max_length=10,
                            choices=(('Member', 'Member'),
                                     ('Carer', 'Carer'),
                                     ('Helper', 'Helper'),
                                     ('Leader', 'Leader'),
                                     ('Officer', 'Officer'),
                                     ),
                            default= 'Member')

    mobile_number = models.CharField(max_length=16, blank=True)
    landline_number = models.CharField(max_length=16, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.user.first_name, self.user.last_name)


class Child(models.Model):
    member = models.OneToOneField(Member)
    dob = models.DateField(help_text='Format: YYYY/MM/DD',
                           validators=[MinValueValidator(datetime.date(1900, 7, 22)),
                                       MaxValueValidator(datetime.date(2012, 12, 12))],
                           null=True)


    carer = models.ForeignKey(Member, related_name='carer', null=True)
    carer_2 = models.ForeignKey(Member, related_name='+', null=True,  on_delete=models.SET_NULL)
    emergency_contact = models.ForeignKey(Member, related_name='+', null=True)

    allergies = models.TextField()
    conditions = models.TextField()

    doctors_name = models.CharField(max_length=15)
    doctors_phone = models.CharField(max_length=16, blank=True)
    doctors_address = models.TextField()

    class Meta:
        verbose_name_plural = "children"

    def __unicode__(self):
        return self.member.__unicode__()
