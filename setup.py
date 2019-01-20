from setuptools import find_packages, setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name='django-db-auto-create',
    version='0.1.0',
    license='MIT',
    description='Automatically create database on migrate.',
    long_description=readme(),
    keywords='django db create',
    author='Vacasa, LLC',
    author_email='opensource@vacasa.com',
    url='https://github.com/Vacasa/django-db-auto-create',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    install_requires=[
        'django',
    ],
    zip_safe=False
)
