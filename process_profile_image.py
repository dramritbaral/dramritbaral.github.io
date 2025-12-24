#!/usr/bin/env python3
"""
Script to crop profile image and add white background
"""

try:
    from PIL import Image, ImageOps
    import sys
    import os
except ImportError:
    print("Error: Pillow (PIL) is not installed.")
    print("Please install it using: pip3 install Pillow")
    sys.exit(1)

def process_image(input_path, output_path):
    """Crop image to focus on face and add white background"""
    
    # Open the image
    img = Image.open(input_path)
    
    # Get image dimensions
    width, height = img.size
    print(f"Original size: {width}x{height}")
    
    # Calculate crop to focus on face (typically in upper center)
    # For a professional headshot, crop to focus on the face and upper body
    # Use a portrait aspect ratio (3:4 or similar)
    
    # Determine if we should crop to square or portrait
    # For headshots, portrait ratio works better (width:height ~ 3:4)
    target_aspect = 3/4  # Portrait aspect ratio
    
    if width / height > target_aspect:
        # Image is wider than target, crop width
        crop_width = int(height * target_aspect)
        crop_left = (width - crop_width) // 2
        crop_right = crop_left + crop_width
        crop_top = 0
        crop_bottom = height
    else:
        # Image is taller than target, crop height (focus on upper portion for face)
        crop_height = int(width / target_aspect)
        crop_top = 0  # Start from top to focus on face
        crop_bottom = crop_height
        crop_left = 0
        crop_right = width
    
    # Crop the image
    img_cropped = img.crop((crop_left, crop_top, crop_right, crop_bottom))
    print(f"Cropped size: {img_cropped.size[0]}x{img_cropped.size[1]}")
    
    # Create a white background
    # For professional headshots, use a square format with some padding
    # Or keep the portrait aspect ratio with white padding
    final_width = img_cropped.size[0]
    final_height = img_cropped.size[1]
    
    # Add white padding around the image (10% on each side)
    padding = int(min(final_width, final_height) * 0.1)
    final_width += padding * 2
    final_height += padding * 2
    
    white_bg = Image.new('RGB', (final_width, final_height), color='white')
    
    # Paste the cropped image onto the white background, centered with padding
    paste_x = padding
    paste_y = padding
    
    # If image has transparency, convert to RGB first
    if img_cropped.mode == 'RGBA':
        # Create white background for transparent areas
        white_bg_temp = Image.new('RGB', img_cropped.size, color='white')
        white_bg_temp.paste(img_cropped, mask=img_cropped.split()[3])  # Use alpha channel as mask
        img_cropped = white_bg_temp
    elif img_cropped.mode != 'RGB':
        img_cropped = img_cropped.convert('RGB')
    
    white_bg.paste(img_cropped, (paste_x, paste_y))
    
    # Resize for web use (max 1200px on longest side for good quality but reasonable file size)
    max_dimension = 1200
    if white_bg.size[0] > max_dimension or white_bg.size[1] > max_dimension:
        white_bg.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
        print(f"Resized to: {white_bg.size[0]}x{white_bg.size[1]}")
    
    # Save the processed image
    white_bg.save(output_path, 'JPEG', quality=90, optimize=True)
    print(f"Processed image saved to: {output_path}")
    print(f"Final size: {white_bg.size[0]}x{white_bg.size[1]}")

if __name__ == "__main__":
    input_file = "assets/img/Baral_Amrit_678-0882.jpg"
    output_file = "assets/img/Baral_Amrit_678-0882.jpg"  # Overwrite original
    
    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)
    
    # Create backup
    backup_file = input_file + ".backup"
    if not os.path.exists(backup_file):
        import shutil
        shutil.copy2(input_file, backup_file)
        print(f"Backup created: {backup_file}")
    
    process_image(input_file, output_file)
    print("\n✓ Image processing complete!")

