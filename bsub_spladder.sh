bsub -M 80000 -W 48:00 -R rusage[mem=80000] -J *.yml -o *.yml.job sh *.yml.sh
