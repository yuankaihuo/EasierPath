# Versions
## V 1.0.0
Make sure you delete C:\Users\huoyu\.labelmerc_v1_0_0 before using the file


# Development

## How to package exe file

pip install pywin32

pip install dis3

pip install pyinstaller

pyinstaller labelme.spec

If you see qt5 error, please copy the "imageformats" and "platforms" folders from
C:\Users\huoyu\Anaconda3\envs\labelme\Library\plugins\
to "dist" folder

