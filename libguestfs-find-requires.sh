#!/bin/sh -
# Additional custom requires for libguestfs package.

original_find_requires="$1"
shift

# Get the list of files.
files=`sed "s/['\"]/\\\&/g"`

# Use ordinary find-requires first.
echo $files | tr [:blank:] '\n' | $original_find_requires

# Is supermin.d/hostfiles included in the list of files?
hostfiles=`echo $files | tr [:blank:] '\n' | grep 'supermin\.d/hostfiles$'`

if [ -z "$hostfiles" ]; then
    exit 0
fi

# Generate extra requires for libraries listed in hostfiles.
sofiles=`grep 'lib.*\.so\.' $hostfiles | fgrep -v '*' | sed 's|^\.||'`
for f in $sofiles; do
    if [ -f "$f" ]; then
        echo "$f"
    fi
done
