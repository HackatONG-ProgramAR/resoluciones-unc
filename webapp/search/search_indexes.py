from haystack import indexes

from document.models import DocumentFile


class DocumentFileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return DocumentFile