setup-pipenv: clean-pipenv
	pipenv install --dev

setup: setup-pipenv

clean:
	find . -iname __pycache__ | xargs rm -rf
	find . -iname '*.pyc' | xargs rm -f

clean-pipenv:
	pipenv --rm

clean-pypi:
	mkdir -p sdist eggs wheels
	find . -iname '*.egg' | xargs mv -t eggs
	find . -iname '*.whl' | xargs mv -t wheels
	find . -iname '*.tar.gz' | xargs mv -t sdist
	rm -rf build dist *.egg-info

dist-clean: clean clean-pypi

pypi-dist: clean-pypi
	python setup.py sdist bdist_wheel

update-pipenv:
	pipenv update
	pipenv install --dev
	pipenv clean

dist-upload: pypi-dist
	twine check dist/*
	twine upload dist/* -r pypi --skip-existing
	twine upload dist/* -r pypitest --skip-existing
