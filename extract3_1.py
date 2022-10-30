"""
Funciopnando em todos (menos no footer e em endereço/nome da 1 e 2)

1. usei busca por palavra chave

2. Limitei a região de busca pra evitar repetições

Obs. Apaguei a array já que não vou mudar agora e a parte de pagamento pq só tem na versão 3( posteiormente
volto ela com algum IF ou try
"""
from pdfquery import pdfquery
import json
import re

pdf = pdfquery.PDFQuery("contas/light_modelo_5_2.pdf")
pdf.load()
# pdf.tree.write("xmls/conta2.xml", pretty_print=True, encoding="utf-8")


def transform_number(x):
    if not x:
        return
    x = re.sub(r'[^0-9\,]', '', x)
    x = re.sub(r':|,', '.', x)
    if "." in x:
        return float(x)
    else:
        return int(x)


def transform_date(x):
    x = x.split('/')
    return x


def location_in(x0, y0, x1, y1):
    return pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1)).text()


def search_items(x0, y0, x1, y1, bottom_total, counter=7.25):
    items = []
    left = x0
    bottom = y0
    right = x1
    top = y1

    while bottom > bottom_total:
        items.append(location_in(left, bottom, right, top))
        bottom = round(bottom - counter, 3)
        top = round(top - counter, 3)

    return items


header_information = pdf.extract([
    ('with_formatter', lambda match: match.text()),
    ('classification', 'LTTextLineHorizontal:in_bbox("40, 730, 200, 765")'),  # ok
    ('type_supply', 'LTTextLineHorizontal:in_bbox("190, 733.815, 237.870, 759.595")'),  # ok
    ("reference_date", 'LTTextLineHorizontal:in_bbox("53.050, 610.880, 96.960, 633.780")'),  # ok

    ('with_parent', 'LTTextLineHorizontal:in_bbox("42.500, 621.880, 194.589, 732.714")'),
    ("name", 'LTTextLineHorizontal:in_bbox("40, 713.844, 200, 732.714")'),
    ("address", 'LTTextLineHorizontal:in_bbox("40, 676.351, 200, 693.793")'),
    ('with_formatter', lambda match: transform_number(match.text())),
    ("CEP", 'LTTextLineHorizontal:contains("CEP")'),  # ok
    ("document", 'LTTextLineHorizontal:contains("CNPJ")'),  # ok
    ("conta_contrato", 'LTTextLineHorizontal:contains(" Contrato:")'),  # ok
    ('with_parent', None),
    ("installation_code", 'LTTextLineHorizontal:in_bbox("207.550, 700, 262.594, 724.613")'),  # ok
    ("client_code", 'LTTextLineHorizontal:in_bbox("204.500, 660, 265.660, 686.663")'),  # ok
    ("days_reading", 'LTTextLineHorizontal:in_bbox("441.350, 700.987, 471.358, 741.391")'),  # ok
    ("total_amount_payable", 'LTTextLineHorizontal:in_bbox("188.100, 610.880, 250.920, 633.780")'),  # ok
    ('with_formatter', lambda match: transform_date(match.text())),
    ("due_date", 'LTTextLineHorizontal:in_bbox("110.850, 610.880, 160.890, 633.780")'),  # ok
    ("previous_reading", 'LTTextLineHorizontal:in_bbox("321.700, 700.987, 366.736, 741.391")'),  # ok
    ("current_reading", 'LTTextLineHorizontal:in_bbox("382.650, 700.987, 427.686, 741.391")'),  # ok
    ("next_reading", 'LTTextLineHorizontal:in_bbox("491.800, 700.987, 536.836, 741.697")'),  # ok
])

footer_information = pdf.extract([
    ('with_formatter', lambda match: transform_date(match.text())),
    ('due_date_footer', 'LTTextLineHorizontal:in_bbox("422.650, 206.880, 472.690, 218.780")'),
    ('with_formatter', lambda match: transform_number(match.text())),
    ('invoice_total', 'LTTextLineHorizontal:in_bbox("260.400, 206.880, 326.000, 218.780")'),
    ('withheld_taxes', 'LTTextLineHorizontal:in_bbox("361.550, 206.880, 381.010, 218.780")'),
    ('total_amount_payable_footer', 'LTTextLineHorizontal:in_bbox("486.450, 206.880, 536.490, 218.780")'),

])


header_object = json.dumps(header_information, indent=4, ensure_ascii=False)
footer_object = json.dumps(footer_information, indent=4, ensure_ascii=False)
with open('jsons/test.json', 'w') as conta:
    conta.write(
       "{\n" +
       f'"header" : {header_object}, '
       f'"footer":{footer_object} ' +
       "\n}")
