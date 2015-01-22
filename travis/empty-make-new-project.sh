#!/bin/bash -e

cd /tmp/test/

RESULT=$(make $* 2>&1 | tail -n +4)

echo ${RESULT}

if [ "${RESULT}" != "" ]
then
    echo A Rule is running again
    make $*
    exit 1
fi
