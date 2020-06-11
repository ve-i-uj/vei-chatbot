from setuptools import setup, find_packages

setup(
    name='vei-chatbot',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    description=('A chat bot.'),
    long_description=open('README.md', encoding='utf-8').read(),
    install_requires=[
        'transitions',
        'enum34',
        'python-telegram-bot',
        'attrs',
    ],
    url='',
    author='Aleksei Burov',
    zip_safe=False
)
