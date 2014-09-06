from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core import urlresolvers

from document.models import Document, Entity, EntityOccurrence, EntityKind


def index(request):
    return redirect(urlresolvers.reverse('admin:document_document_changelist'))


def document(request, number):
    return redirect(urlresolvers.reverse('file', args=(number, 0)))


def offset(request, number, offset):
    document = get_object_or_404(Document, number=number)
    index = document.file_offset(offset).index
    return redirect(urlresolvers.reverse('file', args=(number, index)))


def file(request, number, index, occurrence=None):
    index = int(index)
    document = get_object_or_404(Document, number=number)
    document_file = document.file(index)
    if occurrence:
        occurrence = int(occurrence)
    tagged_text = document_file.tagged_text(highlight=occurrence)

    entity_kinds = list(EntityKind.objects.all())
    colors = get_colors(len(entity_kinds))

    context = {'entity_kinds_colors': zip(entity_kinds, colors),
                'document_file': document_file,
                'text': tagged_text,
                'index': index}
    return render(request, 'document/file.html', context)


def occurrence(request, number, occurrence):
    entity_occurrence = get_object_or_404(EntityOccurrence, id=int(occurrence))
    offset = entity_occurrence.offset
    index = entity_occurrence.document.file_offset(offset).index
    return file(request, number, index, occurrence)


def person(request, id):
    return redirect(urlresolvers.reverse('admin:document_person_change', args=(id,)))


def date(request, id):
    return redirect(urlresolvers.reverse('admin:document_date_change', args=(id,)))

def entity(request, id):
    return redirect(urlresolvers.reverse('admin:document_entity_change', args=(id,)))

def document(request, id):
    document = get_object_or_404(Entity, id=id)
    return redirect(urlresolvers.reverse('document', args=(document.key,)))


def get_colors(n):
    # Kelly's maximum contrast colors:
    # http://stackoverflow.com/questions/470690/how-to-automatically-generate-n-distinct-colors
    colors = [
        '#FFB300', # Vivid Yellow
        #'#803E75', # Strong Purple
        #'#FF6800', # Vivid Orange
        '#A6BDD7', # Very Light Blue
        #'#C10020', # Vivid Red
        '#CEA262', # Grayish Yellow
        #'#817066', # Medium Gray
        # The following will not be good for people with defective color vision
        #'#007D34', # Vivid Green
        '#F6768E', # Strong Purplish Pink
        #'#00538A', # Strong Blue
        '#FF7A5C', # Strong Yellowish Pink
        '#53377A', # Strong Violet
        '#FF8E00', # Vivid Orange Yellow
        '#B32851', # Strong Purplish Red
        '#F4C800', # Vivid Greenish Yellow
        '#7F180D', # Strong Reddish Brown
        '#93AA00', # Vivid Yellowish Green
        '#593315', # Deep Yellowish Brown
        '#F13A13', # Vivid Reddish Orange
        '#232C16', # Dark Olive Green
    ]
    assert n <= len(colors), 'Not enough colors for entities.'
    return colors[:n]
