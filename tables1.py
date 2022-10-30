from pdfquery import pdfquery
import json
import re

pdf = pdfquery.PDFQuery("contas/light_modelo_5_3.pdf")
pdf.load()


def location_in(x0, y0, x1, y1):
    return pdf.pq('LTTextLineHorizontal:in_bbox("%s, %s, %s, %s")' % (x0, y0, x1, y1)).text()


def search(expression_re, box):
    valor = re.search(expression_re, box)
    return valor.string


def transform_number(x):
    x = re.sub(r'[^0-9\,\-]', '', x)
    x = re.sub(r':|,', '.', x)
    return x


def search_items(x0, y0, x1, y1, bottom_total, counter=7.25):
    items = []
    left = x0
    bottom = y0
    right = x1
    top = y1

    # fazer um try except
    while bottom > bottom_total:
        try:
            items.append(float(transform_number(location_in(left, bottom, right, top))))
        except:
            items.append(location_in(left, bottom, right, top))

        bottom = round(bottom - counter, 3)
        top = round(top - counter, 3)

    return items


label = pdf.pq('LTTextLineHorizontal:contains("Itens de fatura")')
left_corner = 35
x = float(label.attr('y0'))
print(x)
bottom_corner = round(x - 165, 3)
right_corner = 459
top_corner = round(x + 7, 3)


box = location_in(left_corner, bottom_corner, right_corner, top_corner)

item1 = search(r'\w', box)
print(item1)
item = pdf.extract([
    ('with_formatter', lambda match: match.text()),
    ("sei lá", location_in(45.350, 542.151, 93.195, 550.481))
])
print(item)

print(item)


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
array_text_object = json.dumps(array_test, indent=4, ensure_ascii=False)

with open('jsons/array.json', 'w') as array:
    array.write(array_text_object)

