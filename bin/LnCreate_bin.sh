#!/bin/bash

# __author__  : 'Loreto Notarantonio'
# __version__ : '07-11-2017 15.16.40'

ACTION=$1



       thisDir="$(dirname  "$(test -L "$0" && readlink "$0" || echo "$0")")"     # risolve anche eventuali LINK presenti sullo script
       thisDir=$(cd $(dirname "$thisDir"); pwd -P)/$(basename "$thisDir")        # GET AbsolutePath
        binDir=${thisDir%/.*}               # Remove /. finale (se esiste)
        prjDir=$(dirname "$binDir")
       prjName=$(basename "$prjDir")
      LnLibDir='./LnLib'
     sourceDir='./Source'
        outDIR='./bin'


    echo
    echo "    prjName   : $prjName"
    echo
    echo "    thisDir   : $thisDir"
    echo "    binDir    : $binDir"
    echo "    prjDir    : $prjDir"
    echo
    echo "    LnLibDir  : $LnLibDir"
    echo "    sourceDir : $sourceDir"
    echo
    echo "    outDIR    : $outDIR"

# Creazione della Project_YYYYMMDD.zip nella directory ${outDIR}
cd ${prjDir}
echo
echo "I am in directory:.. ${PWD}"
    zipFileName="${prjName}_$(date +"%Y%m%d").zip"
    CMD="zip -r --exclude='*.git*' --exclude='*/__pycache__/*' ${outDIR}/${zipFileName} $sourceDir __main__.py"
    if [[ "$ACTION" == "--GO" ]]; then
        # $EXECUTE zip -r --exclude='*.git*' ${outDIR}/${zipFileName} $LnLibDir $sourceDir
        echo $CMD
        eval $CMD
    else
        echo $CMD
        echo
        echo "immettere --GO per eseguire"
    fi
echo



# Creazione della LnLib_YYYYMMDD.zip nella directory ${outDIR}
# cd ${prjDir}
echo
echo "I am in directory:.. ${PWD}"
    zipFileName="LnLib_$(date +"%Y%m%d").zip"
    CMD="zip -r --exclude='*.git*' --exclude='*/__pycache__/*' ${outDIR}/${zipFileName} $LnLibDir __main__.py"
    if [[ "$ACTION" == "--GO" ]]; then
        # $EXECUTE zip -r --exclude='*.git*' ${outDIR}/${zipFileName} $LnLibDir $sourceDir
        echo $CMD
        eval $CMD
    else
        echo $CMD
        echo
        echo "immettere --GO per eseguire"
    fi
echo



