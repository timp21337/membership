import floppyforms as forms
import app
from members.models import Session


class LookupField(forms.CharField):
    """
    A Django Form field which appears to the user as a charfield,
    but when the form is submitted, the given string is used as
    a lookup on the primary key of a given Model, and that model
    instance is subsequently returned.
    """

    def __init__(self, *args, **kwargs):
        self.Model = kwargs.pop('model', None)
        super(forms.Field, self).__init__(*args, **kwargs)

    def to_python(self, value):
        try:
            return self.Model.objects.get(pk=value)
        except self.Model.DoesNotExist, e:
            return unicode(value)

    def validate(self, value):
        if isinstance(value, basestring):
            raise forms.ValidationError("'%s' could not be found" % value)



class PasswordWriteForm(forms.Form):
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(render_value=False),
                               label='A pass phrase')
    password2 = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(render_value=False),
                                label='Repeated pass phrase')

    def clean(self):
        if self.cleaned_data.get('password') != self.cleaned_data.get('password2'):
            raise forms.ValidationError('Pass phrases do not match')
        try:
            app.checkPasswordCompliance(self.cleaned_data.get('password'))
        except StandardError, e:
            raise forms.ValidationError(e)
        return self.cleaned_data


class UserWriteForm(PasswordWriteForm):
    isManager = forms.BooleanField(label='Is a manager', required=False)

    def __init__(self, *args, **kwargs):
        username = forms.CharField(max_length=100, required=True, label='Username')
        PasswordWriteForm.__init__(self, *args, **kwargs)
        self.fields.insert(0, 'username', username)

    class Meta:
        fields = (
            'username',
            'password',
            'password2',
            'isManager'
        )

    def save(self):
        return self.cleaned_data


class AuthenticationForm(forms.Form):
    username = forms.CharField(max_length=100, required=True, label='Username')
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput(render_value=False),
                               label='Pass phrase')


class SessionChoiceForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Session.objects.all(), required=True, empty_label=None, label='Session')
