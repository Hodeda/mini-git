import os
import shutil
import string
import filecmp
import random
from datetime import datetime
import pydot


def init():
    """ Represents the init function:
         
         Images folder - containing images saves.
         staging_area - containing files the user would like to backup."""
    current_directory = os.getcwd()
    directory = '.wit'
    wit_folder=os.path.join(current_directory, directory)
    if not os.path.isdir(wit_folder):
        os.mkdir(wit_folder)

    images_folder=os.path.join(wit_folder, 'images')
    if not os.path.isdir(images_folder):
        os.mkdir(images_folder)

    staging_area=os.path.join(wit_folder, 'staging_area')
    if not os.path.isdir(staging_area):
        os.mkdir(staging_area)

    return staging_area

dest=init()


def add(src,dest):
  if not os.path.exists(dest):
        os.makedirs(dest)
  # Loop through the files
  for file_name in os.listdir(src):
    # Get the full paths of the source and dest files
    src_path = os.path.join(src, file_name)
    dest_path = os.path.join(dest, file_name)
    
    # If the source is a directory recur call the function
    if os.path.isdir(src_path):
      add(src_path,dest_path)
    else:
      # else copy all the files
      shutil.copy(src_path, dest_path)

# add(r'C:\Users\User\Desktop\week1',dest)

last_commit_id=None
def commit(message):
  main_directory = os.getcwd()
  images_folder=os.path.join(main_directory, '.wit\images')
  wit_folder=os.path.join(main_directory, '.wit')
  staging_area_folder = os.path.join(main_directory, '.wit\staging_area')
  # Check if the directories have the same files and directories
  if not os.path.isdir(wit_folder):
    return
  if os.path.isfile(os.path.join(wit_folder,"references.txt")):
    with open(os.path.join(wit_folder,"references.txt"),'r') as file:
      prev_commit_id=file.read()[len("HEAD="):40+len("HEAD=")]
    if compare_dirs(os.path.join(images_folder,prev_commit_id),staging_area_folder):
      return
  #making folder
  string_length = 40
  characters = list("1234567890abcdef") # creating a list with numbers and ABC letters.
  commit_id = "".join(random.choices(characters, k=string_length)) # randomly generating a string containg 40 chars with letters and numbers.
  new_folder = os.path.join(images_folder,commit_id)
  
  #making metadata file
  current_directory=os.chdir(images_folder) # changing the cwd to images_folder
  if not os.path.isdir(new_folder): # making each folder with randomized string.
    os.mkdir(commit_id)
    with open(str(commit_id)+ ".txt", "w") as file:
      current_time=datetime.now() 
      dt_string=current_time.strftime("%d/%m/%Y %H:%M:%S") 
      file.write(f"parent=None\n")
      file.write(f"date={dt_string}\n")
      file.write(f"message={message}")

  #making the save
  commit_id_path=os.path.join(images_folder,commit_id)
  add(dest,commit_id_path)

  #orginizing data for future
  wit_folder=os.path.join(main_directory, '.wit')
  prev_commit_exist=os.path.isfile(os.path.join(wit_folder,"references.txt"))
  if prev_commit_exist:
     with open(os.path.join(wit_folder,"references.txt"),'r') as file:
      prev_commit_id=file.read()[len("HEAD="):len(commit_id)+len("HEAD=")]
  with open(os.path.join(wit_folder,"references.txt"),'w') as file:
    file.write(f"HEAD={commit_id}\n")
    file.write(f"master={commit_id}")
   
  #updating commit id
  if prev_commit_exist:
    with open(str(commit_id)+ ".txt", "r") as file:
      file_list = file.readlines()
      file_list[0] = f"parent={prev_commit_id}\n"
      new_file_str = "".join(file_list)
    os.remove(str(commit_id)+ ".txt")
    with open(str(commit_id)+ ".txt", "w") as file:
      file.write(new_file_str)

 

def compare_dirs(dir1, dir2):
    # Check if the directories have the same files and directories
    if set(os.listdir(dir1)) != set(os.listdir(dir2)):
        return False

    # Check if the files and directories have the same content
    for entry in os.listdir(dir1):
        entry1 = os.path.join(dir1, entry)
        entry2 = os.path.join(dir2, entry)
        if os.path.isdir(entry1) and os.path.isdir(entry2):
            # Recursively compare the directories
            if not compare_dirs(entry1, entry2):
                return False
        elif not filecmp.cmp(entry1, entry2, shallow=False):
            # Compare the files
            return False

    # If the above checks pass, the directories are identical
    return True


  
  
# commit('im begging')


#entry1 is the file to print (dir_path1 is the dir to print)
def print_changed_files_in_dir(dir_path1,dir_path2):

  for entry in os.listdir(dir_path1):
    entry1 = os.path.join(dir_path1, entry)
    entry2 = os.path.join(dir_path2, entry)
    if os.path.isdir(entry1) and os.path.isdir(entry2):
        # Recursively compare the directories
        if not compare_dirs(entry1, entry2):
            return False
    elif not os.path.isfile(entry2):
      continue
    elif not filecmp.cmp(entry1, entry2, shallow=False):
        # Compare the files
        print(entry1.replace(dest+'\\',''))



def print_all_files_in_dir(dir_path,to_print=True):
  list1=[]
  for file_name in os.listdir(dir_path):
    if os.path.isdir(os.path.join(dir_path,file_name)):
      list1 += print_all_files_in_dir(os.path.join(dir_path,file_name))
    else:
      if to_print:
        print(file_name)
      list1.append(str(file_name))
  return list1

# folder 1 is staging area, the main folder we are going to compare each time to.
def print_file_difference(folder1, folder2):
  # Create a set of files in folder1
  # files1 = set(os.listdir(folder1))
  files1= set(print_all_files_in_dir(folder1,False))
  # Create a set of files in folder2
  # files2 = set(os.listdir(folder2))
  files2= set(print_all_files_in_dir(folder2,False))

  # Find the files that are present in folder2 but not in folder1
  unmatched_files = set(files2).difference(set(files1))
  if len(unmatched_files) == 0:
    unmatched_files = '' 
  # Print the unmatched files
  print("Files in commit id but not in staging area:", unmatched_files)

    
def status():
  main_directory = os.getcwd()
  images_folder=os.path.join(main_directory, '.wit\images')
  wit_folder=os.path.join(main_directory, '.wit')
  staging_area_folder = os.path.join(main_directory, '.wit\staging_area')
  if not os.path.isdir(wit_folder):
    return
  #printing current commit_id
  with open(os.path.join(wit_folder,"references.txt"),'r') as file:
    file_str = file.read()
    current_commit_id = file_str[len("HEAD="):40+len("HEAD=")]
    print("~Current commit id:" + current_commit_id+'')
  
  current_commit_id_path = os.path.join(images_folder, current_commit_id)

  print(f'~Changes to be committed:')
  #printing all files in dirs, recursivley
  changes_for_commit = print_all_files_in_dir(os.path.join(images_folder,current_commit_id))
  print(f'~Changes not staged for commit:')
  changes_not_staged = print_changed_files_in_dir(dest,os.path.join(images_folder,current_commit_id))
  print(f'~Untracked files:')
  print_file_difference(dest, current_commit_id_path)
  #bug in checkout.1
  if len(changes_for_commit)>0 or len(changes_not_staged)>0:
    return True
  else:
    return False

# status()

def checkout(commit_id):
  main_directory = os.getcwd()
  images_folder=os.path.join(main_directory, '.wit\images')
  wit_folder=os.path.join(main_directory, '.wit')
  staging_area_folder = os.path.join(main_directory, '.wit\staging_area')
  if not os.path.isdir(wit_folder):
    return
  
  status_message=status()
  if status_message == False: # if there's files staged for comitt or not, it wont copy to main dir 
    add(os.path.join(images_folder,str(commit_id)),main_directory)
  


# checkout('ddb338ba3e2c070fdae8197ef43d2d6f97a908d5')

def create_flow_chart(father,son): # ddb338, 1050f636
    main_directory = os.getcwd()
    images_folder=os.path.join(main_directory, '.wit\images')
    wit_folder=os.path.join(main_directory, '.wit')
    staging_area_folder = os.path.join(main_directory, '.wit\staging_area')
    # creating the graph 
    graph = pydot.Dot(graph_type='digraph')

    # add the nodes to the graph
    father_node = pydot.Node(father)
    son_node = pydot.Node(son)
    graph.add_node(father_node)
    graph.add_node(son_node)

    # checking if the prev commit also has a parent, if yes, recurselvy run until no parent
    with open(os.path.join(images_folder,father+".txt"),'r') as file:
      file_str=file.read()
      if 'parent=None' not in file_str:
        parent_commit_id = file_str[len("parent="):40+len("parent=")]
        temp_graph = create_flow_chart(parent_commit_id,father)
        temp_graph.add_node(son_node)
        temp_graph.add_edge(pydot.Edge(father_node,son_node))
        graph=temp_graph
      if 'parent=None' in file_str:
        graph.add_node(father_node)
        graph.add_edge(pydot.Edge(father_node, son_node))
        return graph
    return graph
    


def graph():  
  main_directory = os.getcwd()
  images_folder=os.path.join(main_directory, '.wit\images')
  wit_folder=os.path.join(main_directory, '.wit')
  staging_area_folder = os.path.join(main_directory, '.wit\staging_area')
  if not os.path.isdir(wit_folder):
    return
  
  with open(os.path.join(wit_folder,"references.txt"),'r') as file: # The leaf - getting the current commit id 
    file_str = file.read()
    current_commit_id = file_str[len("HEAD="):40+len("HEAD=")]
  with open(os.path.join(images_folder,current_commit_id+".txt"),'r') as file: # The Parent - getting the previous commit id
    file_str = file.read()
    previous_commit_id = file_str[len("parent="):40+len("parent=")]
  res_list=[]


  create_flow_chart(previous_commit_id,current_commit_id).write_png("flow_chart.png")

graph()
  