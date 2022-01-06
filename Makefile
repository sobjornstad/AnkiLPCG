.PHONY: all addon docs forms clean

all: docs forms addon
docs:
	$(MAKE) -C docs html
forms: src/import_dialog5.py src/import_dialog6.py
addon: build.ankiaddon

src/import_dialog5.py: designer/import_dialog.ui 
	pyuic5 $^ > $@

src/import_dialog6.py: designer/import_dialog.ui 
	pyuic6 $^ > $@

build.ankiaddon: src/*
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
	rm -f build.ankiaddon
