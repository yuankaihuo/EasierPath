

def get_flags(flag_name):
    if flag_name == 'Glomerular':
        flag_dict = [
            ('Hypertrophy', True),
            ('Necrosis', False),
            ('Global sclerosis', False),
            ('Segmental sclerosis', False),
            ('Enlarged capsule space', False)
            ]

    if flag_name == 'Bowman':
        flag_dict = [
            ('Periglomerular fibrosis', True),
            ('Capsular drop', False),
            ('Crescent', False),
            ]

    if flag_name == 'Podocyte':
        flag_dict = [
            ('Tuft adhesion', True),
            ('Collapsing tuft with podocyte hyperplasia', False),
            ('Foam cell', False),
            ]

    if flag_name == 'GBM':
        flag_dict = [
            ('Thick', True),
            ('Double contour', False),
            ('Spike', False),
            ('Bubble-like', False),
            ('Corrugated', False),
            ]

    if flag_name == 'Capillary':
        flag_dict = [
            ('Thrombi', True),
            ('Glomerulitis', False),
            ('Endocapillary proliferation', False),
            ('Microaneurysm', False),
            ]

    if flag_name == 'Mesangial':
        flag_dict = [
            ('Proliferation', True),
            ('Nodular', False),
            ('Mesangiolysis', False),
            ]

    if flag_name == 'Other':
        flag_dict = [
            ('Wire loop', True),
            ('Karyorrhexis', False),
            ]

    return flag_dict