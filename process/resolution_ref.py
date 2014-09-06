# -*- coding: utf-8 *-*
import codecs

from iepy.models import Entity, EntityOccurrence

from process.regexp_ner import (RegExpNERRunner, options_re, options_file_re,
								optional_re)


class ResolutionRefNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        regexp = "<Res>" + "(<.>)?" +"(<CD>|<HCS>)" + "(<No>)?" + "<\d{1,4}>" + "</>" + "<\d{1,4}>"
        super(ResolutionRefNERRunner, self).__init__('resolution_ref', regexp, override)
