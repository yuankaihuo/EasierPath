import openslide
import xmltodict
import numpy as np
from PIL import Image
import os
import cv2

def read_mask(simg,xml_file,output_dir,boarder = 1.2):

    # read region
    with open(xml_file) as fd:
        doc = xmltodict.parse(fd.read())
    layers = doc['Annotations']['Annotation']

    try:
        start_x = np.int(simg.properties['openslide.bounds-x'])
        start_y = np.int(simg.properties['openslide.bounds-y'])
        width_x = np.int(simg.properties['openslide.bounds-width'])
        height_y = np.int(simg.properties['openslide.bounds-height'])
    except:
        start_x = 0
        start_y = 0
        width_x = np.int(simg.properties['aperio.OriginalWidth'])
        height_y = np.int(simg.properties['aperio.OriginalHeight'])
    end_x = start_x + width_x
    end_y = start_y + height_y


    if isinstance(layers, (dict)):
        layers = [layers]

    for i in range(len(layers)):
        regions = layers[i]['Regions']

        if isinstance(layers[i]['Attributes'], dict):
            clss_name = layers[i]['Attributes']['Attribute']['@Name']
        else:
            clss_name = 'unknown'

        if (len(regions) < 2):
            notFound = layers[0]
        else:
            regions = regions['Region']

            if isinstance(regions, (dict)):
                regions = [regions]

            for j in range(len(regions)):
                contour = regions[j]
                img, cimg, mask, bbox, img_iso, cimg_iso, mask_iso = get_contour(simg, contour, start_x, start_y, boarder)
                save_all_images(img, cimg, mask, bbox, img_iso, cimg_iso, mask_iso, output_dir, xml_file, j, clss_name)


    # try:
    #
    #     if(len(multi_contours)<2):
    #         notFound = multi_contours[0]
    #
    #     else:
    #         contours = multi_contours['Region']
    #
    #         try:
    #             contours['Vertices']
    #             img, cimg, mask, bbox, img_iso, cimg_iso, mask_iso  = get_contour(simg, contours, start_x, start_y)
    #                 # img_1 = np.concatenate((img, img, img, img), axis=1)
    #             # img_all = np.concatenate((img_1, img_1), axis=0)
    #             save_all_images(img, cimg, mask, bbox, img_iso, cimg_iso, mask_iso, output_dir, xml_file, 0)
    #
    #         except:
    #             for j in range(len(contours)):
    #                 contour = contours[j]
    #                 img, cimg, mask, bbox, img_iso, cimg_iso, mask_iso  = get_contour(simg, contour, start_x, start_y)
    #                 # img_1 = np.concatenate((img, img, img, img), axis=1)
    #                 # img_all = np.concatenate((img_1, img_1), axis=0)
    #                 save_all_images(img, cimg, mask, bbox, img_iso, cimg_iso, mask_iso, output_dir, xml_file, j)
    #
    # except:
    #     for i in range(len(layers)):
    #         contours = layers[i]['Regions']
    #
    #         if(len(contours)<2):
    #             notFound = layers[0]
    #
    #         else:
    #             contours = contours['Region']
    #
    #             try:
    #                 contours['Vertices']
    #                 img, cimg, mask, bbox, img_iso, cimg_iso, mask_iso  = get_contour(simg, contours, start_x, start_y)
    #                 # img_1 = np.concatenate((img, img, img, img), axis=1)
    #                 # img_all = np.concatenate((img_1, img_1), axis=0)
    #                 save_all_images(img, cimg, mask, bbox, img_iso, cimg_iso, mask_iso, output_dir, xml_file, 0)
    #
    #             except:
    #                 for j in range(len(contours)):
    #                     contour = contours[j]
    #                     img, cimg, mask, bbox, img_iso, cimg_iso, mask_iso = get_contour(simg, contour, start_x, start_y)
    #                     save_all_images(img, cimg, mask, bbox, img_iso, cimg_iso, mask_iso, output_dir, xml_file,j)

def save_all_images(img, cimg, mask, bbox, img_iso, cimg_iso, mask_iso, output_dir, xml_file, roi_num, clss_name):
    # img_1 = np.concatenate((img, img, img, img), axis=1)
    # img_all = np.concatenate((img_1, img_1), axis=0)
    save_one_image(img, output_dir, 'image', xml_file, roi_num, bbox, clss_name)
    # save_one_image(cimg, output_dir, 'contour', xml_file, roi_num, bbox, clss_name)
    # save_one_image(mask, output_dir, 'mask', xml_file, roi_num, bbox, clss_name)
    # save_one_image(img_iso, output_dir, 'image_iso', xml_file, roi_num, bbox, clss_name)
    # save_one_image(cimg_iso, output_dir, 'contour_iso', xml_file, roi_num, bbox, clss_name)
    # save_one_image(mask_iso, output_dir, 'mask_iso', xml_file, roi_num, bbox, clss_name)


def save_one_image(img, output_dir, dir_name, xml_file, roi_num, bbox, clss_name):
    img_all_out = Image.fromarray(img)
    output_dir = os.path.join(output_dir, dir_name)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    img_all_out_file = os.path.join(output_dir, '%s-x-ROI_%d-x-%s-x-%d-x-%d-x-%d-x-%d.png' %
                                    (os.path.basename(xml_file).replace('.xml', ''), roi_num, clss_name,
                                        bbox[0], bbox[1], bbox[2], bbox[3]))
    img_all_out.save(img_all_out_file)

def get_none_zero(black_arr):

    nonzeros = black_arr.nonzero()
    starting_y = nonzeros[0].min()
    ending_y = nonzeros[0].max()
    starting_x = nonzeros[1].min()
    ending_x = nonzeros[1].max()

    return starting_x, starting_y, ending_x, ending_y

def scan_nonblack(simg,px_start,py_start,px_end,py_end):
    offset_x = 0
    offset_y = 0
    line_x = py_end-py_start
    line_y = px_end-px_start

    val = simg.read_region((px_start+offset_x, py_start), 0, (1, 1))
    arr = np.array(val)[:, :, 0].sum()
    while arr == 0:
        val = simg.read_region((px_start+offset_x, py_start), 0, (1, line_x))
        arr = np.array(val)[:, :, 0].sum()
        offset_x = offset_x + 1

    val = simg.read_region((px_start, py_start+offset_y), 0, (1, 1))
    arr = np.array(val)[:, :, 0].sum()
    while arr == 0:
        val = simg.read_region((px_start, py_start+offset_y), 0, (line_y, 1))
        arr = np.array(val)[:, :, 0].sum()
        offset_y = offset_y + 1

    x = px_start+offset_x-1
    y = py_start+offset_y-1
    return x,y


def get_nonblack_starting_point(simg):
    px = 0
    py = 0
    black_img = simg.read_region((px, py), 3, (3000, 3000))
    starting_x, starting_y, ending_x, ending_y = get_none_zero(np.array(black_img)[:, :, 0])

    multiples = int(np.floor(simg.level_dimensions[0][0]/float(simg.level_dimensions[3][0])))

    #staring point
    px2 = (starting_x - 1) * multiples
    py2 = (starting_y - 1) * multiples
    #ending point
    px3 = (ending_x + 1) * multiples
    py3 = (ending_y + 1) * multiples

    # black_img_big = simg.read_region((px2, py2), 0, (1000, 1000))
    # offset_x, offset_y, offset_xx, offset_yy = get_none_zero(np.array(black_img_big)[:, :, 0])
    #
    # x = px2+offset_x
    # y = py2+offset_y

    xx, yy = scan_nonblack(simg, px2, py2, px3, py3)

    return xx,yy

def get_ROI(simg, region):
    vertices = region['Vertices']['Vertex']
    x0 = float(vertices[0]['@X'])
    y0 = float(vertices[0]['@Y'])
    z0 = float(vertices[0]['@Z'])
    x1 = float(vertices[1]['@X'])
    y1 = float(vertices[1]['@Y'])
    z1 = float(vertices[1]['@Z'])
    x2 = float(vertices[2]['@X'])
    y2 = float(vertices[2]['@Y'])
    z2 = float(vertices[2]['@Z'])
    x3 = float(vertices[3]['@X'])
    y3 = float(vertices[3]['@Y'])
    z3 = float(vertices[3]['@Z'])

    # get manual ROI coordinate
    ys = int(round(x0))
    xs = int(round(y0))
    yss = int(round(x1))
    xss = int(round(y2))
    widths = int(round(x1 - x0))
    heights = int(round(y2 - y1))

    start_x, start_y = get_nonblack_starting_point(simg)
    #isimg.read_region((44600, 82700), 0, (widths,heights).show()
    max_widths = int(simg.properties['openslide.bounds-height'])
    img = simg.read_region((start_x+xs, max_widths-yss+start_y), 0, (heights,widths))
    img = np.array(img.convert('RGB'))
    return img

def get_contour(simg, contour, start_x, start_y, boarder = 1.2):
    max_height = int(simg.properties['openslide.bounds-width'])
    max_widths = int(simg.properties['openslide.bounds-height'])
    vertices = contour['Vertices']['Vertex']
    x_min = max_height
    x_max = 0
    y_min = max_widths
    y_max = 0



    for vi in range(len(vertices)):
        xraw = float(vertices[vi]['@Y'])
        yraw = float(vertices[vi]['@X'])
        if xraw < x_min:
            x_min = xraw
        if xraw > x_max:
            x_max = xraw
        if yraw < y_min:
            y_min = yraw
        if yraw > y_max:
            y_max = yraw

        x_min = int(round(x_min))
        x_max = int(round(x_max))
        y_min = int(round(y_min))
        y_max = int(round(y_max))

        # add cropping
        xx_min = max(x_min-50, 0)
        xx_max = min(x_max+50, max_height)
        yy_min = max(y_min-50, 0)
        yy_max = min(y_max+50, max_widths)

        heights = xx_max-xx_min
        widths = yy_max-yy_min

        xs = xx_min
        yss = yy_max


    cnt = np.zeros((len(vertices),1,2))
    for vi in range(len(vertices)):
        xx = float(vertices[vi]['@Y'])-xs
        yy = yss - float(vertices[vi]['@X'])
        cnt[vi,0,0] = int(xx)
        cnt[vi,0,1] = int(yy)



    #isimg.read_region((44600, 82700), 0, (widths,heights).show()

    read_x0 = start_x+xs
    read_y0 = max_widths-yss+start_y
    read_height = heights
    read_widths = widths
    bbox = (read_x0, read_y0, read_height, read_widths)

    img = simg.read_region((read_x0, read_y0), 0, (read_height,read_widths))
    img = np.array(img.convert('RGB'))

    cimg = img.copy()
    vertices = contour['Vertices']['Vertex']
    cnt = np.zeros((len(vertices),1,2))
    for vi in range(len(vertices)):
        xx = float(vertices[vi]['@Y'])-xs
        yy = yss - float(vertices[vi]['@X'])
        cnt[vi,0,0] = int(xx)
        cnt[vi,0,1] = int(yy)

    cv2.drawContours(cimg, [cnt.astype(int)], -1, (0, 255, 0), 3)

    #draw mask
    mask = np.zeros(cimg.shape, dtype=np.uint8)
    cv2.drawContours(mask, [cnt.astype(int)], -1, (255, 255, 255), -1)

    # Image.fromarray(cimg).show()
    length_iso = np.max([read_height, read_widths])
    length_iso = np.int(length_iso*boarder)  #have boarder
    iso_offset_h = np.int((length_iso - read_height) / 2)
    iso_offset_w = np.int((length_iso - read_widths) / 2)

    img_iso = simg.read_region((read_x0-iso_offset_h, read_y0-iso_offset_w), 0, (length_iso,length_iso))
    img_iso = np.array(img_iso.convert('RGB'))

    cimg_iso = img_iso.copy()
    cimg_iso[iso_offset_w:(iso_offset_w+read_widths),iso_offset_h:(iso_offset_h+read_height),:] = cimg

    mask_iso = np.zeros(img_iso.shape, dtype=np.uint8)
    mask_iso[iso_offset_w:(iso_offset_w + read_widths), iso_offset_h:(iso_offset_h + read_height), :] = mask

    return img, cimg, mask, bbox, img_iso, cimg_iso, mask_iso

def get_MASK(simg, region, contour):
    vertices = region['Vertices']['Vertex']
    x0 = float(vertices[0]['@X'])
    y0 = float(vertices[0]['@Y'])
    z0 = float(vertices[0]['@Z'])
    x1 = float(vertices[1]['@X'])
    y1 = float(vertices[1]['@Y'])
    z1 = float(vertices[1]['@Z'])
    x2 = float(vertices[2]['@X'])
    y2 = float(vertices[2]['@Y'])
    z2 = float(vertices[2]['@Z'])
    x3 = float(vertices[3]['@X'])
    y3 = float(vertices[3]['@Y'])
    z3 = float(vertices[3]['@Z'])

    # get manual ROI coordinate
    ys = int(round(x0))
    xs = int(round(y0))
    yss = int(round(x1))
    xss = int(round(y2))
    widths = int(round(x1 - x0))
    heights = int(round(y2 - y1))

    start_x, start_y = get_nonblack_starting_point(simg)
    #isimg.read_region((44600, 82700), 0, (widths,heights).show()
    max_height = int(simg.properties['openslide.bounds-height'])

    img = simg.read_region((start_x+xs, max_height-yss+start_y), 0, (heights,widths))
    img = np.array(img.convert('RGB'))

    cimg = img.copy()
    vertices = contour['Vertices']['Vertex']
    cnt = np.zeros((len(vertices),1,2))
    for vi in range(len(vertices)):
        xx = float(vertices[vi]['@Y'])-xs
        yy = yss - float(vertices[vi]['@X'])
        cnt[vi,0,0] = int(xx)
        cnt[vi,0,1] = int(yy)

    cv2.drawContours(cimg, [cnt.astype(int)], -1, (0, 255, 0), 3)

    #draw mask
    mask = np.zeros(cimg.shape, dtype=np.uint8)
    cv2.drawContours(mask, [cnt.astype(int)], -1, (255, 255, 255), -1)

    # Image.fromarray(cimg).show()


    return img, cimg, mask