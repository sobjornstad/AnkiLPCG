.PHONY: all docs forms zip clean

all: docs 6forms zip
docs:
	$(MAKE) -C docs html
forms: 5forms 6forms
#forms: src/import_dialog.py
5forms: $(patsubst designer/%_dialog.ui,src/%_dialog5.py,$(wildcard designer/*))
6forms: $(patsubst designer/%_dialog.ui,src/%_dialog6.py,$(wildcard designer/*))
zip: build.zip

src/import_dialog5.py: designer/import_dialog.ui
	pyuic5 $^ > $@

src/import_dialog6.py: designer/import_dialog.ui
	pyuic6 $^ > $@

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
