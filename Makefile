tables:
	cat tools/document_begin.txt > main_tables.tex
	bash tables.sh  >> main_tables.tex
	cat temp_tables.tex >> main_tables.tex
	rm temp_tables.tex
	cat tools/document_end.txt >> main_tables.tex
	pdflatex main_tables.tex -o main_tables.pdf