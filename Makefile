.PHONY: commit dist release setup update

export PIPENV_VENV_IN_PROJECT=1

MESSAGE =
VERSION = $(shell grep "version" setup.py | sed "s/.*version='\(.*\)*'.*/\1/")
TAG     = v$(VERSION)

commit: git-commit
dist: dist-upload
release: git-tag
setup: setup-pipenv
update: git-pull update-pipenv

setup-pipenv: clean-pipenv
	pipenv install --dev

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

git-tag:
	git tag --sign $(TAG)
	git push --tag

git-pull:
	git pull

git-commit:
	git add .
	git commit --gpg-sign
	git push

github-release:
	go run github.com/aktau/github-release release \
		--user gousaiyang \
		--repo tbtrim \
		--tag $(TAG) \
		--name $(TAG) \
		--description $(MESSAGE)
