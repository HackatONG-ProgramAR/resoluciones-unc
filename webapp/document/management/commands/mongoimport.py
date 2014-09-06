from django.core.management.base import BaseCommand
from django.db import transaction

from iepy.db import connect
from iepy.models import IEDocument, Entity as IEPYEntity

from document.models import EntityKind, Entity, EntityOccurrence, Document, \
        DocumentFile, Person, Date


class Command(BaseCommand):
    args = '<dbname>'
    help = 'Import Mongo database.'

    @transaction.commit_manually
    def handle(self, *args, **options):
        assert len(args) == 1
        dbname = args[0]
        connect(dbname)

        self.import_documents(dbname)
        self.import_entities(dbname)
        self.import_entity_occurrences(dbname)

    def import_documents(self, dbname):
        print 'Importing documents from {}...'.format(dbname)
        docs = IEDocument.objects.timeout(False)
        for doc in docs:
            number = int(doc.metadata['number'])
            date = doc.metadata.get('date')
            print 'Document {}'.format(number)

            document = Document(number=number, date=date)
            document.save()

            for index, (filename, pages, offset) in enumerate(doc.metadata['files']):
                pages = u' '.join(pages)
                document_file = DocumentFile(document=document, index=index, \
                        filename=filename, pages=pages, offset=offset)
                document_file.save()

        transaction.commit()

    def import_entities(self, dbname):
        print 'Importing entity kinds and entities (persons and dates)...'
        entities = IEPYEntity.objects.timeout(False)
        i, j = 0, 0
        for entity in entities:
            kind_name = entity.kind
            # get_or_create doesn't work when autocommit is off:
            #kind, _ = EntityKind.objects.get_or_create(name=kind_name)
            # FIXME: create entity kinds before, all at once
            try:
                kind = EntityKind.objects.get(name=kind_name)
            except:
                kind = EntityKind(name=kind_name)
                kind.save()

            if kind_name == u'person':
                name = entity.key
                #print 'Person {}'.format(i)
                if 'identifier' in entity:
                    identifier = entity.identifier
                else:
                    identifier = None
                person = Person(key=name, kind=kind, name=name, identifier=identifier)
                person.save()
                i += 1
            elif kind_name == u'date':
                name = entity.key
                #print 'Date {}'.format(k)
                date = Date(key=name, kind=kind)
                date.save()
                j += 1
            else:
                # Not subclassed entity:
                entity = Entity(key=entity.key, kind=kind)
                entity.save()

        transaction.commit()
        print 'Imported {} persons and {} dates'.format(i, j)

    def import_entity_occurrences(self, dbname):
        print 'Importing entity occurrences...'
        docs = IEDocument.objects.timeout(False)
        i = 0
        for doc in docs:
            number = int(doc.metadata['number'])
            print 'Processing document {}...'.format(number)

            occurrences = []
            for entity_oc in doc.entities:
                document = Document.objects.get(number=number)

                # convert token offsets to text offsets
                offset = doc.offsets[entity_oc.offset]
                offset_end = doc.offsets[entity_oc.offset_end]

                entity = Entity.objects.get(key=entity_oc.entity.key)
                entity_oc = EntityOccurrence(document=document, entity=entity, \
                        offset=offset, offset_end=offset_end)
                entity_oc.save()
                occurrences.append(entity_oc)
                i += 1

            transaction.commit()

        print 'Imported {} entity occurrences'.format(i)
