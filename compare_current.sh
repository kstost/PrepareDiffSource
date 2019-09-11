#!/bin/bash
# https://www.lesstif.com/pages/viewpage.action?pageId=26083916
if [ "$#" -eq 1 ]; then
    python prepare_diff_source.py kstost $(basename `pwd`) `pwd` $1
fi
