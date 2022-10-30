from pdfquery import pdfquery
import json
import re

pdf = pdfquery.PDFQuery("contas/light_modelo_5_3.pdf")
pdf.load()

# Buscar localização de itens da fatura
x0 = 35
x1 = 459
base = pdf.pq('LTTextLineHorizontal:contains("Itens de fatura")')
base_bottom_top = float(base.attr('y0'))
bottom_corner = round(base_bottom_top - 165, 3)
top_corner = round(base_bottom_top, 3)


def transform_number(x):
    """ Pega o valor de entrada e deixa apenas os numeros em int ou float """
    if not x:
        return
    x = re.sub(r'[^0-9\,]', '', x)
    x = re.sub(r':|,', '.', x)
    if "." in x:
        return float(x)
    else:
        return int(x)


def search(expression_re, box):
    """ função de busca onde dentro de um box ela acha uma expressão regex """
    valor = re.search(expression_re, box)
    return valor


def location(x0, y0, x1, y1):
    """ função de localização espacial pdf"""
    return pdf.pq('LTTextLineHorizontal:overlaps_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1))


def location_in(x0, y0, x1, y1):
    """ função de localização espacial pdf dentro do box  """
    return pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1))


# encontrando primeiro item dentro do box de itens da fatura
box = location_in(x0, bottom_corner, x1, top_corner)
busca = search(r'\w.{20}', box.text()).group()
start = pdf.pq('LTTextLineHorizontal:contains("%s")' % busca)
start_top = round(float(start.attr('y1')), 3)
start_bottom = round(float(start.attr('y0')), 3)

# buscando itens andando linha a linha
verify_count = start_top - start_bottom
count = 7.5
if verify_count < 6.9:
    count = 7.25
items = {}


while start_bottom > bottom_corner:
    titulo = location_in(x0, start_bottom, 198, start_top).text()
    unid = location_in(180, start_bottom, 230, start_top).text()
    quant = location_in(210, start_bottom, 270, start_top).text()
    preco_unitario = location_in(240, start_bottom, 300, start_top).text()
    valor = location_in(290, start_bottom, 340, start_top).text()
    pis_cofins = location_in(320, start_bottom, 360, start_top).text()
    calc_icms = location_in(340, start_bottom, 390, start_top).text()
    aliquota_icms = location_in(380, start_bottom, 415, start_top).text()
    icms_valor = location_in(405, start_bottom, 440, start_top).text()
    tarifa_unit = location_in(420, start_bottom, x1, start_top).text()
    if titulo:
        items[titulo] = {
            "unidade": unid,
            "quantidade": transform_number(quant),
            "preco_unitario": transform_number(preco_unitario),
            "valor": transform_number(valor),
            "pis_cofins": transform_number(pis_cofins),
            "calculo_icms": transform_number(calc_icms),
            "aliquota_icms": transform_number(aliquota_icms),
            "icms_valor": transform_number(icms_valor),
            "tarifa_unitaria": transform_number(tarifa_unit)
        }
        items[titulo] = {key: value for key, value in items[titulo].items() if value is not None and value != ""}
    start_bottom = round(start_bottom - count, 3)
    start_top = round(start_top - count, 3)

# salvando os itens em Json
items_object= json.dumps(items, indent=4, ensure_ascii=False)
with open('jsons/array.json', 'w') as array:
    array.write(items_object)