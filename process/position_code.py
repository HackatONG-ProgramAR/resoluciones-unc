# -*- coding: utf-8 *-*
import codecs

from iepy.models import Entity, EntityOccurrence

from process.regexp_ner import (RegExpNERRunner, options_re, options_file_re,
								optional_re)


# c6d, cargo 119/49


class PositionCodeNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        regexp = "<c[o6H]d>" + optional_re("<,>") + optional_re("<.>") + "<cargo>" + "<\d{1,3}>" + "</>" + "<\d{1,3}>"
        super(PositionCodeNERRunner, self).__init__('position_code', regexp, override)
