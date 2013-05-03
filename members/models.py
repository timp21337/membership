import os

import datetime
from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import subprocess

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '../')

print PROJECT_ROOT


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


def create_backup(member):
    member.role = "Backup"
    member.save()
    return member


def create_doctor(member):
    member.role = "Doctor"
    member.save()
    return member


def create_child(first_name, last_name, gender, dob, carer):
    child_u = User.objects.create_user(username(first_name, last_name))
    child_u.first_name = first_name
    child_u.last_name = last_name
    child_u.save()
    child_m = Member()
    child_m.user = child_u
    child_m.gender = gender
    child_m.carer = carer
    bits = str(dob).split('-')
    child_m.dob = date(int(bits[0]), int(bits[1]), int(bits[2]))
    child_m.save()
    return child_m


def username(first_name, last_name):
    return "%s_%s" % (degunked(first_name), degunked(last_name))


def degunked(string):
    return str(string).replace(' ', '').replace('-', '').lower()


class Member(models.Model):
    user = models.OneToOneField(User, primary_key=True)

    gender = models.CharField(max_length=1,
                              choices=(('M', 'Male'), ('F', 'Female')),
                              default= 'F')
    role = models.CharField(max_length=10,
                            choices=(('Member', 'Member'),
                                     ('Carer', 'Carer'),
                                     ('Backup', 'Backup'),
                                     ('Doctor', 'Doctor'),
                                     ('Helper', 'Helper'),
                                     ('Leader', 'Leader'),
                                     ('Officer', 'Officer'),
                                     ),
                            default= 'Member')
    address = models.TextField()

    mobile = models.CharField(max_length=16, blank=True)
    landline = models.CharField(max_length=16, blank=True)
    crb_expiry = models.DateField(help_text='Format: YYYY/MM/DD',
                                  validators=[MinValueValidator(datetime.date(2011, 7, 22)),
                                              MaxValueValidator(datetime.date(2016, 12, 12))],
                                  null=True)
    membership_expiry = models.DateField(help_text='Format: YYYY/MM/DD',
                                         validators=[MinValueValidator(datetime.date(2011, 7, 22)),
                                                     MaxValueValidator(datetime.date(2016, 12, 12))],
                                         null=True)

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

    carer = models.ForeignKey('self', related_name='+', null=True, on_delete=models.SET_NULL)
    carer_2 = models.ForeignKey('self', related_name='+', null=True, on_delete=models.SET_NULL)
    backup = models.ForeignKey('self', related_name='+', null=True, on_delete=models.SET_NULL)
    doctor = models.ForeignKey('self', related_name='+', null=True, on_delete=models.SET_NULL)

    allergies = models.TextField(default="None")
    conditions = models.TextField(default="No")
    diet = models.TextField(default="None")
    medicines = models.TextField(default="No")
    date_signed = models.DateField(help_text='Format: YYYY/MM/DD',
                                   validators=[MinValueValidator(datetime.date(2011, 7, 22)),
                                               MaxValueValidator(datetime.date(2016, 12, 12))],
                                   null=True)

    def __unicode__(self):
        return "%s (%s)" % (self.user.first_name, self.user.last_name)

    def registrationFormLatex(self):
        template_name = os.path.join(os.path.dirname(__file__), 'tex/RegistrationForm.tex.template')
        template = file(template_name, 'r').read()
        dotted = dottedDict(self, 'child', {})
        done = False
        while not done:
            try:
                page = template % dotted
                done = True
            except KeyError, e:
                dotted[e.message] = ''
        return page

    @classmethod
    def output(cls):
        out_dir = os.path.join(PROJECT_ROOT, "reports")
        inc = '\\documentclass [12pt, a4paper] {article}\n'
        inc += '\\usepackage{pdfpages}\n'
        inc += '\\begin{document}\n'
        for kid in Member.objects.all():
            if kid.role == "Member":
                tex_filename = '%s/%s.tex' % (out_dir, kid.user.username)
                pdf_filename = '%s/%s.pdf' % (out_dir, kid.user.username)
                file(tex_filename, 'w').write(kid.registrationFormLatex())
                subprocess.call('pdflatex -output-directory reports %s' % tex_filename, shell=True)

                inc += '\includepdf{' + pdf_filename + '}\n'
        inc += '\\end{document}\n'
        file('%s/all.tex' % out_dir, 'w').write(inc)
        subprocess.call('pdflatex -output-directory reports %s/all.tex' % out_dir, shell=True)
        for m in Member.carers():
            print (m.user.first_name, m.user.last_name, m.membership_expiry, m.crb_expiry)


    @classmethod
    def carers(cls):
        return [o for o in cls.objects.all() if o.role not in ["Doctor", "Backup", "Member"]]


def dottedDict(model, name, dict):
    for f in model._meta.fields:
        if type(f) in [models.fields.related.ForeignKey, models.fields.related.OneToOneField]:
            referred = getattr(model, f.name)
            if referred is not None:
                dottedDict(referred, '%s.%s' % (name, f.name), dict)
        else:
            dict['%s.%s' % (name, f.name)] = model.__dict__[f.name]

    return dict
