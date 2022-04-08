
SVG_FILES := $(wildcard figures/*.svg)
PDF_FILES := $(patsubst %.svg, %.pdf, $(SVG_FILES))

all: $(PDF_FILES)
	pdflatex -shell-escape main.tex
	evince main.pdf

%.pdf : %.svg
	inkscape $<  -o $@ --export-type=pdf

clean:
	-rm *.toc *.nav *.log *.snm *.out *.aux
	-rm figs/*.pdf_tex figs/*.pdf
