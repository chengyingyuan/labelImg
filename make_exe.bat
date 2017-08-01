set PYTHONHOME=E:\Apps\Python35
REM set PATH=E:\Apps\Qt\Qt5.8_MSVC64\5.8\msvc2015_64\bin;%PYTHONHOME%;%PATH%
REM Qt DLL path not recognized by pyinstaller - so weird 
set PATH=E:\Apps\Python35\Lib\site-packages\PyQt5\Qt\bin;%PATH%

rmdir /S /Q dist
rmdir /S /Q build
del labelImg.spec
%PYTHONHOME%\Scripts\pyinstaller.exe -w -p libs -p . --add-data data;data labelImg.py
