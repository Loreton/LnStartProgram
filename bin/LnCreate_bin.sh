#!/bin/bash

# __author__  : 'Loreto Notarantonio'
# __version__ : '25-10-2017 11.36.31'

ACTION=$1
EXECUTE=
[[ "$ACTION" != "--GO" ]] && EXECUTE='echo'

       thisDir="$(dirname  "$(test -L "$0" && readlink "$0" || echo "$0")")"     # risolve anche eventuali LINK presenti sullo script
       thisDir=$(cd $(dirname "$thisDir"); pwd -P)/$(basename "$thisDir")        # GET AbsolutePath
        binDir=${thisDir%/.*}               # Remove /. finale (se esiste)
        prjDir=$(dirname "$binDir")
       prjName=$(basename "$prjDir")
      LnLibDir=$prjDir/LnLib
     sourceDir=$prjDir/Source
        outDIR="$binDir"


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
    zipFileName="$prjName_$(date +"%Y%m%d").zip"
    $EXECUTE zip -r --exclude='*.git*' ${outDIR}/${zipFileName} $LnLibDir/* $sourceDir/*
echo

# Creazione dello zip di DDNS nella directory ${outDIR}
# cd ${ProjectDir}
# echo
# echo "I am in directory:.. ${PWD}"
#     zipFileName="DDNS_$(date +"%Y%m%d").zip"
#     $EXECUTE zip -r --exclude='*.git*' --exclude='bin*' --exclude='conf*' ${outDIR}/${zipFileName} *
# echo
