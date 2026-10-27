@echo off
REM Build Lulu Desktop Pet for Windows. Run this on a Windows machine.
cd /d "%~dp0"

python -m pip install -r requirements.txt
python scripts\build_icons.py
pyinstaller lulu-pet.spec --noconfirm --clean

echo.
echo Build complete: dist\LuluDesktopPet\
echo Distribute the whole dist\LuluDesktopPet folder (keep its structure intact).
echo Zip it for sharing:
python -c "import zipfile,os; src='dist/LuluDesktopPet'; out='dist/LuluDesktopPet-win64.zip'; os.path.exists(out) and os.remove(out); z=zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED); [z.write(os.path.join(r,f), os.path.relpath(os.path.join(r,f),'dist')) for r,_,fs in os.walk(src) for f in fs]; print('wrote', out)"
pause
