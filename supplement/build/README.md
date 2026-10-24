# Building the supplement

Inputs are the exported CSVs of the supplementary package (`<inputs>`).

```
python3 figs.py <inputs>        # new figures into ../figures (via out/figures)
python3 render.py <inputs>      # fills SUPPLEMENT.tmpl.md into SUPPLEMENT.md
pandoc SUPPLEMENT.md -f markdown-implicit_figures -o supplement.pdf --pdf-engine=pdflatex \
  --columns=1000 -V geometry:margin=2cm -V papersize=a4 -V fontsize=10pt -V fontfamily=libertine -H header.tex
```
