# -*- coding: utf-8 *-*
import codecs

from iepy.data.models import Entity, EntityOccurrence

from process.regexp_ner import (RegExpNERRunner, options_re, options_file_re,
								optional_re)


class  PositionNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        positions = ['Ayudante A', 'Ayudante B',
                    'Asistente', 'Adjunto', 'Asociado',
                    'Titular']
        positions_p = ['Ayudantes A', 'Ayudantes B',
                    'Asistentes', 'Adjuntos', 'Asociados',
                    'Titulares']
        position = options_re(positions+positions_p)
        regexp = "<Profesor|Profesores|Prof|Profs>" + optional_re("<,>") + optional_re("<.>") + position
        super(PositionNERRunner, self).__init__('position', regexp, override)
