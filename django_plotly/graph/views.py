from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
import plotly.express as px
from .bin2real import *
from .forms import *
from .models import *

# Create your views here.
def structure_list(request):
    if request.method == 'POST':
        if 'submit_new' in request.POST:
            response = redirect('field_list')
        elif 'submit_del' in request.POST:
            response = _del_structure(request)
        else:
            response = HttpResponse('Undefined')
    else:
        bs_formset = get_binstructure_formset()
        response = render(request, 'graph/structure.html', {'bs_formset': bs_formset})
    return response

def _del_structure(request):
    bs_formset = get_binstructure_formset(data=request.POST)
    bs_formset.full_clean() # To access to form.cleaned_data
    for form in bs_formset:
        if form.cleaned_data['DELETE']:
            bs = form.save(commit=False)
            bs.delete()
    return HttpResponse('Del')

def field_list(request, bs_id=None):
    if request.method == 'POST':
        if 'submit_add' in request.POST:
            response = _append_field_form(request)
        elif 'submit_save' in request.POST:
            response = _save_field_formset(request, bs_id)
        else:
            response = HttpResponse('Undefined')
    else:
        if bs_id is not None: # Field list for the BinStructure(bs_id)
            bs = get_object_or_404(BinStructure, pk=bs_id)
            bs_form = BinStructureForm(instance=bs)
            bf_formset = get_binfield_from_binstructure(bs_id)
        else: # Empty field list
            bs_form = BinStructureForm()
            bf_formset = get_binfield_formset()
        response = render(request, 'graph/field.html', {'bs_form': bs_form, 'bf_formset': bf_formset})
    return response

def _append_field_form(request):

    # Keep current name and fields, then append one more extra field
    bs_form = BinStructureForm(data=request.POST)
    bf_formset = get_binfield_formset(data=request.POST)
    bf_formset.full_clean() # To access to form.cleaned_data
    values = []
    for form in bf_formset:
        bs = form.cleaned_data.get('bs')
        label = form.cleaned_data.get('label', '')
        bits = form.cleaned_data.get('bits')
        id = form.cleaned_data.get('id')
        values.append({'bs': bs, 'label': label, 'bits': bits, 'id': id})
    new_bf_formset = get_binfield_formset(initial=values, extra=len(values) + 1)
    
    return render(request, 'graph/field.html', {'bs_form': bs_form, 'bf_formset': new_bf_formset})

def _save_field_formset(request, bs_id):
    bs_form = BinStructureForm(data=request.POST)
    bf_formset = get_binfield_formset(data=request.POST)
    if bs_form.is_valid() and bf_formset.is_valid():
        bs = bs_form.save(bs_id=bs_id)
        for form in bf_formset:
            form.instance.bs = bs
            form.save(bf=form.cleaned_data.get('id'))
        response = HttpResponse('Saved')
    else:
        response = HttpResponse('Invalid')
    return response

def plot(request):
    if request.method == 'POST':
        sel_bs = SelectBinStructureForm(data=request.POST)
        if sel_bs.is_valid():

            # Make binary structure from the selected BinStructure
            cbs = CustomBinStructure()
            bs_name = sel_bs.cleaned_data['bs']
            bfs = BinField.objects.filter(bs__name=bs_name)
            for bf in bfs:
               cbs.append_field(bf.label, bf.bits) 
            cbs.make_binstructure()

            # Read a sample file
            cbs_dict = cbs.read_bin_to_dict('graph/sample.bin')

            # Plot
            fig = px.scatter(x=cbs_dict['use22bits'], y=cbs_dict['use2bits'])
            plot_div = fig.to_html(full_html=False)
            response = render(request, 'graph/plot.html', {'plot_div': plot_div})
        else:
            response = HttpResponse('post')
    else:
        sel_bs = SelectBinStructureForm()
        response = render(request, 'graph/plot.html', {'sel_bs': sel_bs})
    return response
