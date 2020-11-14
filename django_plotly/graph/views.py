from django.shortcuts import render
import plotly.express as px
from . import bin2real

# Create your views here.
def plot(request):

    # Make binary structure
    bs = bin2real.CustomBinStructure()
    bs.add_field('use22bits', 22)
    bs.add_field('use10bits', 10)
    bs.add_field('', 7)
    bs.add_field('use2bits', 2)
    bs.add_field('', 4)
    bs.add_field('use3bits', 3)
    bs.make_binstructure()

    # Read sample file
    sts = bs.read_bin_to_dict('graph/sample.bin')

    # Plot
    fig = px.scatter(x=sts['use22bits'], y=sts['use2bits'])
    plot_div = fig.to_html(full_html=False)
    return render(request, 'graph/plot.html', {'plot_div': plot_div})
