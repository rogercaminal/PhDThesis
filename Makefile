#!/bin/bash
FILE=thesis
#COMPILATION=latex
COMPILATION=pdflatex

all: $(FILE).tex
#	./prepBib.sh
	${COMPILATION} ${FILE}.tex
#	feynmf ${FILE}.tex
	bibtex ${FILE}
	${COMPILATION} ${FILE}.tex
	${COMPILATION} ${FILE}.tex
	rm -rf */*.pdf

spell: 
	for f in $( ls */*.tex ); do aspell -c $f; done

ps: $(FILE).dvi
	dvips ${FILE}.dvi

pdf: $(FILE).dvi
	dvipdf ${FILE}.dvi

clean:
	rm -rf *.aux */*.aux */*/*-eps-converted-to.pdf *.pdf *.dvi *.out *.lot *.log *.lof *blg *.bbl *.toc
