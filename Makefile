.PHONY: pipenv poetry naca_airfoil

pipenv:
	cp config/$@/* .
	$@ shell

poetry:
	cp config/$@/* .
	$@ shell

naca_airfoil:
	cp script/$@.py .
	python3 $@.py
	rm $@.py
