import codecs
import os

from django.db import models
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

from model_utils.managers import InheritanceManager

from webapp.settings import BASE_DIR


data_root_path = os.path.dirname(BASE_DIR)  # project home absolute path


class Document(models.Model):
    class Meta:
        ordering = ['number']
        verbose_name = _(u'document')
        verbose_name_plural = _(u'documents')

    number = models.IntegerField(primary_key=True, verbose_name=_(u'number'))
    date = models.DateField(null=True, verbose_name=_(u'date'))

    def text(self):
        text = u''
        for f in self.documentfile_set.all():
            text += f.text()
        return text

    def files(self):
        return self.documentfile_set.all()

    def file(self, index):
        return self.documentfile_set.get(index=index)

    def file_offset(self, offset):
        return self.documentfile_set.filter(offset__lte=offset).last()

    def __unicode__(self):
        return u'Document {}'.format(self.number)


class DocumentFile(models.Model):
    document = models.ForeignKey(Document)
    index = models.IntegerField()
    filename = models.CharField(max_length='100', primary_key=True)
    pages = models.CharField(max_length='100')
    offset = models.IntegerField()

    def link_tag(self, s=None):
        if not s:
            s = unicode(self)
        index = self.index
        number = self.document.number
        url = urlresolvers.reverse('file', args=(number, index))
        return u'<a href="{}">{}</a>'.format(url, s)

    def text(self):
        filename = self.filename
        file_path = os.path.join(data_root_path, filename)
        f = codecs.open(file_path, encoding='utf-8')
        text = f.read()
        return text

    def tagged_text(self, highlight=None):
        document = self.document
        text = self.text()
        start_offset = self.offset
        end_offset = start_offset + len(text)

        # get entity occurrences in this document file
        entities = document.entityoccurrence_set.filter(offset__gte=start_offset, \
                offset__lt=end_offset)

        # tag occurrences in text
        tagged_text = u''
        offset = 0
        for e in entities:
            next_offset = e.offset - start_offset
            next_offset_end = e.offset_end - start_offset
            tagged_text += text[offset:next_offset]
            clazz = None
            if e.id == highlight:
                extra_class = 'highlight'
            else:
                extra_class = None
            link = e.entity.link_tag(text[next_offset:next_offset_end], clazz, extra_class)
            tagged_text += link
            offset = next_offset_end
        tagged_text += text[offset:]

        return tagged_text

    def __unicode__(self):
        return u'{} ({})'.format(self.document, self.filename)


class EntityKind(models.Model):
    name = models.CharField(max_length='100', primary_key=True)


class Entity(models.Model):
    class Meta:
        ordering = ['key']

    objects = InheritanceManager()
    key = models.CharField(max_length='200', unique=True, verbose_name=_(u'key'))
    kind = models.ForeignKey(EntityKind)

    def occurrences(self):
        return self.entityoccurrence_set.order_by('document')

    def occurrence_count(self):
        return self.entityoccurrence_set.count()

    def subclass(self):
        return Entity.objects.get_subclass(id=self.id)

    def link_tag(self, s=None, clazz=None, extra_class=None):
        if not s:
            s = unicode(self)
        if clazz is None:
            clazz = self.kind.name
        title = clazz
        if extra_class:
            clazz += ' ' + extra_class
        url = urlresolvers.reverse(self.kind.name, args=(self.id,))
        return u'<a href="{}" class="{}" title="{}">{}</a>'.format(url, clazz, _(title), s)

    def __unicode__(self):
        return self.key


class EntityOccurrence(models.Model):
    document = models.ForeignKey(Document)
    entity = models.ForeignKey(Entity)
    offset = models.IntegerField()
    offset_end = models.IntegerField()

    def kind(self):
        return self.entity.kind.name

    def entity_subclass(self):
        return self.entity.subclass()

    def link_tag(self, s=None):
        if not s:
            s = unicode(self)
        number = self.document.number
        url = urlresolvers.reverse('occurrence', args=(number, self.id))
        return u'<a href="{}">{}</a>'.format(url, s)

    def __unicode__(self):
        return u'Document {}:{}'.format(self.document.number, self.offset)


class Person(Entity):
    class Meta:
        ordering = ['name']
        verbose_name = _(u'person')
        verbose_name_plural = _(u'persons')

    name = models.CharField(max_length='200', verbose_name=_(u'name'))
    identifier = models.CharField(max_length='100', null=True, verbose_name=_(u'identifier'))

    def __unicode__(self):
        return self.name


class Date(Entity):
    class Meta:
        verbose_name = _(u'date')
        verbose_name_plural = _(u'dates')
