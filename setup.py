from setuptools import setup, find_packages

setup(
    name='django-facebook-photos',
    version=__import__('facebook_photos').__version__,
    description='Django implementation for Facebook Graph API Photos and Albums',
    long_description=open('README.md').read(),
    author='ramusus',
    author_email='ramusus@gmail.com',
    url='https://github.com/ramusus/django-facebook-photos',
    download_url='http://pypi.python.org/pypi/django-facebook-photos',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,  # because we're including media that Django needs
    install_requires=[
        'django-facebook-api>=0.6.7',
        'django-facebook-users>=0.1.0',
        'django-facebook-pages>=0.3.0',
        'django-m2m-history>=0.1.2',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
