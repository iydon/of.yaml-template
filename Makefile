.PHONY: main

main:
	cp script/$@.py .
	python3 $@.py
	rm $@.py
