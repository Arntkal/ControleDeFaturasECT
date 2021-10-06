import re
import time
import pandas as pd

from .models import Tarifa

def DeparaFatura(path_fatura):
    inicio = time.time()
    #path_fatura = f'C:/Users/guilh/Desktop/Rolo do Kujiw/fatura.csv'
    path_fatura = 'ControleTarifaECT/files'+path_fatura
    fatura = open(path_fatura)
    fatura = fatura.readlines()[3:]

    # tratativa de retorno de arquivo no mesmo formato
    pathRetorno = path_fatura[:-4]
    pathRetorno = pathRetorno+"_log.csv"

    arquivo = ''

    for item in fatura:
        item = item.split(';')
        try:  # checa se o primeiro ítem é um numero, assim ignorando prováveis artefatos na tabela
            check = float(item[0])
        except:
            continue
        codigo_ect = item[3]
        codigo_ect = codigo_ect[-4:] # tava vindo cheio de zero na frente, então separa os últimos 4 digitos
        etiqueta = item[10]
        valor = float(re.sub(r'[R$. ]', '', item[7]).replace(',', '.')) # remove R$ e troca decimal ',' por '.')
        valor_declarado = float(re.sub(r'[R$. ]', '', item[11]).replace(',', '.'))
        peso = int(item[6])
        if valor_declarado > 0: # tratativa do valor cobrado quando há valor declarado, para evitar flags indevidos
            valor_add = valor_declarado - 21 #valor padrão para PAC e SEDEX, sujeito à mudanças quando outros serviços
            valor_add = valor_add / 100
            valor_add = round(valor_add, 2) #TODO: ARREDONDAMENTO PADRÃO, ALINHAR COM O KUJIW SE HÁ REGRA
            valor = valor - valor_add
        if peso == 0: # peso zero, ligado à outros serviços. Provavelmente precisa logar ou no mínimo ignorar
            continue
        elif peso > 10000: # se peso >10000 precisa tratar pra cálculo lá na frente
            kg_adicional = peso-10000 # diferença do peso pra cálculo
        else:
            kg_adicional = '-'

        linha = f'{etiqueta};{str(codigo_ect)};{str(peso)};{str(kg_adicional)};{str(valor)};{str(valor_declarado)}\n'

        with open(pathRetorno, 'a') as log:
             log.write(linha)

    fatura = open(pathRetorno)
    fatura = fatura.readlines()

    resultado = '<table class="table table-bordered dataTable" id="dataTable"><thead><tr role="row">'
    resultado = f'{resultado}<th>Etiqueta</th><th>Código ECT</th><th>Peso</th><th>Valor</th><th>Valor Declarado</th><th>Range</th><th>Status</th></tr></thead>'

    path_table = path_fatura[:-4]
    path_table = path_table+'_processado.xlsx'
    
    qtdTotal = 0
    qtdInconsistente = 0
    qtdCodECT = 0
    qtdPeso = 0
    
    for item in fatura:
        qtdTotal += 1
        item = item.split(';')
        etiqueta = item[0]
        peso = int(item[2])
        codigoECT = item[1]
        valor = item[4]
        valor_declarado = item[5]
        if peso > 10000:
            peso_2 = 10000
            raw = f'SELECT * FROM controleTarifaECT_tarifa WHERE idCodigoTarifa_Id = (SELECT id FROM controleTarifaECT_codigotarifa WHERE codigoECT LIKE "%{codigoECT}%") and peso_I <= {peso_2} AND peso_F >= {peso_2}'
        else:
            raw = f'SELECT * FROM controleTarifaECT_tarifa WHERE idCodigoTarifa_Id = (SELECT id FROM controleTarifaECT_codigotarifa WHERE codigoECT LIKE "%{codigoECT}%") and peso_I <= {peso} AND peso_F >= {peso}'
        if len(list(Tarifa.objects.raw(raw))) > 0:
            resultSQL = Tarifa.objects.raw(raw)[0]

            thisdict = {
                'L1': resultSQL.rangeL1,
                'L2': resultSQL.rangeL2,
                'L3': resultSQL.rangeL3,
                'L4': resultSQL.rangeL4,
                'E1': resultSQL.rangeE1,
                'E2': resultSQL.rangeE2,
                'E3': resultSQL.rangeE3,
                'E4': resultSQL.rangeE4,
                'N1': resultSQL.rangeN1,
                'N2': resultSQL.rangeN2,
                'N3': resultSQL.rangeN3,
                'N4': resultSQL.rangeN4,
                'N5': resultSQL.rangeN5,
                'N6': resultSQL.rangeN6,
                'I1': resultSQL.rangeI1,
                'I2': resultSQL.rangeI2,
                'I3': resultSQL.rangeI3,
                'I4': resultSQL.rangeI4,
                'I5': resultSQL.rangeI5,
                'I6': resultSQL.rangeI6,
            }

            valor = str(valor.replace('.', ','))

            try:
                rangeEncontrado = list(thisdict.keys())[list(thisdict.values()).index(valor)]
                status = 'OK'
                cor = '#ffffff'
            except:
                if peso > 10000:
                    rangeEncontrado = 'Peso Excedente'
                    status = 'Validar'
                    cor = '#ffff66'
                    qtdPeso += 1
                else:
                    rangeEncontrado = 'ERRO'
                    status = 'Valor inconsistente'
                    cor = '#ffcccc'
                    qtdInconsistente += 1

        else:
            status = 'Código ECT inexistente/incorreto'
            rangeEncontrado = 'ERRO'
            cor = '#ffcccc'
            qtdCodECT += 1
        
        resultado = f'{resultado}<tr style="background-color: {cor}"><td>{etiqueta}</td><td>{codigoECT}</td><td>{peso}</td><td>{valor}</td><td>{valor_declarado}</td><td>{rangeEncontrado}</td><td>{status}</td></tr>'

    resultado = f'{resultado}</table>'

    table = pd.read_html(resultado)[0]
    table.to_excel(path_table, index=False)
    fim = time.time()
    tempo = round(fim - inicio)
    qtdErros = qtdCodECT+qtdInconsistente+qtdPeso
    resultado2 = '<table class="table table-bordered dataTable" id="dataTable"><thead><tr role="row">'
    resultado2 = f'{resultado2}<th>Objetos Analisados</th><th>Obj. Peso Excedente</th><th>Obj. Valor Inconsistente</th><th>Obj. ECT inexistente</th><th>Todos Erros</th><th>Tempo</th></tr></thead>'
    resultado2 = f'{resultado2}<tr><td>{qtdTotal}</td><td>{qtdPeso}</td><td>{qtdInconsistente}</td><td>{qtdCodECT}</td><td>{qtdErros}</td><td>{tempo} segundos</td></tr>'
    resultado2 = f'{resultado2}</table>'


    resultado = {'resultado': resultado2, 'path_table': path_table}

    return resultado
