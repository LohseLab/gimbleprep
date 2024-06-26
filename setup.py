from setuptools import setup

setup(
    name='gimbleprep',
    version='0.0.2',
    description='Preprocess fasta, bam and vcf files ready to be used by gimble',
    url='http://github.com/LohseLab/gimbleprep',
    author='Lohse Lab',
    author_email='',
    license='GPLv3',
    packages=["gimbleprep"],
    package_dir={
        "": ".",
        "gimbleprep": "./gimbleprep",
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
        "vcflib==1.0.3",
        "tabixpp==1.1.0",
        "mosdepth==0.3.2",
    ],
    entry_points={
        'console_scripts': [
            'gimbleprep = gimbleprep.interface:main',
        ]
    }
)
