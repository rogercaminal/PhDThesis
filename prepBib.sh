#!/bin/bash
cp Bibliography/myBib.bib saveBib.bib
sed 's/ü/\\"u/g' <saveBib.bib >Bibliography/myBib.bib
cp Bibliography/myBib.bib saveBib.bib
sed 's/ö/\\"u/g' <saveBib.bib >Bibliography/myBib.bib
cp Bibliography/myBib.bib saveBib.bib
sed 's/ä/\\"u/g' <saveBib.bib >Bibliography/myBib.bib
cp Bibliography/myBib.bib saveBib.bib
sed 's/ß/\\ss/g' <saveBib.bib >Bibliography/myBib.bib
cp Bibliography/myBib.bib saveBib.bib
sed 's/The D0 Coll/The D\O~Coll/g' <saveBib.bib >Bibliography/myBib.bib
cp Bibliography/myBib.bib saveBib.bib
sed 's/howpublished = {{\(.*\)}/howpublished = {\\url{\1}/g'  < saveBib.bib > Bibliography/myBib.bib
cp Bibliography/myBib.bib saveBib.bib
sed 's/howpublished = {h\(.*\)/howpublished = {\\url{h\1}/g' < saveBib.bib > Bibliography/myBib.bib
rm saveBib.bib

