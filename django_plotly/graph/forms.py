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

class BinFieldForm(forms.ModelForm):
    class Meta:
        model = BinField
        fields = '__all__'
        widgets = {'bs': forms.HiddenInput()}

    def save(self, commit=True, bf=None):
        if bf is not None: # UPDATE
            bf.label = self.cleaned_data['label']
            bf.bits = self.cleaned_data['bits']
            bf.save()
            obj = bf
        else: # INSERT
            obj = super().save(commit=commit)
        return obj

def get_binstructure_formset(data=None):
    FormSetClass = forms.modelformset_factory(model=BinStructure, exclude=[], 
        can_delete=True, extra=0)
    return FormSetClass(data=data)
        
def get_binfield_formset(srctype='', src=None):
    extra = 0
    data = None
    queryset = BinField.objects.none()
    initial = None

    if srctype == 'formset': # Get formset with an extra form
        bf_formset = src
        bf_formset.full_clean() # To access to form.cleaned_data
        values = []
        for form in bf_formset:
            label = form.cleaned_data.get('label', '') # Permit empty label 
            bits = form.cleaned_data.get('bits')
            id = form.cleaned_data.get('id')
            values.append({'label': label, 'bits': bits, 'id': id})
        initial = values
        extra = len(values) + 1
    elif srctype == 'post': # Get formset from request.POST
        data = src
    elif srctype == 'bs_id': # Get formset belongs to bs_id's BinStructure
        queryset=BinField.objects.filter(bs__id=src)
    else: # Get formset with an empty form
        extra = 1

    # Get formset class from factory
    FormSetClass = forms.modelformset_factory(model=BinField, form=BinFieldForm,
        exclude=[], extra=extra)
    return FormSetClass(data=data, queryset=queryset, initial=initial)

def save_binstructure_binfield_formset(bs_form, bs_id, bf_formset):
    saved = False
    if bs_form.is_valid() and bf_formset.is_valid():
        bs = bs_form.save(bs_id=bs_id)
        for form in bf_formset:
            form.instance.bs = bs
            form.save(bf=form.cleaned_data.get('id'))
            saved = True
    return saved
