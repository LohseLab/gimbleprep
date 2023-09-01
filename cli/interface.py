"""usage: gimble-preprocess [<args>...] [-V -h]

[Options]
    -h, --help            Show this screen
    -V, --version         Show version
"""

import sys
import os
import importlib
from docopt import docopt
from timeit import default_timer as timer

RUNNER_BY_MODULE = {
    'preprocess': 'cli.preprocess', 
}
MODULES = RUNNER_BY_MODULE.keys()


def main(gimble_dir=None):
    if gimble_dir is None:
        gimble_dir = os.path.dirname(os.path.join(os.path.realpath(__file__), '..'))
    try:
        start_time = timer()
        __version__ = '0.0.1'
        version = "gimble v%s" % __version__
        args = docopt(__doc__, version=version, options_first=True)
        if '--version' in args['<args>'] or '-V' in args['<args>']:
            sys.exit("gimble v%s" % __version__)
        params = {
            'module': 'preprocess',
            'path': gimble_dir,
            'cwd': os.getcwd(),
            'version': version
        }
        try:
            runner = importlib.import_module(RUNNER_BY_MODULE[params['module']])
            runner.main(params)
        except ImportError as error:
            print("[X] ImportError: %s" % error)
    except KeyboardInterrupt:
        sys.stderr.write("\n[X] Interrupted by user after %i seconds!\n" % (timer() - start_time))
        sys.exit(-1)