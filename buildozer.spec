[app]
title = Billar Trazos
package.name = billartrazos
package.domain = org.diego
source.dir = .
source.include_exts = py,png,jpg,kv
version = 0.1
requirements = python3,kivy,pyjnius,android
orientation = portrait
fullscreen = 0
android.permissions = SYSTEM_ALERT_WINDOW
android.api = 34
android.minapi = 26
android.archs = arm64-v8a
android.add_src = javasrc
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
