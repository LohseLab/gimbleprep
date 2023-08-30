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

installation_steps = """[========================= Missing dependencies =========================]
1. Get conda from https://conda.io/miniconda.html

2. Create the following conda environment 
>>> conda create -n gimble python=3.7.12 bedtools bcftools samtools vcflib mosdepth=0.3.2 pysam numpy docopt tqdm pandas tabulate zarr scikit-allel parallel matplotlib msprime demes dask numcodecs python-newick nlopt -c conda-forge -c bioconda -y

3. Load the environment (needs to be activated when using gimble)
>>> conda activate gimble

4. Install agemo (make sure you have the conda environment activated)
>>> (gimble) pip install agemo

5. Rock'n'roll ...
[========================================================================]
"""
def main(gimble_dir):
    try:
        start_time = timer()
        __version__ = '1.0.3'
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
            print(installation_steps)
    except KeyboardInterrupt:
        sys.stderr.write("\n[X] Interrupted by user after %i seconds!\n" % (timer() - start_time))
        sys.exit(-1)