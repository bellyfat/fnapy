#
# Makefile
# , 2016-08-24 15:38
#

test:
	pytest -v test_client.py


clean:
	rm -f *.pyc


.PHONY: clean

# vim:ft=make