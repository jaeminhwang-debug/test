from django.shortcuts import render
import plotly.express as px
from .bin2real import CustomBinStructure
from .forms import get_custom_field_formset

# Create your views here.
def define_structure(request):
    if request.method == 'POST' and 'submit_add' in request.POST:
        formset = _append_form(request)
    else:
        CustomFieldFormSet = get_custom_field_formset()
        formset = CustomFieldFormSet()
    return render(request, 'graph/define_structure.html', {'formset': formset})

def _append_form(request):
    CustomFieldFormSet = get_custom_field_formset()
    prev_formset = CustomFieldFormSet(request.POST)
    prev_values = []
    if prev_formset.is_valid():
        print('valid')
        for prev_form in prev_formset:
            try:
                prev_values.append({
                    'field_name': prev_form.cleaned_data['field_name'],
                    'bits': prev_form.cleaned_data['bits']})
            except KeyError:
                prev_values.append({'field_name': '', 'bits': None})
        formset = CustomFieldFormSet(initial=prev_values)
    else:
        print(prev_formset.errors)
        formset = prev_formset
    return formset

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
