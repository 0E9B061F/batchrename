from distutils.core import setup
import py2exe

icons = [('images', ['./icon16.png', './icon32.png', './icon64.png', './logo.png', './xquit.png'])]

setup(
	windows=[{
		'script': 'br.py',
		"icon_resources": [(1, "icon.ico")]
	}],
	data_files = icons
)
