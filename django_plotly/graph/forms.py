from django.forms import modelformset_factory, ModelForm
from .models import BinStructure, BinField

def get_binstructure_formset():
    FormSetClass = modelformset_factory(model=BinStructure, exclude=[], can_delete=True, extra=0)
    return FormSetClass()

def get_binfield_formset(data=None, initial=None, empty=True, extra=1):
    FormSetClass = modelformset_factory(model=BinField, exclude=['bin_structure'], extra=extra)
    if empty:
        return FormSetClass(data=data, queryset=BinField.objects.none(), initial=initial)
    else:
        return FormSetClass(data=data, initial=initial)

class BinStructureForm(ModelForm):
    class Meta:
        model = BinStructure
        fields = ['name']
