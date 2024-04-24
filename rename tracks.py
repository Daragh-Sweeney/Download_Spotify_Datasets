import os

def rename_files_with_and_in_directory(directory):
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if ':' in filename or "'" in filename:
                old_filepath = os.path.join(root, filename)
                new_filename = filename.replace(':', '_').replace("'", "")
                new_filepath = os.path.join(root, new_filename)
                os.rename(old_filepath, new_filepath)
                print(f"Renamed {old_filepath} to {new_filepath}")


# Replace 'main_directory_path' with the path to the main directory containing subdirectories
main_directory_path = 'projects/tracks/'

# Traverse through each subdirectory and rename files
for subdir in os.listdir(main_directory_path):
    subdir_path = os.path.join(main_directory_path, subdir)
    if os.path.isdir(subdir_path):
        rename_files_with_and_in_directory(subdir_path)

