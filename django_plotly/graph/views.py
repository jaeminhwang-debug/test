import os
import ast
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .bin2real import *
from .forms import *
from .models import *

# Create your views here.
def main(request):
    return render(request, 'graph/main.html')

def binstruct_list(request):
    if request.method == 'POST':
        if 'submit_new' in request.POST:
            response = redirect('binfield_list')
        elif 'submit_del' in request.POST:
            response = _delete_binstruct(request)
        else:
            raise Http404('Undefined')
    else:
        bs_fs = get_binstruct_formset()
        response = render(request, 'graph/binstruct.html', {'bs_fs': bs_fs})
    return response

def _delete_binstruct(request):
    bs_fs = get_binstruct_formset(request.POST)
    delete_binstruct_formset(bs_fs)
    return HttpResponseRedirect(request.path_info)

def binfield_list(request, bs_id=None):
    if request.method == 'POST':
        if 'submit_add' in request.POST:
            response = _append_binfield_form(request)
        elif 'submit_del' in request.POST:
            response = _delete_binfield_form(request)
        elif 'submit_save' in request.POST:
            response = _save_binfield_formset(request, bs_id)
        else:
            raise Http404('Undefined')
    else:
        if bs_id is not None: # Field list for the BinStruct(bs_id)
            bs = get_object_or_404(BinStruct, pk=bs_id)
            bs_form = BinStructForm(instance=bs)
            bf_fs = get_binfield_formset('bs_id', bs_id)
        else: # Empty field list
            bs_form = BinStructForm()
            bf_fs = get_binfield_formset()
        response = render(request, 'graph/binfield.html', {'bs_form': bs_form, 'bf_fs': bf_fs})
    return response

def _append_binfield_form(request):
    bs_form = BinStructForm(request.POST)
    bf_fs = get_binfield_formset('post', request.POST)
    bf_fs = get_binfield_formset('formset_append', bf_fs)
    return render(request, 'graph/binfield.html', {'bs_form': bs_form, 'bf_fs': bf_fs})

def _delete_binfield_form(request):
    bs_form = BinStructForm(request.POST)
    bf_fs = get_binfield_formset('post', request.POST)
    bf_fs = get_binfield_formset('formset_delete', bf_fs)
    return render(request, 'graph/binfield.html', {'bs_form': bs_form, 'bf_fs': bf_fs})

def _save_binfield_formset(request, bs_id):
    bs_form = BinStructForm(request.POST)
    bf_fs = get_binfield_formset('post', request.POST)
    saved = save_binstruct_binfield_formset(bs_form, bs_id, bf_fs)
    if saved:
        response = redirect('binstruct_list')
    else:
        response = response = render(request, 'graph/error.html', {'msgs': ['Failed to save.']})
    return response

def bindata_list(request):
    if request.method == 'POST':
        if 'submit_up' in request.POST:
            response = _upload_files(request)
        elif 'submit_del' in request.POST:
            response = _delete_files(request)
        else:
            raise Http404('Undefined')
    else:
        bd_fs = get_bindata_formset()
        file_form = FileForm()
        response = render(request, 'graph/bindata.html', {'bd_fs': bd_fs, 'file_form': file_form})
    return response

def _upload_files(request):
    form = FileForm(request.POST, request.FILES)
    err_msgs = save_fileform(form)
    if len(err_msgs) == 0:
        response = HttpResponseRedirect(request.path_info)
    else:
        response = render(request, 'graph/error.html', {'msgs': err_msgs})
    return response

def _delete_files(request):
    bd_fs = get_bindata_formset(request.POST)
    delete_bindata_formset(bd_fs)
    return HttpResponseRedirect(request.path_info)

def bindata_download(request, y, m, d, n):
    fpath = make_bindata_path(y, m, d, n)
    if os.path.exists(fpath):
        with open(fpath, 'rb') as f:
            response = HttpResponse(f.read())
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(fpath)
    else:
        response = render(request, 'graph/error.html', {'msgs': ['File does not exist.']})
    return response

def plot(request):
    sel_bd = None
    sel_bs = None
    sel_graph = None
    sel_bf_forms = None
    graph_opt = None
    plot_div = None

    if request.method == 'POST':
        sel_bd = SelectBinDataForm(request.POST)
        sel_bs = SelectBinStructForm(request.POST)
        sel_graph = SelectGraphForm(request.POST)
        graph_opt = GraphOption(request.POST)
        if sel_bs.is_valid() and sel_graph.is_valid():
            bs = sel_bs.cleaned_data.get('bs')
            graph_id = ast.literal_eval(sel_graph.cleaned_data.get('graph'))
            sel_bf_forms, sel_bf_ids = get_select_binfield_forms(
                bs, SelectGraphForm.get_required_num(graph_id), request.POST.getlist('bf'))
            plot_div = None
            if sel_bd.is_valid() and 'submit_plot' in request.POST:
                plot_div = get_plotly_html(
                    bs,
                    SelectGraphForm.get_id_str(graph_id),
                    sel_bf_ids,
                    get_bindata_path(sel_bd.cleaned_data.get('bd')),
                    graph_opt)
    else:
        sel_bd = SelectBinDataForm()
        sel_bs = SelectBinStructForm()
        sel_graph = SelectGraphForm()
        graph_opt = GraphOption()
        
    response = render(request, 'graph/plot.html', 
        {'sel_bd': sel_bd, 'sel_bs': sel_bs, 
         'sel_graph': sel_graph, 'sel_bf_forms': sel_bf_forms, 'plot_div': plot_div,
         'graph_opt': graph_opt})

    return response

def get_plotly_html(bs, graph_id_str, bf_ids, fpath, graph_opt):
    div = None

    # Make binary structure from the selected BinStruct
    cbs = CustomBinStruct()
    bfs = BinField.objects.filter(bs=bs)
    for bf in bfs:
        cbs.append_binfield(bf.label, bf.bits)
    cbs.make_binstruct()

    # Read the selected file
    data = cbs.read_bin_to_dict(fpath)
    df = pd.DataFrame.from_dict(data)

    # Get field fields from the bf_ids
    fls = []
    for bf_id in bf_ids:
        fls.append(get_binfield_label(bf_id))

    # Plot
    fig = None
    if graph_id_str == SelectGraphForm.SCATTER:
        fig = px.scatter(data_frame=df, x=fls[0], y=fls[1])
    elif graph_id_str == SelectGraphForm.SCATTER_3D:
        d = go.Scatter3d(x=data[fls[0]], y=data[fls[1]], z=data[fls[2]], mode='markers',
            marker=dict(size=2))
        fig = go.Figure(d)
        fig.update_layout(scene=dict(xaxis_title=fls[0], yaxis_title=fls[1], zaxis_title=fls[2]))
    elif graph_id_str == SelectGraphForm.LINE:
        fig = px.line(data_frame=df, x=fls[0], y=fls[1])
    elif graph_id_str == SelectGraphForm.LINE_3D:
        fig = px.line_3d(data_frame=df, x=fls[0], y=fls[1], z=fls[2])
    
    if fig:
        fig.update_layout(width=graph_opt.get('width'), height=graph_opt.get('height'))
        div = fig.to_html(full_html=False)
    return div
