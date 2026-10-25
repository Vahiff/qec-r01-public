.PHONY: test build-pdf clean

test:
	python -m unittest discover -s tests -v

build-pdf:
	cd paper && pdflatex -interaction=nonstopmode main.tex && pdflatex -interaction=nonstopmode main.tex

clean:
	rm -rf paper/*.aux paper/*.log paper/*.out paper/*.bbl paper/*.blg __pycache__/* tests/__pycache__/*
