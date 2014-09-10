import re
import codecs

from refo import Predicate, Any, Star, finditer


class Word(object):

    def __init__(self, token, pos='', entity_pos='O', entity=None, sent_start=False):
        self.token = token
        self.pos = pos
        self.entity_pos = entity_pos
        self.entity = entity
        self.sent_start = sent_start

    def __unicode__(self):
        show = [self.token, self.pos, self.entity_pos]
        if self.sent_start:
            show.append('START')
        return u'/'.join(show)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __repr__(self):
        return str(self)


class W(Predicate):

    def __init__(self, token='.*', pos='.*', entity_pos='.*', entity=Any(), sent_start=None):
        self.token = re.compile(token + "$")
        self.pos = re.compile(pos + "$")
        self.entity_pos = re.compile(entity_pos + "$")
        self.entity = entity
        self.sent_start = sent_start
        super(W, self).__init__(self.match)

    def match(self, word):
        result = self.token.match(word.token) and \
                    self.pos.match(word.pos) and \
                    self.entity_pos.match(word.entity_pos) and \
                    self.entity.f(word) and \
                    (self.sent_start is None or self.sent_start == word.sent_start)
        return result

    def __repr__(self):
        return '<W token={}>'.format(self.token.pattern[:-1])


class E(Predicate):

    def __init__(self, key='.*', canonical_form='.*', kind='.*'):
        self.key = re.compile(key + "$")
        self.canonical_form = re.compile(canonical_form + "$")
        self.kind = re.compile(kind + "$")
        super(E, self).__init__(self.match)

    def match(self, word):
        if word.entity:
            result = self.key.match(word.entity.entity.key) and \
                        self.canonical_form.match(word.entity.entity.canonical_form) and \
                        self.kind.match(word.entity.entity.kind)
        else:
            result = False
        return result


def entity_re(key='.*', canonical_form='.*', kind='.*', inside_sent=True):
    if inside_sent:
        sent_start = False
    else:
        sent_start = None
    pattern = W(entity_pos='S', entity=E(key, canonical_form, kind)) + \
                Star(W(entity_pos='I', sent_start=sent_start))
    return pattern


def document_words(doc):
    # XXX: it is assumed that entities are not overlapping

    sentences = list(doc.sentences) + [-1]
    next_sent_start = sentences.pop(0)
    assert next_sent_start == 0
    entities = list(doc.entities)
    if entities:
        e = entities.pop(0)
        offset = e.offset
        offset_end = e.offset_end
    else:
        offset = offset_end = len(doc.tokens)

    result = []
    for i, token in enumerate(doc.tokens):
        if i == next_sent_start:
            sent_start = True
            next_sent_start = sentences.pop(0)
        else:
            sent_start = False

        if i < offset:
            # not in the next entity yet
            word = Word(token, sent_start=sent_start)
        elif offset <= i:
            # in the entity
            if offset == i:
                e_pos = 'S' # start of entity
            elif offset < i:
                e_pos = 'I' # inside of entity
            word = Word(token, entity_pos=e_pos, entity=e, sent_start=sent_start)

        # if required, advance to next entity:
        if i == offset_end - 1:
            if entities:
                e = entities.pop(0)
                offset = e.offset
                offset_end = e.offset_end
            else:
                offset = offset_end = len(doc.tokens)

        result.append(word)

    return result


def pprint_match(m, words):
    i, j = m.group()
    return ' '.join([str(w) for w in words[i:j]])


def tokenized_re(s):
    s2 = s.split()
    result = W(token=s2.pop(0))
    while s2:
        result = result + W(token=s2.pop(0))
    return result


def options_re(options):
    assert options
    options2 = map(tokenized_re, options)
    result = options2.pop(0)
    while options2:
        result = result | options2.pop(0)
    return result

def options_file_re(filename):
    f = codecs.open(filename, encoding="utf8")
    options = f.read().strip().split('\n')
    f.close()
    return options_re(options)
