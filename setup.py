from setuptools import setup, find_packages


def get_version():
    with open('picombo/__init__.py', 'r') as file:
        for line in file:
            if line.startswith('__version__'):
                return line.split("'")[1]
    raise RuntimeError('Unable to find version string.')


setup(
    name='picombo',
    version=get_version(),
    author='Udon Asakawa',
    author_email='udonuopn.a@gmail.com',
    description='Users select an item from a list and retrieve it.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/udonuopn/picombo',
    packages=find_packages(),
    install_requires=[
        'prompt-toolkit'
    ],
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)