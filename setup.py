from setuptools import setup

setup(
    name='gimbleprep',
    version='0.0.2b3',
    description='Preprocess fasta, bam and vcf files ready to be used by gimble',
    url='http://github.com/LohseLab/gimbleprep',
    author='Lohse Lab',
    author_email='',
    license='GPLv3',
    packages=["cli", "lib"],
    package_dir={
        "": ".",
        "cli": "./cli",
        "lib": "./lib",
    },
    install_requires=[
        "docopt",
        "numpy",
        "pandas",
        "parallel",
        "pysam",
        "tqdm",
        "bedtools",
        "bcftools",
        "samtools",
        "vcflib",
        "mosdepth==0.3.2"
    ],
    entry_points={
        'console_scripts': [
            'gimbleprep = cli.interface:main',
        ]
    }
)
