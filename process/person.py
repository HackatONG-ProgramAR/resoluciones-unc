# -*- coding: utf-8 *-*
import codecs

from iepy.models import Entity, EntityOccurrence

from process.regexp_ner import RegExpNERRunner, options_re, options_file_re


class PersonNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        # TODO: write this regexp!
        regexp = ''

        super(PersonNERRunner, self).__init__('person', regexp, override)

    def process_match(self, match):
        name = ' '.join(match.group('name'))
        kind = self.label
        identifier = match.group('id')
        if identifier:
            identifier = ''.join(identifier)
        entity, created = Entity.objects.get_or_create(key=name, kind=kind,
                defaults={'canonical_form': name, 'identifier': identifier})
        offset, offset_end = match.span()
        entity_oc = EntityOccurrence(entity=entity, offset=offset, offset_end=offset_end)

        return entity_oc
