from setuptools import setup

with open('README.rst', 'rb') as f:
    long_description = f.read().decode('utf-8')

setup(
    name='tbtrim',
    version='0.1.0.post1',
    description='A utility to trim Python traceback information.',
    long_description=long_description,
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
    ],
    keywords='traceback',
    py_modules=['tbtrim'],
)
