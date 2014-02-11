from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-comments',
	version=version,
	description="Adds comments to 'things' in CKAN",
	long_description="""\
	""",
	classifiers=[],
	keywords='',
	author='Ross Jones',
	author_email='ross@servercode.co.uk',
	url='http://github.com/rossjones/ckanext-comments',
	license='',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	namespace_packages=['ckanext', 'ckanext.comments'],
	include_package_data=True,
	zip_safe=False,
	dependency_links = ['https://github.com/datagovuk/mollom/tarball/xmlrpc#egg=mollom'],
	install_requires=[
		'requests',
		'nose',
		'nose-timer',
		'mollom'
	],
	entry_points=\
	"""
        [ckan.plugins]
	    # Add plugins here
	    comments=ckanext.comments.plugin:CommentsPlugin

        [paste.paster_command]
        initdb = ckanext.comments.command:InitDBCommand
        import = ckanext.comments.command:XMLImport
	""",
)
