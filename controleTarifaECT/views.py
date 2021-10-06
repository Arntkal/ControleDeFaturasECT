from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.storage import default_storage
from .form import UploadFileForm, testForm
from .depara_fatura import DeparaFatura
from .models import Tarifa


# Create your views here.
@staff_member_required
def index(request):
    template = loader.get_template('base/base-menu.html')
    context = {'context' : 'hello'}
    return HttpResponse(template.render(context, request))
    
@staff_member_required
def table(request):
    template = loader.get_template('base/table.html')
    context = {'NO' : 'hello'}
    return HttpResponse(template.render(context, request))
    
@staff_member_required
def getFile(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            #pathFile = './ControleTarifaECT/files/'+file.name
            pathFile = file.name
            file_name = default_storage.save(pathFile, file)
            #  Reading file from storage
            file = default_storage.open(file_name)
            file_url = default_storage.url(file_name)
            depara = DeparaFatura(file_url)
            # resultado = open(depara, 'r').read()
            # resultado = resultado.replace('\n', '<br>')
            depara_html = depara['resultado']
            depara_link = depara['path_table']
            depara_link = depara_link.replace('ControleTarifaECT/files/', '')
            resultado = f"<div style='width:140px;margin:0 auto;'><a href='{depara_link}' class='btn btn-primary'>Baixar Planilha</a></div><br>{depara_html}"
            template = loader.get_template('base/base-menu.html')
            context = {'context' : 'Resultado: <br><br>' +resultado}
            return HttpResponse(template.render(context, request))
    else:
        form = UploadFileForm()
    return render(request, 'base/form.html', {'form': form})
    
@staff_member_required
def formDeTest(request):
    if request.method == 'POST':
        form = testForm(request.POST)
        if form.is_valid():
            peso = request.POST['peso']
            codigoECT = request.POST['codigoECT']
            raw = f'SELECT * FROM controleTarifaECT_tarifa WHERE idCodigoTarifa_Id = (SELECT id FROM controleTarifaECT_codigotarifa WHERE codigoECT LIKE "%{codigoECT}%") and peso_I <= {peso} AND peso_F >= {peso}'
            if len(list(Tarifa.objects.raw(raw))) > 0:
                resultSQL = Tarifa.objects.raw(raw)[0]
                resultado = f"Código : {codigoECT} <br>"
                resultado = f"{resultado}Peso informado: {peso} <br>"
                resultado = f"{resultado}Peso entre: {resultSQL.peso_I} a {resultSQL.peso_F}<br>"    
                resultado = f"{resultado}L1: {resultSQL.rangeL1}<br>"
                resultado = f"{resultado}L2: {resultSQL.rangeL2}<br>"
                resultado = f"{resultado}L3: {resultSQL.rangeL3}<br>"
                resultado = f"{resultado}L4: {resultSQL.rangeL4}<br>"
                resultado = f"{resultado}E1: {resultSQL.rangeE1}<br>"
                resultado = f"{resultado}E2: {resultSQL.rangeE2}<br>"
                resultado = f"{resultado}E3: {resultSQL.rangeE3}<br>"
                resultado = f"{resultado}E4: {resultSQL.rangeE4}<br>"
                resultado = f"{resultado}N1: {resultSQL.rangeN1}<br>"
                resultado = f"{resultado}N2: {resultSQL.rangeN2}<br>"
                resultado = f"{resultado}N3: {resultSQL.rangeN3}<br>"
                resultado = f"{resultado}N4: {resultSQL.rangeN4}<br>"
                resultado = f"{resultado}N5: {resultSQL.rangeN5}<br>"
                resultado = f"{resultado}N6: {resultSQL.rangeN6}<br>"
                resultado = f"{resultado}I1: {resultSQL.rangeI1}<br>"
                resultado = f"{resultado}I2: {resultSQL.rangeI2}<br>"
                resultado = f"{resultado}I3: {resultSQL.rangeI3}<br>"
                resultado = f"{resultado}I4: {resultSQL.rangeI4}<br>"
                resultado = f"{resultado}I5: {resultSQL.rangeI5}<br>"
                resultado = f"{resultado}I6: {resultSQL.rangeI6}"
            else:
                resultado = "Valores não encontrados no sistema"
            template = loader.get_template('base/base-menu.html')
            context = {'context' : 'Resultado: <br><br>' +resultado}
            return HttpResponse(template.render(context, request))
    else:
        form = testForm()
    return render(request, 'base/form-2.html', {'form': form})
    

#SELECT * FROM controleTarifaECT_tarifa WHERE idCodigoTarifa_Id = (SELECT id FROM controleTarifaECT_codigotarifa WHERE codigoECT LIKE "%04677%") and peso_I < 524 AND peso_F > 524    