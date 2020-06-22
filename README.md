# EasierPath: An Open-source Tool for Human-in-the-loop Deep Learning Quantification of Renal Pathology

## Quick Start
### Get our software: 

Version 1.0.1

Updates:
1. Add the function of adjusting the threshold of detections
2. Save the detections as ImageScope file
3. Adjust the hot keys
4. Add the function of "save patch"

Download Address: https://vanderbilt.box.com/s/0a9x1l00h1gzfpvstdayvqp26p033tla

*Version 1.0.0
This is an older version, here is the Download Address: https://vanderbilt.box.com/s/juhh42e86x0wvy7fj286lrauqmanywxd
Maybe you need to delete C:\Users\huoyu\.labelmerc_v1_0_1 before using the file at the first time

### Explanation Video: 
This is an recorded explanation video posted on Youtube. This video contains various parts, including "How to download EasierPath", "Explanation for the toolbox", ""
Video Address: https://vanderbilt.box.com/s/aih7n8h0ii4nzq34gueff9g6ops8u5aj

## Source Code

EasierPath is a computer-human intergrated pipeline for structural objects annotation, like glomeruli, for whole slice imaging. This pipeline contains (1) Detection using deep learning, (2) Filtering with optimal threshold, (3) Manual QA by doctors, (4) Object Extraction and (5) Data Management. The related source code and binary files have been included in the Docker. They are all found in "python".

## Development
### How to package exe file
You can run the following command
```
pip install pywin32
pip install dis3
pip install pyinstaller
pyinstaller labelme.spec
```

- If you see qt5 error, please copy the "imageformats" and "platforms" folders from
C:\Users\huoyu\Anaconda3\envs\labelme\Library\plugins\
to "dist" folder

Use the version with "SavePatch" in windows
Please download openslide windows binary form
https://openslide.org/download/

Then, go to "System Properties" --> "Advanced" --> "Envrioment Variables"
 
Find "Path" in User Variables, then add the downloaded "bin" folder to Path

### How to use EasierPath
- Use "Open" or "Open Dir"(Open Diractory) to open the desired project, which should include one .png file and one .xml file.
- To change the threshold of the desired image, click "Thresh Up" or "Thresh Down". With the software processes, the final annotation of such threshold will be displayed.
- "Zoom in" and "Zoom out" are used to enlarge or dwindle the image for better vision.
- Go to "Edit" -> "Create Circle", one can circle and annotate the missing structural objects using this tool.
- If the annotation is incorrect, one can simply click that circle and delete it.
- Once all the annotations are successfully processed, one can use "Save ImageScope" button to save that image into a .scn file which can be open by ImageScope Software.
- "Save Patches" can be used to save patches of all the annotation images for further analysis.

### How to run the code and get EasierPath
```
pip install pyyaml
pip install qtpy
pip install matplotlib
pip install pillow
pip install termcolor
pip install spyder
pip install xmltodict
pip install openslide-python
```
