export LC_CTYPE=C 
export LANG=C

DIRECTORY="Interpretations/Figures/"

for f in `/bin/ls $DIRECTORY/*.eps`; do
  if grep -q "Internal" "$f"; then 
    echo $f
    sed -i "" "s/Internal//g" $DIRECTORYT$f
    sed -i "" "s/ATLAS/R. Caminal - PhD Thesis/g" $DIRECTORYT$f
  fi
  if grep -q "Work in progress" "$f"; then 
    echo $f
    sed -i "" "s/Work in progress//g" $DIRECTORYT$f
    sed -i "" "s/ATLAS/R. Caminal - PhD Thesis/g" $DIRECTORYT$f
  fi
done
