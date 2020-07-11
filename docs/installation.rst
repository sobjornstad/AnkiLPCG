============
Installation
============

From AnkiWeb
============

Most users will want to install LPCG through AnkiWeb.
This is the easiest method, and it lets you get updates automatically.

You can find LPCG on `its AnkiWeb page <https://ankiweb.net/shared/info/2084557901>`_,
which will show instructions for completing the installation.
LPCG, like Anki, is licensed under the `GNU AGPL3`_ license.

.. _GNU AGPL3: http://www.gnu.org/licenses/agpl.html


From source
===========

If you want to do development on LPCG, you can install it from source.
The source is available `at GitHub`_.

1. Clone the Git repository.
#. Create a virtual environment with ``python -m venv venv``,
   and activate it (usually ``. venv/bin/activate``).
#. Install Python dependencies with ``pip install -r requirements.txt``.
   LPCG is tested on Python 3.7 but will probably work on 3.6 or 3.8 too.
#. Ensure you have PyQt5 and the ``pyuic5`` command available.
#. Run ``make`` to generate code for the dialog from Qt Designer
   (among other things).

To run the add-on within Anki,
symlink or move the ``src`` directory into your Anki add-ons directory.
Running ``pytest`` from the root directory will run the unit tests.

.. _at GitHub: https://github.com/sobjornstad/AnkiLPCG
