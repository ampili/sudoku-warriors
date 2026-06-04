[app]

# (string) Title of your application
title = Sudoku Warriors

# (string) Package name
package.name = sudokuwarriors

# (string) Package domain (needed for android package name)
package.domain = org.example

# (string) Source code directory
source.dir = .

# (list) Source files to include (let's include common web/app assets)
source.include_exts = py,png,jpg,kv,atlas,json,html,css,js

# (string) Application version (Fixed the missing version error)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Supported orientations (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use private data directory (True), or public (False)
android.private_storage = True

# (list) Architecture to build for (Flattened for standard modern devices)
android.archs = arm64-v8a, armeabi-v7a

# (int) Anywhere from 0 to 2. 0 is silent, 1 is info, 2 is debug (specify full output)
log_level = 2

# (int) Fill missing values with defaults if True
warn_on_root = 1

[buildozer]
