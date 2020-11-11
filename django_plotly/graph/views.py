from django.shortcuts import render
from . import bin2real
import plotly.express as px

from ctypes import LittleEndianStructure, c_uint, c_ushort
class SampleBin(LittleEndianStructure):
    """
    Define your structure here
    """
    _fields_ = [
        ('use22bits', c_uint, 22),
        ('use10bits', c_uint, 10),

        ('', c_ushort, 7),
        ('use2bits', c_ushort, 2),
        ('', c_ushort, 4),
        ('use3bits', c_ushort, 3),
    ]

# Create your views here.
def plot(request):
    sts = bin2real.read_bin_dict('graph/sample.bin', 6, SampleBin)
    fig = px.scatter(x=sts['use22bits'], y=sts['use2bits'])
    plot_dev = fig.to_html(full_html=False)
    return render(request, 'graph/plot.html', {'plot_dev': plot_dev})
