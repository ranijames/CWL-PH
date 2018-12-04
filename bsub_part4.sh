bsub -M 80000 -W 48:00 -R rusage[mem=80000] -J part3 -o part3.job sh part3_job.sh
