from django.forms import modelformset_factory
from .models import BinField

def get_binfield_formset(data=None, initial=None, empty=True, extra=1):
    FormSetClass = modelformset_factory(model=BinField, exclude=[], extra=extra)
    if empty:
        return FormSetClass(data=data, queryset=BinField.objects.none(), initial=initial)
    else:
        return FormSetClass(data=data, initial=initial)
