from django import forms
from .models import *

class BinStructureForm(forms.ModelForm):
    class Meta:
        model = BinStructure
        fields = '__all__'

    def save(self, commit=True, bs_id=None):
        if bs_id is not None: # UPDATE
            bs = BinStructure.objects.get(id=bs_id)
            bs.name = self.cleaned_data['name']
            bs.save()
            obj = bs
        else: # INSERT
            obj = super().save(commit=commit)
        return obj

class SelectBinStructureForm(forms.Form):
    bs = forms.ModelChoiceField(queryset=BinStructure.objects.all(), 
        widget=forms.Select(attrs={'onchange': 'this.form.submit();'}))

def get_binstructure_formset(data=None):
    FormSetClass = forms.modelformset_factory(model=BinStructure, exclude=[], 
        can_delete=True, extra=0)
    return FormSetClass(data=data)

class TestModelForm(forms.ModelForm):
    class Meta:
        model = BinField
        fields = '__all__'

    def save(self, commit=True, bf=None):
        if bf is not None: # UPDATE
            bf.label = self.cleaned_data['label']
            bf.bits = self.cleaned_data['bits']
            bf.save()
            obj = bf
        else: # INSERT
            obj = super().save(commit=commit)
        return obj

def get_binfield_formset(data=None, initial=None, extra=1):
    FormSetClass = forms.modelformset_factory(model=BinField, form=TestModelForm,
        exclude=[], extra=extra)
    return FormSetClass(data=data, queryset=BinField.objects.none(), initial=initial)
        
def get_binfield_from_binstructure(bs_id):
    FormSetClass = forms.modelformset_factory(model=BinField, exclude=[], extra=0)
    return FormSetClass(queryset=BinField.objects.filter(bs__id=bs_id))
