import os
import subprocess

import datetime
from datetime import date
from django.db import models, connection
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '../')

print PROJECT_ROOT


def initialise():
    admin = User.objects.create_superuser('admin', 'adam@example.org', 'admin')
    admin.first_name = "Adam"
    admin.last_name = "Admin"
    admin.save()


def create_adult(first_name, last_name, email, gender, address, landline, mobile):
    adult_m = Member()
    adult_m.username = username(first_name, last_name)
    adult_m.first_name = first_name
    adult_m.last_name = last_name
    adult_m.email = email
    adult_m.gender = gender
    adult_m.address = address
    adult_m.landline = landline
    adult_m.mobile = mobile
    adult_m.role = 'Carer'
    adult_m.status = 'Carer'
    adult_m.save()
    return adult_m


def create_backup(member):
    member.role = "Backup"
    member.status = 'Backup'
    member.save()
    return member


def create_doctor(member):
    member.role = "Doctor"
    member.status = 'Doctor'
    member.save()
    return member


def create_child(first_name, last_name, gender, dob, carer):
    child_m = Member()
    child_m.username = username(first_name, last_name)
    child_m.first_name = first_name
    child_m.last_name = last_name
    child_m.gender = gender
    child_m.carer = carer
    bits = str(dob).split('-')
    child_m.dob = date(int(bits[0]), int(bits[1]), int(bits[2]))
    child_m.status = 'Elfin'
    child_m.save()
    return child_m


def username(first_name, last_name):
    return "%s_%s" % (degunked(first_name), degunked(last_name))


def degunked(string):
    return str(string).replace(' ', '').replace('-', '').lower()


class Member(User):

    gender = models.CharField(max_length=1,
                              choices=(('M', 'Male'), ('F', 'Female')),
                              default= 'F')
    address = models.TextField(blank=True)

    mobile = models.CharField(max_length=16, blank=True)
    landline = models.CharField(max_length=16, blank=True)

    dob = models.DateField(help_text='Format: YYYY-MM-DD',
                           validators=[MinValueValidator(datetime.date(1900, 7, 22)),
                                       MaxValueValidator(datetime.date(2012, 12, 12))],
                           null=True,
                           blank=True)
    role = models.CharField(max_length=10,
                            choices=(('Member', 'Member'),
                                     ('Carer', 'Carer'),
                                     ('Backup', 'Backup'),
                                     ('Doctor', 'Doctor'),
                                     ('Helper', 'Helper'),
                                     ('Leader', 'Leader'),
                                     ('Officer', 'Officer'),
                                     ('Sibling', 'Sibling'),
                                     ),
                            default= 'Member')
    status = models.CharField(max_length=10,
                              choices=(('Elfin', 'Elfin'),
                                       ('Pioneer', 'Pioneer'),
                                       ('Woodchip', 'Woodchip'),
                                       ('Gone', 'Gone'),
                                       ('Waiting', 'Waiting'),
                                       ('Carer', 'Carer'),
                                       ('ExCarer', 'ExCarer'),
                                       ('Doctor', 'Doctor'),
                                       ),
                              null=True,
                              blank=True)

    carer = models.ForeignKey('self',  related_name='children', null=True, on_delete=models.SET_NULL, blank=True)
    carer_2 = models.ForeignKey('self', related_name='+', null=True, on_delete=models.SET_NULL, blank=True)
    backup = models.ForeignKey('self', related_name='+', null=True, on_delete=models.SET_NULL, blank=True)
    doctor = models.ForeignKey('self', related_name='+', null=True, on_delete=models.SET_NULL, blank=True)

    crb_expiry = models.DateField(help_text='Format: YYYY/MM/DD',
                                  validators=[MinValueValidator(datetime.date(2011, 7, 22)),
                                              MaxValueValidator(datetime.date(2016, 12, 12))],
                                  null=True,
                                  blank=True)
    membership_expiry = models.DateField(help_text='Format: YYYY/MM/DD',
                                         validators=[MinValueValidator(datetime.date(2011, 7, 22)),
                                                     MaxValueValidator(datetime.date(2016, 12, 12))],
                                         null=True,
                                         blank=True)
    allergies = models.TextField(default="None")
    conditions = models.TextField(default="No")
    diet = models.TextField(default="None")
    medicines = models.TextField(default="No")
    tetanus = models.DateField(help_text='Format: YYYY-MM-DD',
                                   validators=[MinValueValidator(datetime.date(1960, 7, 22)),
                                               MaxValueValidator(datetime.date(2016, 12, 12))],
                                   null=True,
                                   blank=True)
    date_signed = models.DateField(help_text='Format: YYYY-MM-DD',
                                   validators=[MinValueValidator(datetime.date(2011, 7, 22)),
                                               MaxValueValidator(datetime.date(2016, 12, 12))],
                                   null=True,
                                   blank=True,
                                   default=date.today())

    def extras(self):
        return [self.is_adult, self.age_years, self.firstChild, self.secondChild]

    class Meta:
        ordering = ['username']

    def __unicode__(self):
        return "%s (%s)" % (self.first_name, self.last_name)

    def is_adult(self):
        if self.role in ['Carer',
                         'Backup',
                         'Doctor',
                         'Helper',
                         'Leader',
                         'Officer']:
            return True
        else:
            return False

    def age_years(self):
        return int(self.age_decimal())

    def age_decimal(self):
        if self.dob is not None:
          return (date.today() - self.dob).days/365.25
        else: 
          return 99


    def children(self):
        return self.carer_set.all()

    def firstChild(self): 
       if self.children.count() > 0 :
         return self.children.all()[0]
       else: 
         return ''

    def secondChild(self): 
       if self.children.count() > 1 :
         return self.children.all()[1]
       else: 
         return ''
        


    def registrationFormLatex(self, title):
        print title
        template_name = os.path.join(os.path.dirname(__file__), 'tex/RegistrationForm.tex.template')
        template = file(template_name, 'r').read()
        dotted = dottedDict(self, 'member', {'title' : title})
        done = False
        while not done:
            try:
                page = template % dotted
                done = True
            except KeyError, e:
                print e
                dotted[e.message] = ''  # e.message is key name
        return page

    def membership_expired_alert(self):
        if self.membership_expiry is None:
            return '-'
        if str(self.membership_expiry) < str(date.today()):
            return '*'
        else:
            return ' '

    def crb_expired_alert(self):
        if self.crb_expiry is None:
            return '-'
        if str(self.crb_expiry) < str(date.today()):
            return '*'
        else:
            return ' '


    @classmethod
    def output(cls, selection,  *args, **kwargs):
        title = kwargs['title']
        out_dir = os.path.join(PROJECT_ROOT, "reports")
        inc = '\\documentclass [12pt, a4paper] {article}\n'
        inc += '\\usepackage{pdfpages}\n'
        inc += '\\begin{document}\n'
        if len(args) == 1 and len(args[0]) == 1:
            all_name = '%s_%s' % (selection, args[0][0])
        else:
            all_name = selection
        method = getattr(cls, selection)
        for kid in method(args):
            tex_filename = '%s/%s.tex' % (out_dir, kid.username)
            pdf_filename = '%s/%s.pdf' % (out_dir, kid.username)
            
            file(tex_filename, 'w').write(kid.registrationFormLatex(title))
            subprocess.call('pdflatex -output-directory reports %s' % tex_filename, shell=True)

            inc += '\includepdf{' + pdf_filename + '}\n'
        inc += '\\end{document}\n'
        file_name = '%s/%s.tex' % (out_dir, all_name)
        file(file_name, 'w').write(inc)
        subprocess.call('pdflatex -output-directory reports %s' % file_name, shell=True)
        connection.close()


    @classmethod
    def summary(cls, selection, *args):
        method = getattr(cls, selection)
        total = 0
        adults = 0
        kids = 0
        for m in method(args):
            total += 1
            if m.is_adult():
                adults += 1
                print ("%-12s %-17s %-1s %s %s %s %s" % (m.first_name,
                                                    m.last_name,
                                                    m.gender,
                                                    m.membership_expired_alert(),
                                                    m.membership_expiry,
                                                    m.crb_expired_alert(),
                                                    m.crb_expiry))
            else:
                kids += 1
                print ("%-12s %-17s %-1s %2.2f" % (m.first_name,
                                                 m.last_name,
                                                 m.gender,
                                                 m.age_decimal()))
        print "Total: %d Adults: %d Children: %d" %(total, adults, kids)
        connection.close()


    @classmethod
    def diets(cls, selection, *args):
        method = getattr(cls, selection)
        total = 0
        adults = 0
        kids = 0
        for m in method(args):
            total += 1
            if m.is_adult():
                adults += 1
                print ("%-12s %-16s %s" % (m.first_name,
                                           m.last_name,
                                           m.diet))
            else:
                kids += 1
                print ("%-12s %-16s %s" % (m.first_name,
                                           m.last_name,
                                           m.diet))
        print "Total: %d Adults: %d Children: %d" %(total, adults, kids)
        connection.close()


    @classmethod
    def conditions_m(cls, selection, *args):
        method = getattr(cls, selection)
        total = 0
        adults = 0
        kids = 0
        for m in method(args):
            total += 1
            if m.is_adult():
                adults += 1
                print ("%-12s %-16s %s" % (m.first_name,
                                           m.last_name,
                                           m.conditions))
            else:
                kids += 1
                print ("%-12s %-16s %s" % (m.first_name,
                                           m.last_name,
                                           m.conditions))
        print "Total: %d Adults: %d Children: %d" %(total, adults, kids)
        connection.close()

    @classmethod
    def allergies_m(cls, selection, *args):
        method = getattr(cls, selection)
        total = 0
        adults = 0
        kids = 0
        for m in method(args):
            total += 1
            if m.is_adult():
                adults += 1
                print ("%-12s %-16s %s" % (m.first_name,
                                           m.last_name,
                                           m.allergies))
            else:
                kids += 1
                print ("%-12s %-16s %s" % (m.first_name,
                                           m.last_name,
                                           m.allergies))
        print "Total: %d Adults: %d Children: %d" %(total, adults, kids)
        connection.close()

    @classmethod
    def emails(cls, selection, *args):
        method = getattr(cls, selection)
        total = 0
        adults = 0
        kids = 0
        emails = set()
        for m in method(args):
            total += 1
            #print m
            if m.is_adult():
                adults += 1
                if m.email != '':
                    emails.add(m.email)
            else:
                kids += 1
                if m.carer is not None and m.carer.email != '' :
                    emails.add(m.carer.email)
                if m.carer_2 is not None and m.carer_2.email != '' :
                    emails.add(m.carer_2.email)
        print ", ".join(sorted([str(e).lower() for e in emails]))
#        print "%s " % [e for e in emails]
        print "Total: %d Adults: %d Children: %d" %(total, adults, kids)
        connection.close()


    @classmethod
    def carers(cls, *args):
        return [o for o in cls.objects.all() if o.role not in ["Doctor", "Backup", "Member"]]
    @classmethod
    def dump(cls, *args):
        print args[0]
        return True

    @classmethod
    def current_carers(cls, *args):
        return [o for o in cls.objects.all()
                  if len(o.children.all()) > 0
                     and (o.children.all()[0].status == "Elfin"
                       or (len(o.children.all()) > 1 and o.children.all()[1].status == "Elfin")
                     )
               ]

    @classmethod
    def members_with_status(cls, status):
        return [o for o in cls.objects.all() if o.status == status]

    @classmethod
    def members_with_role(cls, role):
        return [o for o in cls.objects.all() if o.role == role]

    @classmethod
    def unsigned(cls, *args):
        return [o for o in cls.members_with_role('Member') if o.date_signed is None]

    @classmethod
    def elfins(cls, *args):
        return sorted(Member.members_with_status('Elfin'), key=lambda member: member.age_decimal())

    @classmethod
    def woodchips(cls, *args):
        return Member.members_with_status('Woodchip')

    @classmethod
    def waiters(cls, *args):
        return Member.members_with_status('Waiting')

    @classmethod
    def boys(cls, list):
        return [i for i in list if i.gender == 'M']

    @classmethod
    def girls(cls, list):
        return [i for i in list if i.gender == 'F']

    @classmethod
    def attendees(cls, session_names):
        session = Session.objects.get(name=session_names[0][0])
        return [a.member for a in Attendance.objects.filter(session=session)]


def dottedDict(model, name, dict):
    for f in model._meta.fields:
        if type(f) in [models.fields.related.ForeignKey, models.fields.related.OneToOneField]:
            referred = getattr(model, f.name)
            if referred is not None:
                dottedDict(referred, '%s.%s' % (name, f.name), dict)
        else:
            dict['%s.%s' % (name, f.name)] = model.__dict__[f.name]

    try:
        extras = getattr(model, 'extras')
        for m in extras():
            print "Adding: %s.%s = %s" % (name, m.__name__, str(m()))
            if m() is not None:
              dict['%s.%s' % (name, m.__name__)] = m()
    except AttributeError, e:
        print e
        pass

    return dict


class Session(models.Model):
    name = models.CharField(max_length=40, default=str(date.today()))
    start_date = models.DateField(help_text='Format: YYYY-MM-DD',
                                  null=True,
                                  default=date.today())
    end_date = models.DateField(help_text='Format: YYYY-MM-DD',
                                null=True,
                                default=date.today())

    def __unicode__(self):
        return self.name


class CurrencyField(models.DecimalField):
    __metaclass__ = models.SubfieldBase

    def __init__(self, verbose_name=None, name=None, **kwargs):
        super(CurrencyField, self). __init__(
            verbose_name=verbose_name, name=name, max_digits=10,
            decimal_places=2, **kwargs)

    def to_python(self, value):
        try:
            return super(CurrencyField, self).to_python(value).quantize(Decimal("0.01"))
        except AttributeError:
            return None


class Attendance(models.Model):
    session = models.ForeignKey(Session)
    member = models.ForeignKey(Member)
    amount = CurrencyField(default=0)

    def set_member(self, val):
        self.member = val
        return self

    def __unicode__(self):
        return "%s - %s" % (self.session, self.member)

