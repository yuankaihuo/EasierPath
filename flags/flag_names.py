flag_dict = {}
flag_dict['Glomerular'] = {}
flag_dict['Glomerular']['title'] = 'Glomerular morphology'
flag_dict['Glomerular']['map'] = [
            ('1.Hypertrophy', False),
            ('2.Necrosis', False),
            ('3.Global disappearing glomerulosclerosis', False),
            ('4.Global solidified glomerulosclerosis', False),
            ('5.Global obsolescent glomerulosclerosis', False),
            ('6.Segmental sclerosis', False),
            ('7.Enlarged capsule space', False)
            ]

flag_dict['Bowman'] = {}
flag_dict['Bowman']['title'] = 'Bowman capsule & PECs'
flag_dict['Bowman']['map'] = [
            ('1.Periglomerular fibrosis', False),
            ('2.Capsular drop', False),
            ('3.Cellular crescent', False),
            ('4.Fibrocellular crescent', False),
            ('5.Fibrous crescent', False),
            ('6.Capsule broken', False),
            ]

flag_dict['Podocyte'] = {}
flag_dict['Podocyte']['title'] = 'Podocyte injury'
flag_dict['Podocyte']['map'] = [
            ('1.Tuft adhesion', False),
            ('2.Collapsing tuft with podocyte hyperplasia', False),
            ('3.Foam cell', False),
            ]

flag_dict['GBM'] = {}
flag_dict['GBM']['title'] = 'GBM'
flag_dict['GBM']['map'] = [
            ('1.Thick', False),
            ('2.Double contour', False),
            ('3.Spike', False),
            ('4.Bubble-like', False),
            ('5.Corrugated', False),
            ('6.GBM broken', False),
            ]

flag_dict['Capillary'] = {}
flag_dict['Capillary']['title'] = 'In capillary'
flag_dict['Capillary']['map'] = [
            ('1.Thrombi', False),
            ('2.Glomerulitis', False),
            ('3.Endocapillary hypercellularity', False),
            ('4.Microaneurysm', False),
            ]

flag_dict['Mesangial'] = {}
flag_dict['Mesangial']['title'] = 'Mesangial'
flag_dict['Mesangial']['map'] = [
            ('1.Proliferation', False),
            ('2.Nodular', False),
            ('3.Mesangiolysis', False),
            ('4.Expansion', False),
            ('5.Hyalinosis', False),
            ]

flag_dict['Other'] = {}
flag_dict['Other']['title'] = 'Other'
flag_dict['Other']['map'] = [
            ('1.Wire loop', False),
            ('2.Karyorrhexis', False),
            ]

flag_dict['Tumor'] = {}
flag_dict['Tumor']['title'] = 'Tumor'
flag_dict['Tumor']['map'] = [
            ('Primary', False),
            ('Cyst', False),
            ('Others', False),
            ]

def get_flags():

    #change this window
    # flag_names = ['Tumor']
    flag_names = ['Glomerular', 'Bowman', 'Podocyte', 'GBM', 'Capillary','Mesangial','Other']

    flag_dict_list = []
    for fi in range(len(flag_names)):
        out_dict = {}
        flag_name = flag_names[fi]
        out_dict['name'] = flag_name
        out_dict['title'] = flag_dict[flag_name]['title']
        out_dict['map'] = flag_dict[flag_name]['map']
        flag_dict_list.append(out_dict)

    return flag_dict_list
