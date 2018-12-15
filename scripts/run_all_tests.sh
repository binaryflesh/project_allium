cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"/../tests/

if test "$OSTYPE" == "win32"; then
	python master_test.py
elif test "$OSTYPE" == "win64" ; then
	python master_test.py
else
	python3 master_test.py

fi