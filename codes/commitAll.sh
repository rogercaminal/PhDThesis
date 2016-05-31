#!/bin/bash

STRINGTOCOMMIT=""
for f in `/bin/ls -d */`; do
    STRINGTOCOMMIT+="$f "
done

svn commit -m "Commit all folders" $STRINGTOCOMMIT
