from setuptools import setup, find_packages
import os

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name="todo_notifs",
	version="0.0.1dev",
	description="todo notifier",
	long_description=read('README.md'),
	author="mingmeih",
	author_email="mingmeihuang1@gmail.com",
	license="GPLv3",
	packages=find_packages(),
	python_requires=">=3",
	install_requires = [
		'python-dateutil',
		'PyQt5'
	],
	entry_points = {
		"console_scripts" : [
			"notifier = todo_notifs.__main__:main",
		],
		"gui_scripts" : [
			"todo_list = todo_notifs.gui.__main__:main"
		]		
	},
)