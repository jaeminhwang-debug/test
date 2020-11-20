from django.shortcuts import render, redirect
from django.http import HttpResponse
import plotly.express as px
from .bin2real import *
from .forms import *

# Create your views here.
def structure_list(request):
    if request.method == 'POST':
        if 'submit_new' in request.POST:
            response = redirect('field_list')
        else:
            response = HttpResponse('Undefined')
    else:
        bs_formset = get_binstructure_formset()
        response = render(request, 'graph/structure.html', {'bs_formset': bs_formset})
    return response

def field_list(request):
    if request.method == 'POST':
        if 'submit_add' in request.POST:
            response = _append_field_form(request)
        elif 'submit_save' in request.POST:
            response = _save_field_formset(request)
        else:
            response = HttpResponse('Undefined')
    else:
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
        try:
            label = form.cleaned_data['label']
        except KeyError:
            label = ''
        try:
            bits = form.cleaned_data['bits']
        except KeyError:
            bits = None
        values.append({'label': label, 'bits': bits})
    new_bf_formset = get_binfield_formset(initial=values, extra=len(values) + 1)
    
    return render(request, 'graph/field.html', {'bs_form': bs_form, 'bf_formset': new_bf_formset})

def _save_field_formset(request):
    bs_form = BinStructureForm(data=request.POST)
    if bs_form.is_valid():
        bf_formset = get_binfield_formset(data=request.POST)
        if bf_formset.is_valid():
            model = bs_form.save()
            for form in bf_formset:
                form.instance.bin_structure = model
            bf_formset.save()
    return HttpResponse('Saved')

def plot(request):

    # Make binary structure
    bs = CustomBinStructure()
    bs.append_field('use22bits', 22)
    bs.append_field('use10bits', 10)
    bs.append_field('', 7)
    bs.append_field('use2bits', 2)
    bs.append_field('', 4)
    bs.append_field('use3bits', 3)
    bs.make_binstructure()

    # Read sample file
    bs_dict = bs.read_bin_to_dict('graph/sample.bin')

    # Plot
    fig = px.scatter(x=bs_dict['use22bits'], y=bs_dict['use2bits'])
    plot_div = fig.to_html(full_html=False)
    return render(request, 'graph/plot.html', {'plot_div': plot_div})
