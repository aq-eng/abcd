
f5/%.py :
	python -i -c "__name__ = '__main__'; execfile('$*.py')"

# run unittest specific file 
f6/%.py :
	python -m unittest -v $*

# run unitest all files
f7 :
	python -m unittest discover -v --pattern="*.py"


clean :
	rm *.pyc
