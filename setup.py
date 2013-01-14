from distutils.core import setup, Extension

ext_modules = [Extension("cvardict",
	["cvardict/cvardict.c", "cvardict/cvshm.c"],
	libraries = ["rt"]
)]

setup(name = "purpledefrag",
	version = "0.1",
	packages = [
		"purpledefrag",
		"purpledefrag.q3df",
		"purpledefrag.app",
		"purpledefrag.app.controllers",
		"purpledefrag.app.models"
	],
	ext_package = "purpledefrag",
	ext_modules = ext_modules
)
