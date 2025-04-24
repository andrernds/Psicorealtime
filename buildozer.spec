[app]
title = MenteClara
package.name = menteclara
package.domain = org.menteclara
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
requirements = python3,kivy,matplotlib,reportlab
orientation = portrait
fullscreen = 1

# Para permitir salvar arquivos (PDF) e gráficos
android.permissions = WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.minapi = 21

# Arquivos a incluir no APK
include_patterns = *.png,*.json,*.ttf

# Ícone e banner (opcional)
icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1
