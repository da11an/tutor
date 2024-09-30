from setuptools import setup, find_packages

setup(
    name='math_tutor',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'egghunt=math_tutor.cli.egghunt:main',
            'reviewfacts=math_tutor.cli.review_factfamily:review_fact_family'
        ],
    },
    description='A package to help anyone learn math facts',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Dallan Prince',
    author_email='dallan.prince@gmail.com',
    license='MIT',
    url='https://github.com/da11an/tutor',
    classifiers=[
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    test_suite='tests',
    tests_require=['unittest'],
    )
