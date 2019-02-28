from io import open

from setuptools import setup

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='tbtrim',
    version='0.2.1',
    description='A utility to trim Python traceback information.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gousaiyang/tbtrim',
    author='Saiyang Gou',
    author_email='gousaiyang223@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
    ],
    keywords='traceback trim exception excepthook',
    py_modules=['tbtrim'],
)
