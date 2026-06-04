[app]
title = Sudoku Warriors
package.name = sudokuwarriors
package.domain = org.sudokuwarriors

# Source code location and file extensions to include
source.dir = .
source.include_exts = py,html,css,js

# Critical Python dependencies for your engine
requirements = python3,flask,jinja2,werkzeug,itsdangerous,click

# Target Android settings
orientation = portrait
fullscreen = 1
android.permissions = INTERNET

# Tells Buildozer to use a webview layout to display your Flask templates
bootstrap = webview

