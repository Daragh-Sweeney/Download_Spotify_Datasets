import os
import zipfile

def zip_directory(directory, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                # Get relative path for storing in the ZIP file
                relative_path = os.path.relpath(file_path, directory)
                # Write the file to the ZIP archive
                zipf.write(file_path, relative_path)

# Example usage:
directory_to_zip = 'projects/tracks'
zip_filename = 'projects/tracks.zip'
zip_directory(directory_to_zip, zip_filename)