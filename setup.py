from setuptools import setup, find_packages

setup(
    name='chatbot',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    description=('A chat bot.'),
    long_description=open('README.md', encoding='utf-8').read(),
    install_requires=[
        'transitions',
    ],
    url='',
    author='Aleksei Burov',
    author_email='burov_alexey@mail.ru',
    zip_safe=False
)
