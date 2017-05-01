"""
Backup

A script to copy your files from one location to another.
Input a source directory and a destination directory.

Robert Stefanic (c) 2017

"""

from functools import reduce
import os, shutil, sys

def main():

    # Check the sources and make sure the arguments are valid
    errorcheck_arguments(len(sys.argv))
    source_path = assign_path(1)
    destination_path = assign_path(2)
    errorcheck_source(source_path)

    # Compute the size of the files and move the files
    total_size = get_total_size(source_path)
    copy_directory(source_path, destination_path, total_size)
    print("\nDone.")
    sys.exit()

### IO Actions ###

def copy_directory(source, destination, total_size):
""" Copy the directory from the source path to the destination path  """

    def copy_files(src, dest, bytes_copied):
        """ Copy the files from a given path to the destination path """
        
        for file in os.listdir(src):
            cur_file = os.path.join(src, file)
            if os.path.isfile(cur_file):
                shutil.copy2(cur_file, dest)
                bytes_copied += os.path.getsize(cur_file)
                print_progress_bar(progress_bar(bytes_copied, total_size))
                continue
            else:
                os.makedirs(os.path.join(dest, file))
                copy_files(cur_file,
                           os.path.join(dest, file),
                           bytes_copied)
                bytes_copied += get_total_size(cur_file)

        print_progress_bar(progress_bar(bytes_copied, total_size))

    # Get the total size of the files to copy and begin copying
    print("Total size of files to copy: %s bytes..." % total_size)
    copy_files(source, destination, 0)

    
def print_progress_bar(progress):
""" Write to the console, and overwrite what's currently displayed  """

    sys.stdout.write(progress)
    sys.stdout.flush()


### Pure Functions ###

def get_total_size(path):
""" Determine the size of a directory """

    def get_size(current_file):
        if (os.path.isdir(os.path.join(path, current_file))):
            if os.listdir(os.path.join(path, current_file)):
                return get_total_size(os.path.join(path, current_file))
        return os.path.getsize(os.path.join(path, current_file))

    if os.listdir(path):
        return reduce((lambda x, y: x + y),
                  map((lambda x: get_size(x)), os.listdir(path)))
    else:
        return 0

    
def progress_bar(current_progress, total):
""" Determine the current progress and return a string """

    percent = (current_progress / (total * 1.0)) * 100
    
    def determine_bartype(n):
        if (n / (30 * 1.0)) * 100 < percent:
            return '#'
        else:
            return '-'
        
    bar = reduce((lambda x, y: x + y),
             map((lambda x: determine_bartype(x)),
             range(1, 30)))
    return ("Copying Files [%s] %.f%% Complete \r" %
            (bar, percent))


def assign_path(argv_position):
""" Grab the paths from the system arguments """

    return os.path.abspath(sys.argv[argv_position])


### Error Checks ###

def errorcheck_source(source):
""" Ensure the source input exists and is a directory """

    if (not (os.path.isdir(source) and
             os.path.exists(source))):
        print("Error -- Source must exist" +
              "\nand must be a directory."+
              "\nExiting now.")
        sys.exit()

def errorcheck_arguments(arguments):
""" Make sure the program recieved two arguments  """

    if(arguments != 3):
        print("Error -- Must input 2 arguments" +
              "\nOne for the backup source" +
              "\nOne for the backup destination")
        sys.exit()
        
if __name__ == "__main__":
    main()
