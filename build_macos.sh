#!/usr/bin/env bash
# Genera la aplicación de macOS y el paquete para compartir.
# Nombre visible: Investigación de Operaciones By Carlos Pardo
set -euo pipefail
cd "$(dirname "$0")"

PYTHON="${PYTHON:-python3}"
APP_NAME="Investigación de Operaciones By Carlos Pardo"
# El nombre del ejecutable interno debe ser ASCII: codesign de macOS 27 no
# puede sellar un bundle cuyo CFBundleExecutable contiene caracteres no ASCII
# ("a sealed resource is missing or invalid"). El nombre visible no cambia:
# lo siguen dando CFBundleDisplayName y CFBundleName.
EXE_NAME="AppExe"
ZIP_NAME="Investigación de Operaciones By Carlos Pardo (macOS).zip"

if [ ! -d ".venv-build" ]; then
  "$PYTHON" -m venv .venv-build
fi
# shellcheck disable=SC1091
source .venv-build/bin/activate

python -m pip install --upgrade pip >/dev/null
python -m pip install "pyinstaller>=6.10" >/dev/null

# Parches locales para PyInstaller (idempotentes):
#  1) No pasar --timestamp cuando la identidad es ad-hoc ('-'): macOS lo rechaza.
#  2) No firmar el bundle con --deep: en macOS 27 eso produce un bus error.
# El bundle se firma manualmente más abajo, de abajo hacia arriba.
python - <<'PYEOF'
from pathlib import Path

import PyInstaller
site = Path(PyInstaller.__file__).resolve().parent

osx_utils = site / "utils" / "osx.py"
text = osx_utils.read_text(encoding="utf-8")
old = """    cmd_args = [
        '/usr/bin/codesign', '-s', identity, '--force', '--all-architectures', '--timestamp', *extra_args, filename
    ]"""
new = """    cmd_args = ['/usr/bin/codesign', '-s', identity, '--force', '--all-architectures']
    # Ad-hoc signatures cannot be timestamped; macOS 15+ rejects --timestamp for identity '-'.
    if identity != '-':
        cmd_args.append('--timestamp')
    cmd_args.extend(extra_args)
    cmd_args.append(filename)"""
if old in text:
    osx_utils.write_text(text.replace(old, new), encoding="utf-8")
    print("PyInstaller: parche aplicado (utils/osx.py, sin --timestamp ad-hoc)")

osx_build = site / "building" / "osx.py"
text = osx_build.read_text(encoding="utf-8")
old = """        # Sign the bundle
        logger.info('Signing the BUNDLE...')
        try:
            osxutils.sign_binary(self.name, self.codesign_identity, self.entitlements_file, deep=True)
        except Exception as e:
            # Display a warning or re-raise the error, depending on the environment-variable setting.
            if os.environ.get("PYINSTALLER_STRICT_BUNDLE_CODESIGN_ERROR", "0") == "0":
                logger.warning("Error while signing the bundle: %s", e)
                logger.warning("You will need to sign the bundle manually!")
            else:
                raise RuntimeError("Failed to codesign the bundle!") from e
"""
new = """        # The bundle is signed by the build script. Bottom-up signing avoids a
        # codesign crash on recent macOS versions when using --deep.
        logger.info('Skipping BUNDLE signing; the build script signs it manually.')
"""
if old in text:
    osx_build.write_text(text.replace(old, new), encoding="utf-8")
    print("PyInstaller: parche aplicado (building/osx.py, sin firma --deep del bundle)")
PYEOF

# Compilar fuera de carpetas sincronizadas (Documentos/iCloud), porque el
# proveedor de archivos vuelve a añadir atributos que impiden firmar.
TMP_BUILD="$(mktemp -d "${TMPDIR:-/tmp}/io-build.XXXXXX")"
trap 'rm -rf "$TMP_BUILD"' EXIT

pyinstaller \
  --noconfirm \
  --clean \
  --windowed \
  --name "$APP_NAME" \
  --osx-bundle-identifier "com.io.solucionador" \
  --distpath "$TMP_BUILD/dist" \
  --workpath "$TMP_BUILD/build" \
  --specpath "$TMP_BUILD" \
  main.py

APP="$TMP_BUILD/dist/$APP_NAME.app"
if [ ! -d "$APP" ]; then
  echo "La compilación no generó la aplicación." >&2
  exit 1
fi

# Nombre visible en Finder, Dock y menú de macOS.
PLIST="$APP/Contents/Info.plist"
/usr/libexec/PlistBuddy -c "Set :CFBundleDisplayName $APP_NAME" "$PLIST" 2>/dev/null || \
  /usr/libexec/PlistBuddy -c "Add :CFBundleDisplayName string $APP_NAME" "$PLIST"
/usr/libexec/PlistBuddy -c "Set :CFBundleName $APP_NAME" "$PLIST" 2>/dev/null || \
  /usr/libexec/PlistBuddy -c "Add :CFBundleName string $APP_NAME" "$PLIST"

# Ejecutable interno en ASCII (ver nota al inicio del script).
OLD_EXE="$APP/Contents/MacOS/$APP_NAME"
if [ -f "$OLD_EXE" ]; then
  mv "$OLD_EXE" "$APP/Contents/MacOS/$EXE_NAME"
  /usr/libexec/PlistBuddy -c "Set :CFBundleExecutable $EXE_NAME" "$PLIST"
fi

# Firmar de abajo hacia arriba. --deep hace fallar codesign en macOS 27.
xattr -cr "$APP" || true
signed=0
while IFS= read -r -d '' file; do
  if file "$file" | grep -q "Mach-O"; then
    codesign --force -s - "$file" >/dev/null
    signed=$((signed + 1))
  fi
done < <(find "$APP/Contents" -type f -print0)
echo "Binarios internos firmados: $signed"
codesign --force -s - "$APP/Contents/Frameworks/Python.framework"
codesign --force -s - "$APP"
codesign --verify --deep --strict "$APP"
echo "Firma verificada."

mkdir -p dist
rm -rf "dist/InvestigacionOperaciones.app" "dist/$APP_NAME.app"
# Copiar sin atributos extendidos ni resource forks.
ditto --norsrc --noextattr "$APP" "dist/$APP_NAME.app"
# Finder/iCloud vuelve a añadir FinderInfo a la copia en dist; eso invalida
# la verificación ("resource fork, Finder information, or similar detritus").
xattr -cr "dist/$APP_NAME.app" || true
codesign --verify --deep --strict "dist/$APP_NAME.app"

rm -f "dist/InvestigacionOperaciones-macOS.zip" "dist/$ZIP_NAME"
ditto -c -k --norsrc --noextattr --keepParent \
  "$APP" \
  "dist/$ZIP_NAME"

echo
echo "Listo:"
echo "  dist/$APP_NAME.app"
echo "  dist/$ZIP_NAME"
