string_in = '''{"id": "2B", "type": "8", "orientation": "1", "children": ["FF", "3A", "FF", "3B", "3C", "FF", "3D"]},
 {"id": "3A", "type": "3", "orientation": "5", "children": ["42", "FF"]}, 
 {"id": "42", "type": "1", "orientation": "1", "children": ["FF", "FF"]}, 
 {"id": "3B", "type": "3", "orientation": "5", "children": ["43", "FF"]}, 
 {"id": "43", "type": "1", "orientation": "5", "children": ["FF", "FF"]}, 
 {"id": "3C", "type": "3", "orientation": "5", "children": ["44", "FF"]}, 
 {"id": "44", "type": "1", "orientation": "1", "children": ["FF", "FF"]}, 
 {"id": "3D", "type": "3", "orientation": "5", "children": ["45", "FF"]}, 
 {"id": "45", "type": "1", "orientation": "5", "children": ["FF", "FF"]}'''
 
import json
import re

json_starts = [m.start() for m in re.finditer('{', string_in)]
json_ends = [m.start() for m in re.finditer('}', string_in)]
# assert( (len(json_starts)==len(json_ends)), 'JSON string does not have a complete number of objects')
json_in = []
for i in range(len(json_starts)):
    json_in.append( json.loads(string_in[json_starts[i]:json_ends[i]+1]))
# print(json_in)
module_ids = [j['id'] for j in json_in]
module_types = [int(j['type']) for j in json_in]
module_orientations = [int(j['orientation']) for j in json_in]
module_children_ids = [j['children'] for j in json_in]
print('module_ids:', module_ids)
print('module_types:', module_types)
print('module_orientations:', module_orientations)
print('module_children_ids:', module_children_ids)

# module children indices
module_attachments = []
n_modules = len(module_ids)
for i in range(n_modules):
    children_ids = module_children_ids[i]
    print('Module ' + str(i) + ' children serials: ' + str(children_ids))
    module_attachments_now = []

    for port_num in range(len(children_ids)):
        child_id = children_ids[port_num]
        if not(child_id == 'FF'):
            index_found = module_ids.index(child_id) if child_id in module_ids else None
            print('Found module index ' + str(index_found) + 
                  ' (id: '+ str(module_ids[index_found]) + 
                  ' orn: '+ str(module_orientations[index_found]-1) + 
                  ') on port ' + str(port_num))
        
            # None means it was not found, so something about this string is wrong.
            module_attachments_now.append( [port_num, 
                                            module_orientations[index_found]-1,
                                            index_found] )
    module_attachments.append(module_attachments_now)
print('attachments: ' + str(module_attachments))

node_type_enumeration = ['Null', 'Wheel_module', 'Twist','Bendy_module','Gripper Foot', \
                        'Gripper', 'O=6 module', 'Battery', 'Eigenbody', \
                        'TeeSplitter', 'Foot_module', 'Static straight', \
                         'Static 45 degree bend', 'Static 90 degree bend'] 
module_types_str = []
for module_type in module_types:
    module_types_str.append(node_type_enumeration[module_type])
print(module_types_str)

import description_assembler_2
description_assembler_2.description_assemble(module_types_str, module_attachments, module_ids)
import urdf_loader_test


