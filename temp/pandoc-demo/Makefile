all: pdf latex html md

pdf:
	pandoc --number-sections -t latex --filter pandoc-crossref default.yaml -o output.pdf demo.md
	pandoc --number-sections -t latex --filter pandoc-crossref default.yaml -o output-chapters.pdf demo.md --top-level-division=chapter
	pandoc --number-sections -t latex --filter pandoc-crossref default.yaml -o output-cref.pdf demo.md -M cref=True
	pandoc --number-sections -t latex --filter pandoc-crossref default.yaml -o output-listings.pdf demo.md -M listings --listings

latex:
	pandoc --number-sections -t latex --filter pandoc-crossref default.yaml -o output.latex demo.md
	pandoc --number-sections -t latex --filter pandoc-crossref default.yaml -o output-chapters.latex demo.md --top-level-division=chapter
	pandoc --number-sections -t latex --filter pandoc-crossref default.yaml -o output-cref.latex demo.md -M cref=True
	pandoc --number-sections -t latex --filter pandoc-crossref default.yaml -o output-listings.latex demo.md -M listings --listings

html:
	pandoc --number-sections -s -t html --filter pandoc-crossref default.yaml -o output.html demo.md
	pandoc --number-sections -s -t html --filter pandoc-crossref default.yaml -o output-chapters.html demo.md -M chapters=True

md:
	pandoc --number-sections -t markdown --filter pandoc-crossref default.yaml -o output.md demo.md
	pandoc --number-sections -t markdown --filter pandoc-crossref default.yaml -o output-chapters.md demo.md -M chapters=True
