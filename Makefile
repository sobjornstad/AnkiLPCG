.PHONY: all forms zip clean

all: forms zip
forms: lpcg/import_dialog.py
zip: build.zip

lpcg/import_dialog.py: designer/import_dialog.ui 
	pyuic4 $^ > $@

build.zip: lpcg/* LPCG.py
	rm -f $@
	zip -r $@ lpcg/ LPCG.py

clean:
	rm -f *.pyc
	rm -f lpcg/*.pyc
	rm -f lpcg/import_dialog.py
	rm -f build.zip
