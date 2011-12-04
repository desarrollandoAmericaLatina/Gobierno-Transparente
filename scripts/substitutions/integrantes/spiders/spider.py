from datetime import datetime
import os
import re

from selenium import webdriver
from scrapy.spider import BaseSpider
from scrapy.item import Item, Field
from scrapy.http import FormRequest
from scrapy.selector import HtmlXPathSelector
from scrapy.shell import inspect_response


class AsuntosCrawler(object):
    SEN_TOCTREE_URL = 'http://www0.parlamento.gub.uy/palacio3/p_menucssTree.asp'
    SEN_APROBACIONES_URL = 'http://www0.parlamento.gub.uy/forms2/ultimasaprobacionesfechas.asp?Cuerpo=S'
    DIP_APROBACIONES_URL = 'http://www0.parlamento.gub.uy/forms2/ultimasaprobacionesfechas.asp?Cuerpo=D'
    DETALLE_ASUNTO_URL = 'http://www0.parlamento.gub.uy//websip/lisficha/fichaap.asp?Asunto=%s'

    def __init__(self):
        self.chrome = webdriver.Chrome()


    def list_asuntos_sen(self, start, end):
        start = start.strftime('%d%m%Y')
        end = end.strftime('%d%m%Y')

        self.chrome.get(self.SEN_APROBACIONES_URL)
        desde_input = self.chrome.find_elements_by_name('FecDesde')[0]
        hasta_input = self.chrome.find_elements_by_name('FecHasta')[0]

        desde_input.send_keys(start)
        hasta_input.send_keys(end)

        submit = self.chrome.find_elements_by_id('IMAGE1')[0]
        submit.click()

class IntegranteLegislatura(Item):
    id = Field()
    substitution_info = Field()
    chamber = Field()

class IntegracionCuerpoSpider(BaseSpider):
    name = 'integrantes'
    date_fmt = "%d%m%Y"

    REFERENCE_PATTERN_EXPR = '.*\((\\d*)\).*'
    REFERENCE_VALUE_EXPR = '(Pasaje al Senado|Sustituye *al *(Senador|Representante) *([\\w ]*), *(([\\w]*)) *durante *(la|el) ([\\D ]*)) desde el ([^ ]*)[^\\d]*([^ ]*).*'

    def __init__(self, start=datetime.today()):
        self.start = start
        self.reference_pattern = re.compile(self.REFERENCE_PATTERN_EXPR, re.UNICODE)
        self.substitution_pattern = re.compile(self.REFERENCE_VALUE_EXPR, re.UNICODE)

    def start_requests(self):
        return [
            FormRequest('http://www0.parlamento.gub.uy/forms/IntCpo.asp?Cuerpo=S',
                        formdata={
                            'Fecha': self.start.strftime(self.date_fmt),
                            'Cuerpo': 'S',
                            'Integracion': 'S',
                            'Desde': '15021985',
                            'Hasta': datetime.today().strftime(self.date_fmt),
                            'Dummy': datetime.today().strftime(self.date_fmt),
                            'TipoLeg': 'Act',
                            'Orden': 'Legislador',
                            'Integracion': 'S'
                        },
                        callback=self.parse_dip),
            FormRequest('http://www0.parlamento.gub.uy/forms/IntCpo.asp?Cuerpo=D',
                        formdata={
                            'Fecha': self.start.strftime(self.date_fmt),
                            'Cuerpo': 'D',
                            'Integracion': 'S',
                            'Desde': '15021985',
                            'Hasta': datetime.today().strftime(self.date_fmt),
                            'Dummy': datetime.today().strftime(self.date_fmt),
                            'TipoLeg': 'Act',
                            'Orden': 'Legislador',
                            'Integracion': 'S'
                        },
                        callback=self.parse_sen),
        ]

    def parse_dip(self, response):
        return self.__parse(response, 'Senate')

    def parse_sen(self, response):
        return self.__parse(response, 'Deputy')

    def __parse(self, response, chamber):
        #inspect_response(response)
        hxs = HtmlXPathSelector(response)

        refs = {}
        tds = hxs.select('//table')[-2].select('.//tr')
        for ref_td in tds:
            ref = ref_td.select('.//td').re('.*\((\\d*)\).*')
            if len(ref) != 1:
                continue
            ref = ref[0]
            value = "".join(ref_td.select('.//td/*')[1].select('.//text()').extract()).strip()
            ref_id_elem = ref_td.select('.//td/*/a/@href').extract()
            ref_id = None
            if len(ref_id_elem) == 1:
                ref_id = ref_id_elem[0][-7:-2]
            m = self.substitution_pattern.match(value)
            res = {'fullreason' : value}
            if m:
                if ref_id:
                    res['substituted_id'] = ref_id
                groups = m.groups()
                res['lastname'] = groups[2]
                res['firstname'] = groups[3]
                res['reason'] = groups[6]
                if groups[7]:
                    res['from'] = groups[7]
                if groups[8]:
                    res['to'] = groups[8]
            refs[ref] = res

        table = hxs.select('//table')[4]
        names = table.select('.//tr/td/font/a/parent::*')
        parties = table.select('.//tr/td/font/text()').re('PARTIDO.*')
        items = []
        for name, party in zip(names, parties):
            item = IntegranteLegislatura()
            item['chamber'] = chamber
            item['id'] = name.select('.//a/@href').extract()[0][-7:-2]

            strong = name.select('.//strong').extract()
            if len(strong) == 1:
                strong = strong[0]
                m = self.reference_pattern.match(strong)
                if m:
                    groups = m.groups()
                    if len(groups) == 1:
                        reference = groups[0]
                        if reference in refs:
                            item['substitution_info'] = refs[reference]

            items.append(item)

        return items






