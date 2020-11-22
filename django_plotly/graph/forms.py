from django import forms
from .models import *

def get_binstructure_formset():
    FormSetClass = forms.modelformset_factory(model=BinStructure, exclude=[], can_delete=True, extra=0)
    return FormSetClass()

def get_binfield_formset(data=None, initial=None, empty=True, extra=1):
    FormSetClass = forms.modelformset_factory(model=BinField, exclude=['bs'], extra=extra)
    if empty:
        return FormSetClass(data=data, queryset=BinField.objects.none(), initial=initial)
    else:
        return FormSetClass(data=data, initial=initial)
        
def get_binfield_from_binstructure(bs_id):
    FormSetClass = forms.modelformset_factory(model=BinField, exclude=['bs'], extra=0)
    return FormSetClass(queryset=BinField.objects.filter(bs__id=bs_id))

class BinStructureForm(forms.ModelForm):
    class Meta:
        model = BinStructure
        fields = ['name']

class SelectBinStructureForm(forms.Form):
    bs = forms.ModelChoiceField(queryset=BinStructure.objects.all(), 
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))
