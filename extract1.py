"""
Primeiro código que fiz para extração dos arquivos da conta 3.
"""
from pdfquery import pdfquery
import json
import re

pdf = pdfquery.PDFQuery("contas/light_modelo_5_3.pdf")
pdf.load()


def transform_number(x):
    x = re.sub(r'[^0-9\,]', '', x)
    x = re.sub(r':|,', '.', x)
    return x


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
    ('classification', 'LTTextLineHorizontal:in_bbox("48.150, 743.815, 185.980, 749.595")'),
    ('type_supply', 'LTTextLineHorizontal:in_bbox("201.200, 743.815, 227.870, 749.595")'),
    ("name", 'LTTextLineHorizontal:in_bbox("42.500, 713.844, 185.372, 732.714")'),
    ("address", 'LTTextLineHorizontal:in_bbox("42.500, 676.351, 194.589, 693.793")'),
    ("document", 'LTTextLineHorizontal:in_bbox("42.500, 667.001, 125.380, 675.093")'),
    ("conta_contrato", 'LTTextLineHorizontal:in_bbox("42.500, 657.651, 139.002, 665.743")'),
    ("reference_date", 'LTTextLineHorizontal:in_bbox("53.050, 621.880, 96.960, 633.780")'),
    ('with_formatter', lambda match: int(transform_number(match.text()))),
    ("installation_code", 'LTTextLineHorizontal:in_bbox("207.550, 711.523, 262.594, 724.613")'),
    ("client_code", 'LTTextLineHorizontal:in_bbox("204.500, 673.573, 265.660, 686.663")'),
    ("days_reading", 'LTTextLineHorizontal:in_bbox("451.350, 730.987, 461.358, 741.391")'),
    ('with_formatter', lambda match: float(transform_number(match.text()))),
    ("total_amount_payable", 'LTTextLineHorizontal:in_bbox("188.100, 621.880, 250.920, 633.780")'),
    ('with_formatter', lambda match: transform_date(match.text())),
    ("due_date", 'LTTextLineHorizontal:in_bbox("110.850, 621.880, 160.890, 633.780")'),
    ("previous_reading", 'LTTextLineHorizontal:in_bbox("321.700, 730.987, 366.736, 741.391")'),
    ("current_reading", 'LTTextLineHorizontal:in_bbox("382.650, 730.987, 427.686, 741.391")'),
    ("next_reading", 'LTTextLineHorizontal:in_bbox("491.800, 730.987, 536.836, 741.697")'),
])


footer_information = pdf.extract([
    ('with_formatter', lambda match: transform_date(match.text())),
    ('due_date_footer', 'LTTextLineHorizontal:in_bbox("422.650, 206.880, 472.690, 218.780")'),
    ('with_formatter', lambda match: float(transform_number(match.text()))),
    ('invoice_total' , 'LTTextLineHorizontal:in_bbox("260.400, 206.880, 326.000, 218.780")'),
    ('withheld_taxes', 'LTTextLineHorizontal:in_bbox("361.550, 206.880, 381.010, 218.780")'),
    ('total_amount_payable_footer', 'LTTextLineHorizontal:in_bbox("486.450, 206.880, 536.490, 218.780")'),

])


payment_information = pdf.extract([
    ('with_formatter', lambda match: match.text()),
    ('bank_payment', 'LTTextLineHorizontal:in_bbox("45.350, 181.330, 130.350, 193.230")'),
    ('bank_code', 'LTTextLineHorizontal:in_bbox("202.550, 181.330, 228.120, 193.230")'),
    ('bar_code_numbers', 'LTTextLineHorizontal:in_bbox("283.950, 181.330, 553.610, 193.230")'),
    ('preference_payment', 'LTTextLineHorizontal:in_bbox("45.350, 164.744, 257.208, 173.992")'),
    ('instruction_payment', 'LTTextLineHorizontal:in_bbox("45.350, 89.394, 297.758, 117.34")'),
    ('name_payment', 'LTTextLineHorizontal:in_bbox("45.350, 67.001, 219.594, 75.093")'),
    ('address_payment', 'LTTextLineHorizontal:in_bbox("45.350, 58.851, 130.925, 66.943")'),
    ('agency_cedingCode', 'LTTextLineHorizontal:in_bbox("501.200, 147.744, 555.116, 156.992")'),
    ('our_number_ticket', 'LTTextLineHorizontal:in_bbox("494.900, 136.344, 554.948, 145.592")'),
    ('with_formatter', lambda match: int(transform_number(match.text()))),
    ('number_client_code', 'LTTextLineHorizontal:in_bbox("45.350, 50.701, 99.838, 58.793")'), # Não sei o que é esse número
    ('with_formatter', lambda match: float(transform_number(match.text()))),
    ('value_ticket_payment', 'LTTextLineHorizontal:in_bbox("515.100, 49.994, 555.132, 59.242")'),
    ('value_ticket', 'LTTextLineHorizontal:in_bbox("515.150, 122.244, 555.182, 131.492")'),
    ('with_formatter', lambda match: transform_date(match.text())),
    ('due_date_ticket', 'LTTextLineHorizontal:in_bbox("515.100, 164.744, 555.132, 173.992")'),
])


others_information = pdf.extract([
    ('with_formatter', lambda match: match.text()),
    ('fisco_box', 'LTTextLineHorizontal:in_bbox("282.300, 336.408, 535.060, 360.144")'),
    # contract quantify está aqui apenas para representar, mas deveria ser uma dict
    ('contracted_quantities_name', 'LTTextLineHorizontal:in_bbox("462.050, 488.972, 491.618, 493.596")'),
    #('with_formatter', lambda match: float(transform_number(match.text()))),
    ('contracted_quantities_value', 'LTTextLineHorizontal:in_bbox("530.100, 488.972, 545.668, 493.596")'),
])


def array_test():
    # titles
    name_indice = location_in(45.350, 542.151, 93.195, 550.481)
    unit_indice, quantify_indice = location_in(185.650, 542.358, 226.352, 549.498).split()
    unit_price_with_taxes_indice = location_in(237.350, 538.965, 272.910, 550.915)
    value_indice = location_in(282.050, 542.358, 310.438, 549.498)

    # items
    y0 = 531.715
    y1 = 537.495
    bottom_total = 459

    items_name = search_items(45.350, y0, 123.720, y1, bottom_total)
    items_unit = search_items(186.200, y0, 196.200, y1, bottom_total)
    items_quantify = search_items(214.200, y0, 232.340, y1, bottom_total)
    items_unit_price_with_taxes = search_items(248.350, y0, 277.56, y1, bottom_total)
    items_value = search_items(289.400, y0, 314.490, y1, bottom_total)

    return {
        name_indice: items_name,
        unit_indice: items_unit,
        quantify_indice: items_quantify,
        unit_price_with_taxes_indice: items_unit_price_with_taxes,
        value_indice: items_value
    }
array_test = array_test()


header_object = json.dumps(header_information, indent=4, ensure_ascii=False)
footer_object = json.dumps(footer_information, indent=4, ensure_ascii=False)
payment_object = json.dumps(payment_information, indent=4, ensure_ascii=False)
others_object = json.dumps(others_information, indent=4, ensure_ascii=False)
array_text_object = json.dumps(array_test, indent=4, ensure_ascii=False)
with open('jsons/conta3.json', 'w') as conta:
    conta.write(
       "{\n" +
       f'"header" : {header_object}, '
       f'"footer":{footer_object}, '
       f'"payment":{payment_object}, '
       f'"others":{others_object},'
       f'"array_test":{array_text_object}' +
       "\n}")
