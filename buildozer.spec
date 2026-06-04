[app]

# (string) Title of your application
title = Sudoku Warriors

# (string) Package name
package.name = sudokuwarriors

# (string) Package domain (needed for android package name)
package.domain = org.example

# (string) Source code directory
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,json,html,css,js

# (string) Application version
version = 1.0.0

# (list) Application requirements
# Added pyjnius explicitly to fix the backend dependency error
requirements = python3,kivy,pyjnius

# (str) Supported orientations
orientation = portrait

# (int) Target Android API
android.api = 33

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
