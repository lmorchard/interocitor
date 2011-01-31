from django import forms

from .models import Entry

from django.utils.translation import ugettext_lazy as _


class MyModelForm(forms.ModelForm):
    pass


class MyForm(forms.Form):
    pass


class EntryEditForm(MyModelForm):
    """Form accepting demo Entrys"""

    class Meta:
        model = Entry
        fields = (
            'title', 'link', 'tags', 'summary', 'content',
        )


class EntryNewForm(EntryEditForm):

    class Meta(EntryEditForm.Meta):
        pass
        #fields = EntryEditForm.Meta.fields + ( 'captcha', 'accept_terms', )

