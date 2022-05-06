from django import forms
from django.core.validators import validate_email


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()

# Validators
class MutiEmailField(forms.Field):
    def to_python(self, value):
        if not value:
            return []
        return value.split(',')

    def validate(self, value) :
        super(MutiEmailField, self).validate(value)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    sender = forms.EmailField()
    recipients = MutiEmailField()
    cc_myself = forms.BooleanField(required=False)

    def clean_recipient(self):
        data = self.cleaned_data['recipients']
        if 'sample@gmail.com' not in data:
            raise forms.ValidationError('you have forgetten about sample')

        return data

    def clean(self):
        cleaned_data = super(ContactForm, self).clean()
        cc_myself = cleaned_data.get('cc_myself')
        subject = cleaned_data.get('subject')

        if cc_myself and subject:
            if 'help' not in subject:
                raise forms.ValidationError("Did not send for 'help' in the subject despite 'CC' in yor self")

