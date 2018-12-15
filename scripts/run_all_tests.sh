cd "$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"/../tests/
for f in *.py
do
	if test "${f##*/}" != "master_test.py"
	then
		python3 "$f"
	fi
done