[app]

# (string) Title of your application
title = Sudoku Warriors

# (string) Package name
package.name = sudokuwarriors

# (string) Package domain (needed for android package name)
package.domain = org.example

# (string) Source code directory
source.dir = .

# (list) Source files to include (Added asset extensions to prevent runtime asset loading crashes)
source.include_exts = py,png,jpg,kv,atlas,json,html,css,js,ttf,wav,mp3

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (string) Application version
version = 1.0.0

# (list) Application requirements 
# Includes flask for the logic loop and android for secure main UI thread handling
requirements = python3,hostpython3,kivy,pyjnius,flask,android

# (str) Supported orientations
orientation = portrait

# (int) Target Android API (Set to 34 to satisfy modern Google Play requirements)
android.api = 34

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use private data directory
android.private_storage = True

# (list) Architecture to build for
android.archs = arm64-v8a, armeabi-v7a

# (int) Log level (2 = standard debug output)
log_level = 2

# (int) Fill missing values with defaults if True
warn_on_root = 1

[buildozer]
