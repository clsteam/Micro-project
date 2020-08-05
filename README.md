# Raser
**A pipeline that automatically analyzes RNA-Seq data**
## Introduction
RNA-Seq is a new transcriptome research method, with high efficiency, high sensitivity, and full genome analysis (for any species without pre-designing probes) and other advantages. Currently, a variety of analysis tools have been developed for RNA-Seq data, including data preprocessing, sequence alignment, transcriptome assembly, gene expression estimation, and non-coding RNA detection. However, these analysis tools basically exist independently, lacking a relatively complete system to integrate different tools to complete most of the analysis.

Raser was born from this. He helps you realize most of the software installation-free configuration, parameter configuration, accurate management of multiple samples, complete log management for each sample, and some visualization tasks
## Installing Raser

Raser requires the following software and data resources to be installed. 
>Note, if you can use our [Docker](https://github.com/STAR-Fusion/STAR-Fusion/wiki#Docker)  images, then you'll have all the software pre-installed and can hit the ground running. 

###  1. Downloading from GitHub Clone
```
    $ git clone --recursive git@github.com:clsteam/RASER.git
    $ cd Raser
    $ chmod 744 raser-manager
```
The --recursive parameter is needed to integrate the required submodules.
>If necessary, you can add Raser to your environment variables, which will be handy for future use, like this:（*Add to ~/.bashrc will take effect permanently*）
>`export PATH=$PATH：/PATH_TO_RASER/`

###  2. Tools Required

 * Raser is developed based on Python 3.7 (if you have not installed it, you can go to the official Python website to download and install), you need to **enter the root directory of Raser** and run the following command to install the required Python dependency packages:

```
    $ pip3 install -r requirements.txt
```

* Raser packages most of the software in a separate folder, and users can use it after downloading, but some software needs to be manually installed and compiled:
    1. 

## Running Raser 
>Before running, please make sure that your running parameters are correct. Please check the configuration item for parameter configuration instructions.


* First of all, we can take a look at what are the command line parameters of Raser, you can enter the following code:
```
    $ raser-manager ve -i ./config.ini
```
* If you want to submit a task to run on the PBS server, you can add the `-s/--server` parameter:
```
    $ raser-manager ve -i ./config.ini -s
```
All parameter configurations are divided into configuration files to facilitate classified management and operation. You can enter `--help` to view other available command line parameters:
```
    $ raser-manager ve -i ./config.ini --help
    usage: raser-manager [-h] [-i INI] [-s] [-t]
                         [-l {spam,debug,verbose,info,notice,warning,success,error,critical}]
                         [-c] [-m]
                         {ve,pl}

    positional arguments:
      {ve,pl}               ve: vertebrate, pl: plant

    optional arguments:
      -h, --help            show this help message and exit
      -i INI, --ini INI     configuration file, default {RASER_HOME}/config.ini
      -s, --server          submit tasks to server compute nodes (PBS)
      -t, --test            for testing, only run a sample in the main process
      -l {spam,debug,verbose,info,notice,warning,success,error,critical}, --level {spam,debug,verbose,info,notice,warning,success,error,critical}
                            logger level
      -c, --comm            output the complete command submitted by the task
      -m, --sim             simplified process
```
example：

 ![image](http://i1.fuimg.com/724614/3775734b6c9882bd.png)
 
## Result
* After you complete the task submission, you can find your output log and results in your output directory:
```
.output_raser
├── allele
├── diff
├── assembly_gtf_list.txt
├── fusion
│   └── tophatfusion
│       └── bam
├── lnc_potential.gtf
├── lncrna.gtf
├── log
│   ├── pipe (the log file of each process or sample, named after the sample)
│   │   ├── SRR196226.e
│   │   ├── SRR196226.o
│   │   ├── SRR196227.e
│   │   ├── SRR196227.o
│   │   ├── SRR196228.e
│   │   ├── SRR196228.o
│   │   ├── SRR196229.e
│   │   ├── SRR196229.o
│   │   ├── SRR196230.e
│   │   ├── SRR196230.o
│   │   ├── SRR196231.e
│   │   └── SRR196231.o
│   ├── RASERCMD (record all commands run by Raser)
│   ├── raser-PRJNA142905.e2538136 (main process log file)
│   ├── raser-PRJNA142905.o2538136
│   ├── single.e (additional log file in other languages such as R)
│   └── single.o
├── merged.gtf
├── ncRNA_out
│   ├── cnci
│   │   ├── ambiguous_genes.gtf
│   │   ├── compare_2_infor.txt
│   │   ├── filter_out_noncoding.gtf
│   │   ├── novel_coding.gtf
│   │   └── novel_lincRNA.gtf
│   ├── CNCI.index
│   ├── CPC.txt
│   ├── lnc.fasta
│   ├── lncfinder.R
│   └── lnc_predict.statistics
├── origin.annotated.gtf
├── origin.loci
├── origin.merged.gtf.refmap
├── origin.merged.gtf.tmap
├── origin.stats
└── origin.tracking
```
* Output folder structure of each sample
```
.ERR315326
├── alter_splice_out
│   ├── prefix_1.combined.gtf
│   ├── prefix_1.loci
│   ├── prefix_1.redundant.gtf
│   ├── prefix_1.stats
│   ├── prefix_1.tracking
│   ├── prefix_2.as.nr
│   ├── prefix_2.as.summary
│   ├── ERR315326.xfpkm
│   └── total.as
├── ERR315326_1_clean.fq.gz
├── ERR315326_2_clean.fq.gz
├── ERR315326.bam
├── ERR315326.bam.bai
├── ERR315326.counts
├── ERR315326.counts.summary
├── ERR315326.lnc.counts
├── ERR315326.lnc.counts.summary
├── fastqc_out
│   ├── adapter.fa
│   ├── ERR315326_1_clean_fastqc.html
│   ├── ERR315326_1_fastqc.html
│   ├── ERR315326_2_clean_fastqc.html
│   └── ERR315326_2_fastqc.html
├── tophat_out
│   └── align_summary.txt
├── transcript_out
│   └── transcripts.gtf
├── tree.MD
└── variation_out
    ├── ERR315326.vcf.gz
    ├── ERR315326.vcf.gz.tbi
    ├── org.vcf.gz
    └── org.vcf.gz.tbi
```


## Configuration
#### * Raser将所有的软件运行参数都放入了配置文件中，分成两个部分，一个是`raser/setting.py`，宁外一个是`config.ini`:
##### 1. `config.ini` (main configuration file) is designed to control the process, add samples, and modify tool parameters**
```
[Root]
;require, Raser's output directory
path = /home/output_raser

[Cluster]
;Optional, the parameter items of the task submitted by the PBS server (task name, node, total number of threads, total time limit)
name = pop23
nodes = comput9
ppn = 24
walltime = 200:00:00

[Resource]
; Require, the number of running processes
pools = 6

[Workflow]
; Require, select the project module that needs to be run
differentialexpression = True
allele = True
altersplice = False
fusion = False
lncrna = False

[SampleDir]
; Require, sample name and dictionary
SRP028829=
	/home/populus/SRP028829
	/home/populus/SRP028830
SRP033639=
	/home/populus/SRP033639

[SampleMessage]
; Species, sample sequencing information (phred, library_type)
;require, such as humo
species = populus

;optional, phred33 or phred64
phred =
;optional, fr-unstranded, fr-firststrand or fr-secondstrand
library_type =

[Treatment]
;Optional, sample phenotype
header_name = Run,Treatment
file = /home/populus/treat.csv

[Genome]
home_dir = /home/populus
;require, genome file
genomefile = ${home_dir}/GCF_000495115.1_PopEup_1.0_genomic.fa
;Optional, genome reference annotation file
annotations = ${home_dir}/GCF_000495115.1_PopEup_1.0_genomic.gff
;Optional, index file (if the index has been established, Raser skips this step by default, which can greatly reduce the running time)
bowtie1_index = ${home_dir}/hg_bowtie1
bowtie2_index = ${home_dir}/GCF_000495115.1_PopEup_1.0_genomic
hisat2_index = ${home_dir}/GCF_000495115.1_PopEup_1.0_genomic_hisat2
star_index =
annotations_gtf =
hisat2_splicesites_txt =
bed = ${home_dir}/GCF_000495115.1_PopEup_1.0_genomic.bed
hdrs = ${home_dir}/GCF_000495115.1_PopEup_1.0_genomic.fa.hdrs

[Lncrna]
;Optional, LncRna reference notes and selection criteria
known_lncrna_gtf =
min_length = 200
min_cov = 0
min_fpkm = 0

[Fusion]
;Optional, STAR-Fusion configuration item
starfusion_genome_resource_lib = /home/tools/STAR-Fusion-extra-files/populus/ctat_genome_lib_build_dir

[Allele]
;optional,
; dbsnp, used to annotate snp while calling snp
dbsnp =
; list of sites to blacklist from phasing. The file we are providing contains all HLA genes.
hla_bed =
; list of sites to blacklist when generating allelic counts. These are sites that we have previously identified as having mapping bias, so excluding them will improve results.
haplo_count_bed =
```
**SampleDir:**

* Add sample folders for the experimental group and control group. Each group can have 0 or more folders. Each folder stores sample files. You can also use LUNX regular recursive folders (for example, /home/populus/SRP028829/*). The file format supports .fastq, .fq, .sra files and their gz compression format.
ps: Double-ended data identification is unified as **_1.[fq|fastq][|.gz]** and **_2.[fq|fastq][|.gz]**.

    
##### 2. `raser/setting.py` aims to select analysis tools
```
# The tool is used as a guideline
# All strings must be lowercase
TOOLS_SELECTED = {
    "qualitycontrol": "fastqc",
    "trim": "trimmomatic",
    "alignment": "tophat2",  # tophat2, hisat2, star
    "rmdup": "samtools", # samtools, picard
    "genecount": "featurecounts",  # htseq, featurecounts, star
    "strandspecific": "",   # rseqc
    "transcript": "stringtie",  # cufflinks, stringtie
    "variation": "gatk",  # samtools, gatk
    "differentialexpression": "deseq2",  # ballgown, deseq2, edger
    "altersplice": "asprofile",  # asprofile
    "fusion": "tophatfusion",  # tophatfusion, starfusion
    "lncrna": "cc",  # cc
    "allele": "phaser",  # phaser
}
# Reads the minimum length reserved
MINLEN = 50
# default Read-Group platform (e.g. ILLUMINA, SOLID, LS454, HELICOS and PACBIO)
RGPL = "ILLUMINA"
# Whether to use GTF format as the first choice for the process, the default is False (GTF compatibility is better, especially when STAR builds indexes)
PRIMARY_GTF_ANNOTATIONS = False
# The quality of one end of the double-ended data sheet is very poor, and the high-quality end can be reserved for single-ended analysis
WHETHER_PE_TO_SE = True
# Whether to add a reference comment when comparing, the default is True
WHETHER_ALIGNMENT_WITH_ANNOTATIONS = True
# Keep only marking or removing PCR repeats (only valid for picard), the default is True
WHETHER_MARK_DUPLICATES_ONLY = True
# Automatically detect the chain specificity and use it, the default is False (it will take a lot of time to compare again)
STRAND_SPECIFIC_USE_AUTOMATICALLY = False
# Even if there is no control sample, compulsory assembly of transcripts, default False
ENFORCE_ASSEMBLY = False
```

