""" Main application entry point.

    python -m photonomist  ...

"""
import os

def path_string(photo_path:str)->str:
    """Verifies that the provided path is string

    :param photo_path: path to photos
    :return: photo to paths
    """
    if (photo_path is None) or (type(photo_path) != str) or (len(photo_path)<3):
        raise Exception("Your input is not valid!")
    return photo_path

def clean_path(photo_path:str)->str:
    """Removes second quotes/apostrophes in case that a user has typed/pasted the path with quote.

    :param photo_path: 'raw' path to photos
    :return: path to photos without redundant quotes
    """
    if ord(photo_path[0]) == 34 or ord(photo_path[0])==39:
        photo_path = photo_path[1:]
    if ord(photo_path[-1]) == 34 or ord(photo_path[-1])==39:
        photo_path = photo_path[:-1]
    return photo_path

def path_exists(photo_path:str):
    """Verifies that the provided path exists.

    :param photo_path: path to photos
    """
    if not os.path.exists(photo_path):
        raise FileNotFoundError("The provided path was not found!")

def path_items(photo_path:str):
    """Verifies that the provided path contains items (not only photos).

    :param photo_path: path to photos
    """
    if not os.listdir(photo_path):
        raise Exception("The provided path does not contain any files!")

def traverse_photo_path(photo_path:str):
    """Traverses/Identifies all the directories and files that exist under the provided path.
   
    :param photo_path: path to photos
    :return: A list with all paths that contain .jpg or .nef photos
    """
    photo_roots = []
    # traverse root directory, and list directories as dirs and files as files
    for root, dirs, files in os.walk(photo_path):
        for _file in files:
            if _file.lower().endswith('jpg') or _file.lower().endswith('nef'):
                if root not in photo_roots: photo_roots.append(root)
    
    return photo_roots

def path_photos(photo_roots:list):
    """Prints all the roots that contain photos. In no roots raises an error

    :param photo_roots: list with all roots that contain photos
    """
    if not photo_roots:
        raise Exception("The provided path does not contain any files with .jpg or .nef extension!")
    else:
        print('I found photos in: ')
        print(*photo_roots, sep = "\n")

    
def main():
    """ Execute the application.

    It asks the user to specify the path to the photos.
    It assesses the validity of the provided path and verifies that there is enough storage space.
    """

    # Photo path validation
    photo_path = clean_path(path_string(input("Enter the path to your photos: ")))
    path_exists(photo_path)
    path_items(photo_path)

    photo_roots = traverse_photo_path(photo_path)
    path_photos(photo_roots)

    # Export path validation
    export_path = clean_path(path_string(input("Enter the path where your photo-folders will be created: ")))
    path_exists(export_path)


# Make the script executable.

if __name__ == "__main__":
    raise SystemExit(main())
