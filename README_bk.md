# Versions
## V 1.0.1
Updates: 
#1. Add the function of adjusting the threshold of detections
#2. Save the detections as ImageScope file
#3. Adjust the hot keys
4. Add save patch

Download: https://vanderbilt.box.com/s/juhh42e86x0wvy7fj286lrauqmanywxd

How to use: https://vanderbilt.box.com/s/aih7n8h0ii4nzq34gueff9g6ops8u5aj

QA data: https://vumc.box.com/s/5ii4l0r3kfqxsbsfd15vc4uemyfrw0nt 

## V 1.0.0
Download: https://vanderbilt.box.com/s/juhh42e86x0wvy7fj286lrauqmanywxd

Maybe you need to delete C:\Users\huoyu\.labelmerc_v1_0_1 before using the file at the first time


# Development

## How to package exe file

pip install pywin32

pip install dis3

pip install pyinstaller

pyinstaller labelme.spec

If you see qt5 error, please copy the "imageformats" and "platforms" folders from
C:\Users\huoyu\Anaconda3\envs\labelme\Library\plugins\
to "dist" folder


Use the version with "SavePatch" in windows
Please download openslide windows binary form
https://openslide.org/download/

Then,go to "System Properties" --> "Advanced" --> "Envrioment Variables"
 
Find "Path" in User Variables, then add the downloaded "bin" folder to Path
 

