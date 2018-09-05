XELATEX=xelatex -file-line-error -interaction=nonstopmode

.PHONY: all
all: thesis-letomes.tex
	latexmk -pdf -pdflatex="$(XELATEX)" -use-make thesis-letomes.tex

.PHONY: auto
auto: thesis-letomes.tex
	latexmk -pdf -pdflatex="$(XELATEX)" -use-make -pvc thesis-letomes.tex

.PHONY: clean
clean:
	rm -f thesis-letomes.pdf *.aux *.bbl *bcf *.blg *.log *.out *.tdo *.toc *.xdv *.synctex.gz *.fdb_latexmk *.fls *.run.xml; \
	rm -f **/*.aux
