.PHONY: test build-pdf clean

test:
	python -m unittest discover -s tests -v

build-pdf:
	cd paper && pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex && biber main && pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex && pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
	cd paper && pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error SI.tex && pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error SI.tex

clean:
	rm -rf paper/*.aux paper/*.log paper/*.out paper/*.bbl paper/*.blg __pycache__/* tests/__pycache__/*
