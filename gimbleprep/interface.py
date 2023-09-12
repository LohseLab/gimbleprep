"""
usage: gimbleprep                 -f <f> -v <v> -b <b> [-g <g> -m <m> -M <M> -q <q> -t <t> -o <o> -k] [-h|--help]
                                        
[Options]
    -f, --fasta_file=<f>             FASTA file
    -v, --vcf_file=<v>               VCF file (raw)
    -b, --bam_dir=<b>                Directory containing all BAM files
    -g, --snpgap=<g>                 SnpGap [default: 2]
    -q, --min_qual=<q>               Minimum PHRED quality [default: 1]
    -m, --min_depth=<m>              Min read depth [default: 8]
    -M, --max_depth=<M>              Max read depth (as multiple of mean coverage of each BAM) [default: 2]
    -t, --threads=<t>                Threads [default: 1]
    -o, --outprefix=<o>              Outprefix [default: gimble]
    -k, --keep_tmp                   Do not delete temporary files [default: False]
    -h, --help                       Show this
"""

import sys
import os
import importlib
from docopt import docopt
from timeit import default_timer as timer

RUNNER_BY_MODULE = {
    'preprocess': 'gimbleprep.preprocess', 
}
MODULES = RUNNER_BY_MODULE.keys()


def main(gimble_dir=None):
    if gimble_dir is None:
        gimble_dir = os.path.dirname(os.path.join(os.path.realpath(__file__), '..'))
    try:
        start_time = timer()
        __version__ = '0.0.2d'
        version = "gimble v%s" % __version__
        args = docopt(__doc__, version=version, options_first=True)
        # print(args)
        if '--version' in args.keys() or '-V' in args.keys():
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