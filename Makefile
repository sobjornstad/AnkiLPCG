.PHONY: all docs forms zip clean

all: docs forms zip
docs:
	$(MAKE) -C docs html
forms: src/import_dialog.py
zip: build.zip

src/import_dialog.py: designer/import_dialog.ui 
	pyuic5 $^ > $@

build.zip: src/*
	rm -f $@
	rm -f src/meta.json
	rm -rf src/__pycache__
	( cd src/; zip -r ../$@ * )

clean:
	make -C docs clean
	rm -f *.pyc
	rm -f src/*.pyc
	rm -f src/__pycache__
	rm -f src/import_dialog.py
	rm -f build.zip
