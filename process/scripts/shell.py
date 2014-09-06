"""
IEPY debugging shell.

Usage:
    shell.py <dbname>
    shell.py -h | --help | --version

Options:
  -h --help             Show this screen
  --version             Version number
"""
from docopt import docopt

from iepy.db import connect, DocumentManager
from iepy.models import IEDocument, Entity

from process.settings import pipeline_steps


if __name__ == '__main__':
    opts = docopt(__doc__, version=0.1)
    dbname = opts['<dbname>']
    connect(dbname)
    docs = IEDocument.objects
