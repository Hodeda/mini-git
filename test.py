# import pydot

# def create_flow_chart(prev_commit_id,current_commit_id):
#     # Create the graph object
#     graph = pydot.Dot(graph_type='digraph')

#     # Add the nodes to the graph
#     father_node = pydot.Node(prev_commit_id)
#     son_node = pydot.Node(current_commit_id)
#     graph.add_node(father_node)
#     graph.add_node(son_node)

#     # Add the edges to the graph
#     graph.add_edge(pydot.Edge(father_node, son_node))

#     # Save the graph to a file
#     graph.write_png("flow_chart.png")

import os

def print_all_files_in_dir(dir_path,to_print=True):
  list1=[]
  for file_name in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path,file_name)):
        list1 += print_all_files_in_dir(os.path.join(dir_path,file_name),False)
    else:
      if to_print:
        print(file_name)
      list1.append(str(file_name))
  return list1








print(print_all_files_in_dir(r'C:\Users\User\Desktop\project\.wit\staging_area',False))


