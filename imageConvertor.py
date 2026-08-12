from PIL import Image
import os

def convert_image(input_path, output_format):
    try:
        # Open the image file
        with Image.open(input_path) as img:
            # Prepare output filename (e.g., photo.jpg -> photo.png)
            base_name = os.path.splitext(input_path)[0]
            output_path = f"{base_name}.{output_format.lower()}"
            
            # RGB conversion is needed if saving JPEG (PNG/WEBP can have transparency)
            if output_format.lower() in ['jpg', 'jpeg'] and img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
                
            img.save(output_path)
            print(f" Success! Saved as {output_path}")
            
    except Exception as e:
        print(f" Error converting file: {e}")

# Example Usage
file_to_convert = input("Enter the full path of the image: ")
target_format = input("Enter target format (e.g., png, jpg, webp): ")

convert_image(file_to_convert, target_format)