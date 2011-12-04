#!/bin/sh

MIN=1
MAX=12000

for i in `seq $MIN $MAX`
do
  wget -q "http://www0.parlamento.gub.uy/htmlstat/pl/legisl/fotos/Fot`printf %05d $i`.jpg"
done

rm `grep 'lica Oriental del Uruguay' *.jpg | cut -d: -f1`
