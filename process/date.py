# -*- coding: utf-8 *-*
import codecs

from iepy.models import Entity, EntityOccurrence

from process.regexp_ner import RegExpNERRunner, options_re, options_file_re


class DateNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        day = u'<\d{1,2}>'
        of = u'<de>'
        months = 'enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre'.split()
        month = options_re(months)
        regexp = day + of + month
        super(DateNERRunner, self).__init__('date', regexp, override)
