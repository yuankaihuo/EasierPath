import base64
import io
import json
import os.path as osp
import numpy as np
import xmltodict
import PIL.Image

from labelme._version import __version__
from labelme.logger import logger
from labelme import PY2
from labelme import QT4
from labelme import utils

from flags.flag_names import get_flags


class LabelFileError(Exception):
    pass


class LabelFile(object):

    suffix = '.json'

    def __init__(self, filename=None):
        self.shapes = ()
        self.imagePath = None
        self.imageData = None
        if filename is not None:
            self.load(filename)
        self.filename = filename

    @staticmethod
    def load_image_file(filename):
        try:
            image_pil = PIL.Image.open(filename)
        except IOError:
            logger.error('Failed opening image file: {}'.format(filename))
            return

        # apply orientation to image according to exif
        image_pil = utils.apply_exif_orientation(image_pil)

        with io.BytesIO() as f:
            ext = osp.splitext(filename)[1].lower()
            if PY2 and QT4:
                format = 'PNG'
            elif ext in ['.jpg', '.jpeg']:
                format = 'JPEG'
            else:
                format = 'PNG'
            image_pil.save(f, format=format)
            f.seek(0)
            return f.read()

    def load(self, filename):
        keys = [
            'imageData',
            'imagePath',
            'lineColor',
            'fillColor',
            'shapes',  # polygonal annotations
            'flags',   # image level flags
            'imageHeight',
            'imageWidth',
        ]

        #yuankai add to load new flags
        try:
            all_flags = get_flags()
            additionalFlags_default = {}
            for additional_flag in all_flags:
                keys.append(additional_flag['name'])
                additionalFlags_default[additional_flag['name']] = {}
                for mi in range(len(additional_flag['map'])):
                    additionalFlags_default[additional_flag['name']][additional_flag['map'][mi][0]] = additional_flag['map'][mi][1]
        except:
            if_additiona_flags = False

        try:
            with open(filename, 'rb' if PY2 else 'r') as f:
                data = json.load(f)
            if data['imageData'] is not None:
                imageData = base64.b64decode(data['imageData'])
                if PY2 and QT4:
                    imageData = utils.img_data_to_png_data(imageData)
            else:
                # relative path from label file to relative path from cwd
                imagePath = osp.join(osp.dirname(filename), data['imagePath'])
                imageData = self.load_image_file(imagePath)
            flags = data.get('flags') or {}
            #yuankai add to read additional flags
            additionalFlags = {}
            for additional_flag in all_flags:
                flag_name = additional_flag['name']
                additionalFlags[flag_name] = data.get(flag_name) or additionalFlags_default[flag_name]
            imagePath = data['imagePath']
            self._check_image_height_and_width(
                base64.b64encode(imageData).decode('utf-8'),
                data.get('imageHeight'),
                data.get('imageWidth'),
            )
            lineColor = data['lineColor']
            fillColor = data['fillColor']
            shapes = (
                (
                    s['label'],
                    s['points'],
                    s['line_color'],
                    s['fill_color'],
                    s.get('shape_type', 'polygon'),
                    s.get('flags', {}),
                )
                for s in data['shapes']
            )
        except Exception as e:
            raise LabelFileError(e)

        otherData = {}
        for key, value in data.items():
            if key not in keys:
                otherData[key] = value

        # Only replace data after everything is loaded.
        self.flags = flags
        self.shapes = shapes
        self.imagePath = imagePath
        self.imageData = imageData
        self.lineColor = lineColor
        self.fillColor = fillColor
        self.filename = filename
        self.otherData = otherData
        self.additionalFlags = additionalFlags

    @staticmethod
    def _check_image_height_and_width(imageData, imageHeight, imageWidth):
        img_arr = utils.img_b64_to_arr(imageData)
        if imageHeight is not None and img_arr.shape[0] != imageHeight:
            logger.error(
                'imageHeight does not match with imageData or imagePath, '
                'so getting imageHeight from actual image.'
            )
            imageHeight = img_arr.shape[0]
        if imageWidth is not None and img_arr.shape[1] != imageWidth:
            logger.error(
                'imageWidth does not match with imageData or imagePath, '
                'so getting imageWidth from actual image.'
            )
            imageWidth = img_arr.shape[1]
        return imageHeight, imageWidth

    def save_ImageScope(
        self,
        filename,
        shapes,
        flags=None,
        threshVal=None,
    ):

        down_rate = flags['@DownRate']

        detect_json = []
        doc_out = {}
        doc_out['Annotations'] = {}
        doc_out['Annotations']['@MicronsPerPixel'] = flags['@MicronsPerPixel']
        doc_out['Annotations']['@Level'] = flags['@Level']
        doc_out['Annotations']['@DownRate'] = flags['@DownRate']
        doc_out['Annotations']['@start_x'] = flags['@start_x']
        doc_out['Annotations']['@start_y'] = flags['@start_y']
        doc_out['Annotations']['@width_x'] = flags['@width_x']
        doc_out['Annotations']['@height_y'] = flags['@height_y']
        doc_out['Annotations']['@Device'] = flags['@Device']
        doc_out['Annotations']['Annotation'] = {}
        doc_out['Annotations']['Annotation']['@Id'] = '1'
        doc_out['Annotations']['Annotation']['@Name'] = ''
        doc_out['Annotations']['Annotation']['@ReadOnly'] = '0'
        doc_out['Annotations']['Annotation']['@LineColorReadOnly'] = '0'
        doc_out['Annotations']['Annotation']['@Incremental'] = '0'
        doc_out['Annotations']['Annotation']['@Type'] = '4'
        doc_out['Annotations']['Annotation']['@LineColor'] = '65280'
        doc_out['Annotations']['Annotation']['@Visible'] = '1'
        doc_out['Annotations']['Annotation']['@Selected'] = '1'
        doc_out['Annotations']['Annotation']['@MarkupImagePath'] = ''
        doc_out['Annotations']['Annotation']['@MacroName'] = ''
        doc_out['Annotations']['Annotation']['Attributes'] = {}
        doc_out['Annotations']['Annotation']['Attributes']['Attribute'] = {}
        doc_out['Annotations']['Annotation']['Attributes']['Attribute']['@Name'] = 'glomerulus'
        doc_out['Annotations']['Annotation']['Attributes']['Attribute']['@Id'] = '0'
        doc_out['Annotations']['Annotation']['Attributes']['Attribute']['@Value'] = ''
        doc_out['Annotations']['Annotation']['Plots'] = None
        doc_out['Annotations']['Annotation']['Regions'] = {}
        doc_out['Annotations']['Annotation']['Regions']['RegionAttributeHeaders'] = {}
        doc_out['Annotations']['Annotation']['Regions']['AttributeHeader'] = []
        doc_out['Annotations']['Annotation']['Regions']['Region'] = []

        for di in range(len(shapes)):
            detect_one = shapes[di]
            if detect_one['flags']['prob'] < threshVal:
                continue
            circle = [detect_one['points'][0][0], detect_one['points'][0][1], detect_one['points'][1][1] - detect_one['points'][0][1]]
            detect_dict = {}
            detect_dict['@Id'] = str(di + 1)
            detect_dict['@Type'] = '2'
            detect_dict['@Zoom'] = '0.5'
            detect_dict['@ImageLocation'] = ''
            detect_dict['@ImageFocus'] = '-1'
            detect_dict['@Length'] = '2909.1'
            detect_dict['@Area'] = '673460.1'
            detect_dict['@LengthMicrons'] = '727.3'
            detect_dict['@AreaMicrons'] = '42091.3'
            detect_dict['@Text'] = ('%.3f' % detect_one['flags']['prob'])
            detect_dict['@NegativeROA'] = '0'
            detect_dict['@InputRegionId'] = '0'
            detect_dict['@Analyze'] = '0'
            detect_dict['@DisplayId'] = str(di + 1)
            detect_dict['Attributes'] = None
            detect_dict['Vertices'] = '0'
            detect_dict['Vertices'] = {}
            detect_dict['Vertices']['Vertex'] = []

            if flags['@Device'] == 'leica.device-model':
                coord1 = {}
                coord1['@X'] = str(flags['@height_y'] - (circle[1] - circle[2]) * down_rate)
                coord1['@Y'] = str((circle[0] - circle[2]) * down_rate)
                coord1['@Z'] = '0'
                coord2 = {}
                coord2['@X'] = str(flags['@height_y'] - (circle[1] + circle[2]) * down_rate)  # 左右
                coord2['@Y'] = str((circle[0] + circle[2]) * down_rate)  # 上下
                coord2['@Z'] = '0'
                detect_dict['Vertices']['Vertex'].append(coord1)
                detect_dict['Vertices']['Vertex'].append(coord2)
            elif flags['@Device'] == 'aperio.Filename':
                coord1 = {}
                coord1['@X'] = str((circle[0] - circle[2]) * down_rate)
                coord1['@Y'] = str((circle[1] - circle[2]) * down_rate)
                coord1['@Z'] = '0'
                coord2 = {}
                coord2['@X'] = str((circle[0] + circle[2]) * down_rate)  # 左右
                coord2['@Y'] = str((circle[1] + circle[2]) * down_rate)  # 上下
                coord2['@Z'] = '0'
                detect_dict['Vertices']['Vertex'].append(coord1)
                detect_dict['Vertices']['Vertex'].append(coord2)
            doc_out['Annotations']['Annotation']['Regions']['Region'].append(detect_dict)

        out = xmltodict.unparse(doc_out, pretty=True)
        with open(filename, 'wb') as file:
            file.write(out.encode('utf-8'))

    def save_Patch(
        self,
        filename,
        shapes,
        flags=None,
        threshVal=None,
    ):
        aaa = None

    def save(
        self,
        filename,
        shapes,
        imagePath,
        imageHeight,
        imageWidth,
        imageData=None,
        lineColor=None,
        fillColor=None,
        otherData=None,
        flags=None,
        additional_flags=None,
    ):
        if imageData is not None:
            imageData = base64.b64encode(imageData).decode('utf-8')
            imageHeight, imageWidth = self._check_image_height_and_width(
                imageData, imageHeight, imageWidth
            )
        if otherData is None:
            otherData = {}
        if flags is None:
            flags = {}
        data = dict(
            version=__version__,
            flags=flags,
            shapes=shapes,
            lineColor=lineColor,
            fillColor=fillColor,
            imagePath=imagePath,
            imageData=imageData,
            imageHeight=imageHeight,
            imageWidth=imageWidth,
        )

        #yuankai add to save the addtional labels
        if len(additional_flags)>0:
            for key in additional_flags.keys():
                data[key] = additional_flags[key]


        for key, value in otherData.items():
            data[key] = value

        try:
            with open(filename, 'wb' if PY2 else 'w') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.filename = filename
        except Exception as e:
            raise LabelFileError(e)

    @staticmethod
    def is_label_file(filename):
        return osp.splitext(filename)[1].lower() == LabelFile.suffix
