from PIL import Image, ImageChops
import os

def smart_process(file_path, output_name, is_icon=False):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found")
        return
    
    img = Image.open(file_path).convert("RGBA")
    
    # 1. Find bounding box of content (not white)
    # Background is white (255, 255, 255, 255)
    bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    
    if not bbox:
        print(f"No content found in {file_path}")
        return

    # Crop to content
    cropped = img.crop(bbox)
    
    # Convert white background to transparent
    # We use a threshold to handle slight compression artifacts
    def remove_white(img):
        img = img.convert("RGBA")
        data = img.getdata()
        new_data = []
        for item in data:
            # If the pixel is pure white (255, 255, 255)
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                # We turn it transparent
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        img.putdata(new_data)
        return img

    # Apply transparency to the cropped image
    cropped = remove_white(cropped)

    # 2. Icon must be 1:1, Logo should be landscape
    if is_icon:
        size = max(cropped.width, cropped.height)
        final_canvas = Image.new("RGBA", (size, size), (0, 0, 0, 0))
        offset_x = (size - cropped.width) // 2
        offset_y = (size - cropped.height) // 2
        final_canvas.paste(cropped, (offset_x, offset_y))
    else:
        # Logo: we keep the cropped aspect ratio (landscape)
        final_canvas = cropped

    final_canvas.save(output_name, "PNG")
    print(f"Saved optimized {output_name}")

brand_dir = "brand"
# Icon standard
smart_process(os.path.join(brand_dir, "icon@2x.png"), "brand/icon_test.png", is_icon=True)
# Logo standard
smart_process(os.path.join(brand_dir, "logo@2x.png"), "brand/logo_test.png", is_icon=False)
