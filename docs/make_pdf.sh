rm -rf ./build/
make html
open ./build/html/index.html
make latex
cd ./build/latex/
xelatex *.tex
open *.pdf
cd -
