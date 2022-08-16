.PHONY: pipenv poetry dam_break naca_airfoil

pipenv:
	cp config/$@/* .
	$@ shell

poetry:
	cp config/$@/* .
	$@ shell

dam_break:
	cp script/$@.py .
	python3 $@.py
	rm $@.py

naca_airfoil:
	cp script/$@.py .
	python3 $@.py
	rm $@.py
