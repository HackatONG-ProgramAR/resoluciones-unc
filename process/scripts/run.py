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
from iepy.preprocess import PreProcessPipeline
from process.settings import pipeline_steps


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('process')
    opts = docopt(__doc__, version=0.1)
    connect(opts['<dbname>'])
    docs = DocumentManager()
    pipeline = PreProcessPipeline(pipeline_steps, docs)
    pipeline.process_everything()
