# Utility scripts
## GTF Parser

Either performs proper sorting of GTF for PrimerSeq or checks if GTF is sorted.
Note - The "score" field is parsed as a float and if it fails the str to float conversion then a value of 0.0 is assigned to it.

For Sorting GTF: 
```python gtf_parser.py -i GTF_FILE_PATH -o OUTPUT_FILE_PATH -v VARIABLES_TO_SORT_BY(default: start position)```

For checking if GTF is sorted:  
```python gtf_parser.py -c GTF_FILE_PATH -v VARIABLES_TO_SORT_BY```


#### Arguments:
   
    -h, --help    show the help message and exit
    -i GTF/GFF    Path to gtf file to sort
    -f FileType   Valid options are 'gff' or 'gtf', default 'gtf'
    -o OUTPUT     Path name of properly sorted gtf
    -c IS_SORTED  Path to gtf file to check if sorted correctly
    -v SORT_VARS  Comma separated list of vaiables to sort by, in the order that
                  is desired. Attributes to be used should be mentioned after
                  the key word attributes separated by a ":" and separated by a
                  semicolon. For example -
    
                  start,source,attributes:gene_id;transcript_id



## Job Handler

Has a few useful methods to submitting and interrogate PBS jobs

*submit_job* - Submits a job to the cluster and returns the job ID
* *isRunning* - Takes a job ID as input and returns True if the job is running else returns False
* *get_job_status* - Takes a job ID as input and returns the job status (R,H,C)
* *multiple_jobs_completed* - Takes a list of job IDs and returns True if all of them are completed/cancelled and False if even one is running.

## Run Tests

```
cd tests
nosetests
```
