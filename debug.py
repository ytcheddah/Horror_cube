import os

image_path = '/Users/ytcheddah/Documents/Projects/Horror_cube/images/MainCharacter/MC_Simpleton_SpritSheet.png'
print("File exists:", os.path.exists(image_path))


try:
    with open(image_path, 'rb') as f:
        print("Image file opened successfully!")
except FileNotFoundError:
    print("FileNotFoundError: Could not open the file.")
except Exception as e:
    print("An error occurred:", e)
