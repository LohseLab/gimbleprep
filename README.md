gimbleprep
=========

[![DOI](https://zenodo.org/badge/176883840.svg)](https://zenodo.org/badge/latestdoi/176883840)

# Table of contents

- [Installation](#installation)
- [Workflow](#workflow)
- [Usage](#usage)

# Installation

```
# 1a. clone repository
>>> git clone https://github.com/DRL/gimble.git
# 1b. clone repository
>>> git clone https://github.com/DRL/gimbleprep.git
# 2. Install miniconda from https://conda.io/miniconda.html
# ...
# 3. Create the following conda environment 
>>> conda create -n gimble python=3.7.12 agemo bedtools bcftools samtools vcflib mosdepth=0.3.2 pysam numpy docopt tqdm pandas tabulate zarr scikit-allel parallel matplotlib msprime demes dask numcodecs python-newick nlopt -c conda-forge -c bioconda
# 4. Load the environment (needs to be activated when using gimble)
>>> conda activate gimble
# 5a. Start gimbleprep'ing ...
>>> (gimble) gimbleprep/gimbleprep --help
# 5b. Start gimble'ing ...
>>> (gimble) gIMble/gimble --help
```

# Gimble Workflow

![gIMble workflow](/docs/gIMble.workflow.jpg?raw=true "gIMble workflow")
**gIMble workflow**. `preprocess` (**0**) assures input data conforms to requirements; `parse` (**1**) reads data into a `gIMble`
store, the central data structure that holds all subsequent analysis. The modules `blocks` (**2**) and
`windows` (**3**) partition the data which is summarised as a tally (**4**) of blockwise mutation
configurations (bSFSs) either across all pair-blocks (blocks tally) or for pair-blocks in windows
(windows tally). Tallies may be used either in a bounded search of parameter space via the
module `optimize` (**5**) or to evaluate likelihoods over a parameter grid (which is precomputed using
`makegrid` (**6**)) via the `gridsearch` (**7**) module. The `simulate` (**8**) module allows coalescent
simulation of tallies (simulate tally) based on inferred parameter estimates (either global
estimates or gridsearch results of window-wise data). Simulated data can be analysed to quantify
the uncertainty (and potential bias) of parameter estimates. The results held within a `gIMble` store
can be described, written to column-based output files or removed using the modules `info` (**9**),
`query` (**10**), and `delete` (**11**).


## gimbleprep
`gimbleprep` assures that input files are adequately filtered and processed so that the `gimble` workflow can be completed successfully. 
While this processing of input files could be done more efficiently with other means, it has the advantage of generating a VCF file complies with `gimble` data requirements but which can also be used in alternative downstream analyses.

```
./gimbleprep -f FASTA -b BAM_DIR/ -v RAW.vcf.gz -k
```

Based on the supplied input files:
- `-f` : FASTA of reference
- `-b`: directory of BAM files, composed of readgroup-labelled reads mapped to reference 
- `-v`: compressed+indexed Freebayes VCF file 

the module produces the following output files:

- **genome file** (sequence_id, length) based on FASTA file
- **sample file** (sample_id) based on ReadGroupIDs in BAM files
- **coverage threshold report** for each BAM file
- **gimble VCF file** (see [VCF processing details](#vcf-processing-details))
- **gimble BED file** (see [BAM processing details](#bam-processing-details))
- log of executed commands

After running, output files require manual user input (see [Manually modify files](#manually-modify-preprocessed-files))

### VCF processing details
- MNPs are decomposed into SNPs
- variant sets are defined as
  ```
  - {RAW_VARIANTS} := all variants in VCF
  - {NONSNP}       := non-SNP variants 
  - {SNPGAP}       := all variants within +/- X b of {NONSNP} variants
  - {QUAL}         := all variants with QUAL below --min_qual
  - {BALANCE}      := all variants with any un-balanced allele observation (-e 'RPL<1 | RPR<1 | SAF<1 | SAR<1') 
  - {FAIL}         := {{NONSNP} U {SNPGAP} U {QUAL} U {BALANCE}} 
  - {VARIANTS}     := {RAW_VARIANTS} - {FAIL}```
The processed VCF file 
  - only contains variants from set `{VARIANTS}` 
  - only contains sample genotypes with sample read depths within coverage thresholds (others are set to missing, i.e. `./.`)

### BAM processing details 
- definition of BED region sets
  ```
  - {CALLABLE_SITES}   := for each BAM, regions along which sample read depths lie within coverage thresholds.
  - {CALLABLES}        := bedtools multiintersect of all {CALLABLE_SITES} regions across all BAMs/samples
  - {FAIL_SITES}       := sites excluded due to {FAIL} variant set (during VCF processing)
  - {SITES}            := {CALLABLES} - {FAIL_SITES}
  ```
Resulting BED file 
- only contains BED regions from set `{SITES}` 
- lists which samples are adequately covered along each region

#### Manually modify preprocessed files
+ `gimble.genomefile`:
    + **[Optional]** remove sequence IDs to ignore them in the analyses
+ `gimble.samples.csv` 
    + **[Required]** add population IDs the second column. Must be exactly 2 populations
    + **[Optional]** remove sample IDs to ignore them in the analyses 
+ `gimble.bed`
    + **[Recommended]** intersect with BED regions of interest to analyse particular genomic regions, e.g:  
    ```
    bedtools intersect -a gimble.bed -b my_intergenic_regions.bed > gimble.intergenic.bed
    ``` 
    
#### Congratulations! You can now release the power of gimble on this dataset.
