flag_dict = {}
flag_dict['Glomerular'] = {}
flag_dict['Glomerular']['title'] = 'Glomerular morphology'
flag_dict['Glomerular']['map'] = [
            ('Hypertrophy', False),
            ('Necrosis', False),
            ('Global disappearing glomerulosclerosis', False),
            ('Global solidified glomerulosclerosis', False),
            ('Global obsolescent glomerulosclerosis', False),
            ('Segmental sclerosis', False),
            ('Enlarged capsule space', False)
            ]

flag_dict['Bowman'] = {}
flag_dict['Bowman']['title'] = 'Bowman capsule & PECs'
flag_dict['Bowman']['map'] = [
            ('Periglomerular fibrosis', False),
            ('Capsular drop', False),
            ('Cellular crescent', False),
            ('Fibrocellular crescent', False),
            ('Fibrous crescent', False),
            ('Capsule broken', False),
            ]

flag_dict['Podocyte'] = {}
flag_dict['Podocyte']['title'] = 'Podocyte injury'
flag_dict['Podocyte']['map'] = [
            ('Tuft adhesion', False),
            ('Collapsing tuft with podocyte hyperplasia', False),
            ('Foam cell', False),
            ]

flag_dict['GBM'] = {}
flag_dict['GBM']['title'] = 'GBM'
flag_dict['GBM']['map'] = [
            ('Thick', False),
            ('Double contour', False),
            ('Spike', False),
            ('Bubble-like', False),
            ('Corrugated', False),
            ('GBM broken', False),
            ]

flag_dict['Capillary'] = {}
flag_dict['Capillary']['title'] = 'In capillary'
flag_dict['Capillary']['map'] = [
            ('Thrombi', False),
            ('Glomerulitis', False),
            ('Endocapillary hypercellularity', False),
            ('Microaneurysm', False),
            ]

flag_dict['Mesangial'] = {}
flag_dict['Mesangial']['title'] = 'Mesangial'
flag_dict['Mesangial']['map'] = [
            ('Proliferation', False),
            ('Nodular', False),
            ('Mesangiolysis', False),
            ('Expansion', False),
            ('Hyalinosis', False),
            ]

flag_dict['Other'] = {}
flag_dict['Other']['title'] = 'Other'
flag_dict['Other']['map'] = [
            ('Wire loop', False),
            ('Karyorrhexis', False),
            ]

def get_flags():

    #change this window
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
