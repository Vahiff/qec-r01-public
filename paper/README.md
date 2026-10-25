# QEC-R01 manuscript source

Working scientific draft only. The author is identified as **Vahif Khalilov**; institutional affiliation has not been supplied and must be resolved before any arXiv submission. No external submission or endorsement has occurred.

## Local build

Requires pdfLaTeX, BibLaTeX and Biber (the classic `bibtex` executable is not used):

```sh
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
biber main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

`figures/` contains **unchanged copies** of two graphics originally generated in `../results/figures/`; arXiv source archives need to contain these images alongside `main.tex` and `references.bib`. The repository's experiment remains a code-capacity X-noise-only simulation. QuTiP was not executed. Full preregistered noise-grid and novelty evaluation are incomplete.

## Pre-submission gates (NOT VERIFIED)

- Author contribution statement, institutional affiliation (if applicable), explicit approval for release.
- Independent technical review and literature originality assessment.
- arXiv policies, category suitability, account endorsement (when applicable).
- Independently reproducible compilation in the arXiv TeX environment.

LaTeX and bibliography references were compiled locally. Do not equate local PDF success with arXiv acceptance.
