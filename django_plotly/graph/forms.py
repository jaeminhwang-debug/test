from django.forms import Form, BaseFormSet, formset_factory
from django.forms import CharField, IntegerField
from django.core.exceptions import ValidationError

class CustomFieldForm(Form):
    field_name = CharField(required=False)
    bits = IntegerField(min_value=1, max_value=64)

class BaseCustomFieldFormSet(BaseFormSet):
    def clean(self):
        if any(self.errors):
            return
        field_names = []
        for form in self.forms:
            field_name = form.cleaned_data.get('field_name')
            if field_name in field_names:
                raise ValidationError('Field name must be unique')
            field_names.append(field_name)

def get_custom_field_formset():
    return formset_factory(CustomFieldForm, formset=BaseCustomFieldFormSet)
