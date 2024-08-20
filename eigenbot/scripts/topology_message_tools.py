import json
import re
import numpy as np

# string_in = '''{"id": "2B", "type": "8", "orientation": "1", "children": ["01", "3A", "FF", "3B", "3C", "3D" , "FF"]},
#  {"id": "01", "type": "3", "orientation": "1", "children": ["02"]}, 
#  {"id": "02", "type": "3", "orientation": "1", "children": ["03"]}, 
#  {"id": "03", "type": "10", "orientation": "1", "children": ["FF"]}, 
#  {"id": "3A", "type": "3", "orientation": "5", "children": ["42", "FF"]}, 
#  {"id": "42", "type": "1", "orientation": "1", "children": ["FF", "FF"]}, 
#  {"id": "3B", "type": "3", "orientation": "5", "children": ["43", "FF"]}, 
#  {"id": "43", "type": "1", "orientation": "5", "children": ["FF", "FF"]}, 
#  {"id": "3C", "type": "3", "orientation": "5", "children": ["44", "FF"]}, 
#  {"id": "44", "type": "1", "orientation": "1", "children": ["FF", "FF"]}, 
#  {"id": "3D", "type": "3", "orientation": "5", "children": ["45", "FF"]}, 
#  {"id": "45", "type": "1", "orientation": "5", "children": ["FF", "FF"]}'''

def parse_topology(string_in):
    print('---- Raw data: ----')
    print(string_in)
    print('--------')

    json_starts = [m.start() for m in re.finditer('{', string_in)]
    json_ends = [m.start() for m in re.finditer('}', string_in)]
    # assert( (len(json_starts)==len(json_ends)), 'JSON string does not have a complete number of objects')
    json_in = []
    for i in range(len(json_starts)):
        module_json = string_in[json_starts[i]:json_ends[i]+1]
        # print(module_json)
        json_loaded = json.loads(module_json)
        json_in.append( json_loaded )

    module_ids = list()
    module_types= list()
    module_orientations= list()
    module_children_ids= list()
    for j in json_in:
        # Sometimes a module reports its existance twice, which messes up the tree.
        # filter out repeat entries, if there are any
        if ( j['id'] not in module_ids):
            module_ids.append(j['id'])
            module_types.append(int(j['type'],16)) # converts from hexadecimal
            module_orientations.append(int(j['orientation'])-1) # NOTE: -1 because they are 1-indexed from the messages
            module_children_ids.append(j['children'])

    # FOR TESTING ONLY: zeros indicate bad detections. replace them with 0's
    for io in range(len(module_orientations)):
        if module_orientations[io]<0:
            module_orientations[io] = 0 

    # module_orientations = [int(j['orientation']) for j in json_in] # NOTE: 0-indexed from the messages

    print('module_ids ' + str(len(module_ids)) + ':', module_ids)
    print('module_types' + str(len(module_types)) + ':',  module_types)
    print('module_orientations ' + str(len(module_orientations)) + ':',  module_orientations)
    print('module_children_ids ' + str(len(module_children_ids)) + ':',  module_children_ids)





    # module children indices
    module_attachments = []
    graph_edges = []
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
                      ' orn: '+ str(module_orientations[index_found]) + 
                      ') on port ' + str(port_num))
                graph_edges.append([i, index_found, port_num, module_orientations[index_found]])
                
                # None means it was not found, so something about this string is wrong.
                module_attachments_now.append( [port_num, 
                                                module_orientations[index_found],
                                                index_found] )
        module_attachments.append(module_attachments_now)
    # print('attachments: ' + str(module_attachments))

    node_type_enumeration = ['Null', 'Wheel_module', 'Torsional_module',\
                            'Bendy_module','Gripper_foot', 'Gripper_module',\
                             'O=6 module', 'Battery', 'Eigenbody', \
                            'TeeSplitter', 'Foot_module', 'Static straight', \
                             'Static_45_deg', 'Static_90deg_module', 'Eigenbody'] 

# Hexadecimal (EigenBus) / Decimal (TitanScope) / Type (Name)
# 0x01 / 1 / Wheel actuator
# 0x02 / 2 / Twist actuator
# 0x03 / 3 / Bend actuator
# 0x04 / 4 / Gripper Foot
# 0x05 / 5 / Gripper
# 0x06 / 6 / O=6 module
# 0x07 / 7 / Battery
# 0x08 / 8 / Eigenbody
# 0x09 / 9 / TeeSplitter
# 0x0A / 10 / Foot
# 0x0B / 11 / Static no bend
# 0x0C / 12 / Static 45 degree bend
# 0x0D / 13 / Static 90 degree bend


    module_types_str = []
    for module_type in module_types:
        module_types_str.append(node_type_enumeration[module_type])
    print(module_types_str)

    print('edges:')
    print(graph_edges)

    return module_types_str, graph_edges, module_ids


# compare two topology messages and return if they are the same.
# Topology message might come in a different order each time.
 # to check if two messages m1 and m2 are the same, first check that the
 #  number of nodes is the same. Then go through each node in m2
 #   by serial number and see if it is in m1, and if so, if the 
 #   child serial, port, and orn are the same. This can be done via the
 #    graph_edges and module_ids lists, graph_edge = [parent_ind, child_ind, port, orn].
 #     So for each node, look for m2_module_ids[parent_ind] in m1_module_ids 
 #     and then compare the other fields.  
def compare_topologies(graph_edges1, module_ids1, graph_edges2, module_ids2 ):

    same_graph = True
    # check that they have the same number of nodes and edges
    if not(len(module_ids1)  == len(module_ids2) and 
           len(graph_edges1) == len(graph_edges2)):
        same_graph = False
        
    # check that they have the same nodes
    for module_id in module_ids1:
        if module_id not in module_ids2:
            same_graph = False
    
    if same_graph:
        # check that the edges all have the same properties
        edges_found = [False]*len(graph_edges1)
        for i in range(len(graph_edges1)):
            edge1 = graph_edges1[i]
            parent1, child1, port1, orn1 = edge1
            parent_serial1 = module_ids1[parent1]
            child_serial1 = module_ids1[child1]
            # loop through edges in graph2 and try to find this same edge1 in it
            for edge2 in graph_edges2:
                parent2, child2, port2, orn2 = edge2
                parent_serial2 = module_ids2[parent2]
                child_serial2 = module_ids2[child2]
                if (parent_serial1 == parent_serial2 and 
                    child_serial1 == child_serial2 and 
                    port1 == port2 and
                    orn1 == orn2):
                    edges_found[i] = True
        if not(np.all(edges_found)):
            same_graph = False
        
    return same_graph
