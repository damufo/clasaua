pyinstaller --clean --workpath=./build_win --distpath=./dist_win clasaua_pyinstaller_win_onefile.spec

timeout 2

python clasaua_pyinstaller_post_build.py onefile

pause
