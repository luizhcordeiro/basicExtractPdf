"""


"""
from pdfquery import pdfquery
import json
import re

pdf = pdfquery.PDFQuery("contas/light_modelo_5_3.pdf")
pdf.load()
# expressões regex uteis
data_search = r'\d{2}/\d{2}/\d{4}'
value_seach = r'\d{1,3}(\.\d{3})*,\d{2}'


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

def transform_date(x):
    """ separa os valores de datas em ['d', 'm', 'a'] """
    x = x.split('/')
    return x


def location_in(x0, y0, x1, y1):
    return pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1)).text()


def search(expression_re, box):
    """ Busca uma expressão regex em um determinado box """
    valor = re.search(expression_re, box)
    return valor.group()

header_information = pdf.extract([
    ('with_formatter', lambda match: match.text()),
    ('classification', 'LTTextLineHorizontal:in_bbox("40, 730, 200, 765")'),
    ('type_supply', 'LTTextLineHorizontal:in_bbox("190, 733.815, 237.870, 759.595")'),
    ("reference_date", 'LTTextLineHorizontal:in_bbox("53.050, 610.880, 96.960, 633.780")'),

    ('with_parent', 'LTTextLineHorizontal:in_bbox("42.500, 621.880, 194.589, 732.714")'),
    ("name", 'LTTextLineHorizontal:in_bbox("40, 713.844, 200, 732.714")'),  # buscar pela fonte (?)
    ("address", 'LTTextLineHorizontal:in_bbox("40, 676.351, 200, 693.793")'), # buscar entre CEP e name
    ('with_formatter', lambda match: transform_number(match.text())),
    ("CEP", 'LTTextLineHorizontal:contains("CEP")'),
    ("document", 'LTTextLineHorizontal:contains("CNPJ")'),
    ("conta_contrato", 'LTTextLineHorizontal:contains(" Contrato:")'),
    ('with_parent', None),
    ("installation_code", 'LTTextLineHorizontal:in_bbox("207.550, 700, 262.594, 724.613")'),
    ("client_code", 'LTTextLineHorizontal:in_bbox("204.500, 660, 265.660, 686.663")'),
    ("days_reading", 'LTTextLineHorizontal:in_bbox("441.350, 700.987, 471.358, 741.391")'),
    ("total_amount_payable", 'LTTextLineHorizontal:in_bbox("188.100, 610.880, 250.920, 633.780")'),
    ('with_formatter', lambda match: transform_date(match.text())),
    ("due_date", 'LTTextLineHorizontal:in_bbox("110.850, 610.880, 160.890, 633.780")'),
    ("previous_reading", 'LTTextLineHorizontal:in_bbox("321.700, 700.987, 366.736, 741.391")'),
    ("current_reading", 'LTTextLineHorizontal:in_bbox("382.650, 700.987, 427.686, 741.391")'),
    ("next_reading", 'LTTextLineHorizontal:in_bbox("491.800, 700.987, 536.836, 741.697")'),
])


# Apenas pega o primeiro valor que encontra, ainda não especifico, pois não encontrei paridadades
box = pdf.pq('LTTextLineHorizontal:in_bbox("40, 60, 540, 225")').text()
invoice_total = transform_number(search(value_seach, box))

footer_information = {
    "due_date_footer": transform_date(search(data_search, box)),
    "invoice_total": "",
    "withheld_taxes": "",
    "total_amount_payable_footer": ""
}


header_object = json.dumps(header_information, indent=4, ensure_ascii=False, default=str)
footer_object = json.dumps(footer_information, indent=4, ensure_ascii=False)
with open('jsons/test.json', 'w') as conta:
    conta.write(
       "{\n" +
       f'"header" : {header_object}, '
       f'"footer":{footer_object} ' +
       "\n}")
