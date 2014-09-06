"""
Document processing script. Does NER for persons, dates, etc.

Usage:
    process.py <dbname>
    process.py -h | --help | --version

Options:
  -h --help             Show this screen
  --version             Version number
"""
import logging
from docopt import docopt

from iepy.db import connect, DocumentManager
from iepy.models import set_custom_entity_kinds
from iepy.preprocess import PreProcessPipeline
from iepy.tokenizer import TokenizeSentencerRunner
from iepy.combined_ner import CombinedNERRunner

from process.person import PersonNERRunner
from process.date import DateNERRunner


# Optional custom step:
def extract_plain_text(doc):
    doc.text = doc.metadata['raw_data']
    doc.save()


# Insert here your custom entities:
CUSTOM_ENTITIES = ['date']
#CUSTOM_ENTITIES_FILES = []


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('process')
    opts = docopt(__doc__, version=0.1)
    connect(opts['<dbname>'])
    docs = DocumentManager()
    set_custom_entity_kinds(zip(map(lambda x: x.lower(), CUSTOM_ENTITIES),
                                CUSTOM_ENTITIES))
    pipeline = PreProcessPipeline([
        #extract_plain_text, # optional custom step
        TokenizeSentencerRunner(),
        CombinedNERRunner([
            #PersonNERRunner(),
            DateNERRunner(),
            ], override=True),
    ], docs
    )
    pipeline.process_everything()
