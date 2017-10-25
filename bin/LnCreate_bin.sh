#!/bin/bash

# __author__  : 'Loreto Notarantonio'
# __version__ : '25-10-2017 11.57.51'

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

# Creazione della LnPythonLib_YYYYMMDD.zip nella directory ${outDIR}
cd ${prjDir}
echo
echo "I am in directory:.. ${PWD}"
    zipFileName="${prjName}_$(date +"%Y%m%d").zip"
    CMD="zip -r --exclude='*.git*' ${outDIR}/${zipFileName} $LnLibDir $sourceDir __main__.py"
    if [[ "$ACTION" == "--GO" ]]; then
        # $EXECUTE zip -r --exclude='*.git*' ${outDIR}/${zipFileName} $LnLibDir $sourceDir
        echo $CMD
        eval $CMD
    else
        echo $CMD
    fi
echo


# Creazione dello zip di DDNS nella directory ${outDIR}
# cd ${ProjectDir}
# echo
# echo "I am in directory:.. ${PWD}"
#     zipFileName="DDNS_$(date +"%Y%m%d").zip"
#     $EXECUTE zip -r --exclude='*.git*' --exclude='bin*' --exclude='conf*' ${outDIR}/${zipFileName} *
# echo
