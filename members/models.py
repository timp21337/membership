
import datetime
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


def initialise():
    admin = User.objects.create_superuser('admin', 'timp@paneris.org', 'admin')
    admin.first_name = "Adam"
    admin.last_name = "Admin"
    admin.save()


def create_adult(first_name, last_name, email, gender, address, landline, mobile):
    adult_u = User.objects.create_user(username(first_name, last_name))
    adult_u.first_name = first_name
    adult_u.last_name = last_name
    adult_u.email = email
    adult_u.save()

    adult_m = Member()
    adult_m.user = adult_u
    adult_m.gender = gender
    adult_m.address = address
    adult_m.landline = landline
    adult_m.mobile = mobile
    adult_m.role = 'Carer'
    adult_m.save()
    return adult_m


def create_child(first_name, last_name, gender, dob, carer):
    child_u = User.objects.create_user(username(first_name, last_name))
    child_u.first_name = first_name
    child_u.last_name = last_name
    child_u.save()
    child_m = Member()
    child_m.user = child_u
    child_m.gender = gender

    child_m.save()
    child_c = Child()
    child_c.member = child_m
    child_c.carer = carer
    bits = str(dob).split('-')
    child_c.dob = date(int(bits[0]), int(bits[1]), int(bits[2]))
    child_c.save()
    return child_c


def username(first_name, last_name):
    return "%s%s" % (str(first_name).lower(), str(last_name).lower()[0])


class Member(models.Model):
    user = models.OneToOneField(User, primary_key=True)

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
    address = models.TextField()

    mobile = models.CharField(max_length=16, blank=True)
    landline = models.CharField(max_length=16, blank=True)

    def __unicode__(self):
        return "%s (%s)" % (self.user.first_name, self.user.last_name)


class Child(models.Model):
    member = models.OneToOneField(Member, primary_key=True)
    dob = models.DateField(help_text='Format: YYYY/MM/DD',
                           validators=[MinValueValidator(datetime.date(1900, 7, 22)),
                                       MaxValueValidator(datetime.date(2012, 12, 12))],
                           null=True)
    status = models.CharField(max_length=10,
                              choices=(('Elfin', 'Elfin'),
                                       ('Pioneer', 'Pioneer'),
                                       ('Woodchip', 'Woodchip'),
                                       ('Gone', 'Gone'),
                                       ('Waiting', 'Waiting'),
                                       ),
                              default= 'Elfin')

    carer = models.ForeignKey(Member, related_name='carer', null=True)
    carer_2 = models.ForeignKey(Member, related_name='+', null=True,  on_delete=models.SET_NULL)
    emergency_contact = models.ForeignKey(Member, related_name='+', null=True)
    doctor = models.ForeignKey(Member, related_name='+', null=True)

    allergies = models.TextField(default="None")
    conditions = models.TextField(default="No")
    diet = models.TextField(default="None")
    medicines = models.TextField(default="No")

    class Meta:
        verbose_name_plural = "children"

    def __unicode__(self):
        return self.member.__unicode__()

    def registrationFormLatex(self):

        template = file('members/tex/RegistrationForm.tex.template', 'r').read()
        dotted = dottedDict(self, 'child', {})
        done = False
        while not done:
            try:
                page = template % dotted
                done = True
            except KeyError, e:
                dotted[e.message] = ''
        return page


def dottedDict(model, name, dict):
    for f in model._meta.fields:
        if type(f) in [models.fields.related.ForeignKey, models.fields.related.OneToOneField]:
            referred = getattr(model, f.name)
            if referred is not None:
                dottedDict(referred, '%s.%s' % (name, f.name), dict)
        else:
            dict['%s.%s' % (name, f.name)] = model.__dict__[f.name]

    return dict
