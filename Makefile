.PHONY: pipenv poetry main

pipenv:
	cp config/$@/* .
	$@ shell

poetry:
	cp config/$@/* .
	$@ shell

main:
	cp script/$@.py .
	python3 $@.py
	rm $@.py
