from functools import reduce
import os, shutil, sys

def main():
    errorcheck_arguments(len(sys.argv))
    source_path = assign_path(1)
    destination_path = assign_path(2)
    errorcheck_source(source_path)

    total_size = get_total_size(source_path)
    print(progress_bar(5029, total_size))
    #copy_directory(source_path, destination_path)


def progress_bar(current_progress, total):

    percent = (current_progress / (total * 1.0)) * 100
    
    def determine_bartype(n):
        if (n / (30 * 1.0)) * 100 < percent:
            return '#'
        else:
            return '-'
        
    bar = reduce((lambda x, y: x + y),
             map((lambda x: determine_bartype(x)),
             range(1, 30)))
    return ("Copying Files |%s| %.f%% Complete " %
            (bar, percent))

def copy_directory(source, destination):

    for file in os.listdir(source):
        current_file = os.path.join(source, file)
        if os.path.isdir(current_file):
            os.makedirs(os.path.join(destination, file))
            copy_directory(current_file, os.path.join(destination, file))
        else:
            shutil.copy2(current_file, destination)
            

def get_total_size(path):

    def get_size(current_file):
        if (os.path.isdir(os.path.join(path, current_file))):
            if os.listdir(os.path.join(path, current_file)):
                return get_total_size(os.path.join(path, current_file))
        return os.path.getsize(os.path.join(path, current_file))
    
    return reduce((lambda x, y: x + y),
              map((lambda x: get_size(x)), os.listdir(path)))

def assign_path(argv_position):
    return os.path.abspath(sys.argv[argv_position])

def errorcheck_source(source):
    if (not (os.path.isdir(source) and
             os.path.exists(source))):
        print("Error -- Source must exist" +
              "\nand must be a directory."+
              "\nExiting now.")
        sys.exit()

def errorcheck_arguments(arguments):
    if(arguments != 3):
        print("Error -- Must input 2 arguments" +
              "\nOne for the backup source" +
              "\nOne for the backup destination")
        sys.exit()
        
if __name__ == "__main__":
    main()
