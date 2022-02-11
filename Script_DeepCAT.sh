#!/bin/bash -f

#args:
#    datatype: either -t or -r (-r indicates raw data from immuneanalyzer website)
#    input_dir: input directory
#    job_name: name of job as a string
#    raw_version: either v1 or v2, indicating version of raw data from immuneanalyzer export
#e.g.
#    ./Script_DeepCAT.sh -r ~/work/ucl/bigdata/ucl.projects/deepcat/test testjob v1


# If raw TCR repertoire sequencing data are available please place data 
# in the "Input" folder
var1="Output"
# If raw TCR repertoire sequencing data are not available 
# please use our Sample Data as an example 
#python DeepCAT_modif.py $var3  $var4   
var2="iSMART_results"
var3="DeepCAT_CHKP"

args=("$@")
job_name=${args[2]}
raw_version=${args[3]}

echo job_name: $job_name
echo raw_version: $raw_version

if [ ! -d "DeepCAT_CHKP/" ]; then
    echo "Directory DeepCAT_CHKP DOES NOT exists. Please unzip  DeepCAT_CHKP.zip file"
else
    mkdir jobs/$job_name
    mkdir jobs/$job_name/Output
    mkdir jobs/$job_name/iSMART_results
    if [ ${args[0]} == '-r' ]; then
        if [ "$(ls -A ${args[1]})" ]; then
            if [ ! -d $var2 ]; then
                mkdir $var2
            fi
            echo "Running PrepareAdaptiveFile.py"
            if [ $raw_version == 'v2' ]; then
                python PrepareAdaptiveFile.py ${args[1]} jobs/$job_name/Output
            elif [ $raw_version == 'v1' ]; then
                python PrepareAdaptiveFile.py ${args[1]} jobs/$job_name/Output r1
            fi
            echo "Running iSMARTm.py"
            python iSMARTm.py -d jobs/$job_name/Output -o jobs/$job_name/iSMART_results
        else
            echo "Error! The" ${args[1]} "directory is empty"
            exit 1
        fi   
        args[0]='-r'
    elif [ ${args[0]} == '-t' ]; then
        var2=${args[1]}
    fi  
    python DeepCAT.py jobs/$job_name/iSMART_results $var3 ${args[0]} $job_name
fi
