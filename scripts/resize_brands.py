from PIL import Image
import os

brand_dir = "brand"
files_to_process = [
    ("icon.png", "icon"),
    ("logo.png", "logo")
]

for src_name, base_name in files_to_process:
    src_path = os.path.join(brand_dir, src_name)
    if not os.path.exists(src_path):
        print(f"Skipping {src_name}, not found in {brand_dir}")
        continue
    
    with Image.open(src_path) as img:
        # Save as @2x (512x512)
        hd_path = os.path.join(brand_dir, f"{base_name}@2x.png")
        img.resize((512, 512), Image.Resampling.LANCZOS).save(hd_path)
        print(f"Created {hd_path}")
        
        # Save as standard (256x256)
        std_path = os.path.join(brand_dir, f"{base_name}.png")
        img.resize((256, 256), Image.Resampling.LANCZOS).save(std_path)
        print(f"Created {std_path}")
