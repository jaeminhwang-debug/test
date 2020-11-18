from django.shortcuts import render
from django.http import HttpResponse
import plotly.express as px
from .bin2real import CustomBinStructure
from .forms import get_binfield_formset

# Create your views here.
def define_structure(request):
    if request.method == 'POST':
        if 'submit_add' in request.POST:
            response = _append_form(request)
        elif 'submit_save' in request.POST:
            response = _save_formset(request)
        else:
            response = HttpResponse('Undefined')
    else:
        formset = get_binfield_formset()
        response = render(request, 'graph/define_structure.html', {'formset': formset})
    return response

def _append_form(request):
    formset = get_binfield_formset(data=request.POST)
    if formset.is_valid():

        # Keep values from current forms
        values = []
        for form in formset:
            try:
                values.append({'label': form.cleaned_data['label'],
                               'bits': form.cleaned_data['bits']})
            except KeyError:
                values.append({'label': '', 'bits': None})

        # Get a new formset which have one more extra form
        new_formset = get_binfield_formset(initial=values, extra=len(values) + 1)
    else:
        new_formset = formset
    return render(request, 'graph/define_structure.html', {'formset': new_formset})

def _save_formset(request):
    formset = get_binfield_formset(data=request.POST)
    formset.save()
    return HttpResponse('Save')

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
