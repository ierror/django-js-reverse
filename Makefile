export DJANGO_SETTINGS_MODULE = django_js_reverse.tests.settings
export PYTHONPATH := $(shell pwd)

test:
	pip install -r django_js_reverse/tests/requirements.txt
	flake8 --ignore=W801,E128,E501,W402 django_js_reverse --exclude=django_js_reverse/rjsmin.py
	coverage erase
	tox
	coverage combine
	coverage report
	coverage erase

release: clean
	git checkout master
	git merge develop -m "bump v$(VERSION)"
	git push origin master
	git tag v$(VERSION)
	git push origin v$(VERSION)
	pip install wheel
	python setup.py sdist bdist_wheel upload --sign --identity=99C3C059
	git checkout develop

optimizing_imports:
	pip install -r django_js_reverse/tests/requirements.txt
	isort -rc *.py
	isort -rc django_js_reverse/tests/
	isort -rc django_js_reverse/

clean:
	rm -rf build dist django_js_reverse.egg-info
