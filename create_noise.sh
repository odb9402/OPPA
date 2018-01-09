# This script create noise on the bam file randomly.
# For instance, you can call this script like 
# "craete_noise target.bam control.bam result.bam noiselevel"

bamtools index -in $2 
bamtools index -in $1
bamtools random -in $2 -out temp.bam -n $4
bamtools merge -in $1 -in temp.bam -out $3
rm temp.bam
