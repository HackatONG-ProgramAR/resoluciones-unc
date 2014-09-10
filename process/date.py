# -*- coding: utf-8 *-*
import codecs

from iepy.models import Entity, EntityOccurrence

from process.regexp_ner import RegExpNERRunner, options_re, options_file_re


class DateNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        prefix = u'(?<<= <fecha> )'
        day = u'<\d{1,2}>'
        months = u'Ene|Feb|Mar|Abr|May|Jun|Jul|Ago|Sep|Set|Oct|Nov|Dic'.split('|')
        month = options_re(months)
        year = u'(<\d{2}> | <\d{4}>)'
        regexp = prefix + day + month + year
        super(DateNERRunner, self).__init__('date', regexp, override)
