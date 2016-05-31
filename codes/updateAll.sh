#!/bin/bash

STRINGTOCOMMIT=""
for f in `/bin/ls -d */`; do
    STRINGTOCOMMIT+="$f "
done

svn update  $STRINGTOCOMMIT
