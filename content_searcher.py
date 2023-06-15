from datetime import datetime
import os
import glob

ext_whitelist = [".mdl", ".png", ".ttf", ".otf", ".pcf", ".wav", ".mp4", ".mp3", ".ogg"]

start_time = datetime.now()

search_list = ["C:/Users/johngetman/Downloads/InfinityRP/InfinityRP/addons", "C:/Users/johngetman/Downloads/InfinityRP/InfinityRP/gamemodes", "C:/Users/johngetman/Downloads/InfinityRP/InfinityRP/lua"]

def recursive_file_read(folder, file_name):
    find = False
    
    with os.scandir(folder) as entry_list:
        for entry in entry_list:
            if entry.is_dir():
                x = recursive_file_read(entry.path, file_name)
                if x:
                    find = True
                    break

            # is entry file

            if entry.is_file(): 
                with open(entry.path, encoding='utf-8') as file:
                    lines = file.readlines()
                    for line in lines:
                        if line.find(file_name) > 0:
                            find = True
                            break

    return find

def find_record_of_file(file_name):
    has_record = False
    
    for search in search_list:
        x = recursive_file_read(search, file_name)

        if x:
            has_record = True
            break

    return has_record

def recursive_file_find(folder_name):
    with os.scandir(folder_name) as entry_list:
        for entry in entry_list:
            if entry.is_dir():
                recursive_file_find(entry.path)

            # is entry file

            if entry.is_file(): # если нет упоминания файла, то файл будет удалён 
                name = entry.name
                name_, ext = os.path.splitext(name)

                if not ext in ext_whitelist:
                    continue

                has_record = find_record_of_file(entry.name)
                if not has_record:
                    print(entry.path + "     | was not found; to delete")

                    if ext == ".mdl":
                        for file in glob.glob(os.path.join(folder_name, name_ +'.*')):
                            os.remove(file)
                    else:
                        os.remove(entry.path)
                else:
                    print(entry.path + "     | found")

recursive_file_find(os.getcwd())

print(datetime.now() - start_time)