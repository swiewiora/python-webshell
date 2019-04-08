from setuptools import find_packages, setup

with open('README.md', 'r') as readme:
    long_description = readme.read()

setup(
    name='webshell',
    version='1.0',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'flask',
    ],
    author='Sebastian Wiewiora',
    author_email='sebawiewior@gmail.com',
    description='Flask application which allows the user to execute '
                'arbitrary shell commands on the remote web server via '
                'browser.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/swiewiora/python-webshell',
    license='MIT',
)
