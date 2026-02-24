import os
import time
import subprocess
import hashlib

SAVE_DIR = "images"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_timestamp():
    return time.strftime("%Y-%m-%d_%H-%M-%S")

def main():
    print("📌 Monitoring Clipboard (SVG & PNG Support)...")
    last_checksum = None
    
    while True:
        try:
            # 1. Ask Xclip what formats are available
            check_proc = subprocess.run(
                ['xclip', '-selection', 'clipboard', '-t', 'TARGETS', '-o'], 
                capture_output=True, text=True, timeout=0.5
            )
            targets = check_proc.stdout

            target_format = None
            extension = None

            # 2. PRIORITY: Check if it's an SVG first
            if 'image/svg+xml' in targets:
                target_format = 'image/svg+xml'
                extension = 'svg'
            # 3. FALLBACK: Check if it's a standard PNG (JPGs/WEBPs usually show up here too)
            elif 'image/png' in targets:
                target_format = 'image/png'
                extension = 'png'
            
            # 4. If we found a valid image format, grab it
            if target_format:
                image_proc = subprocess.run(
                    ['xclip', '-selection', 'clipboard', '-t', target_format, '-o'], 
                    capture_output=True, timeout=2.0
                )
                
                content = image_proc.stdout
                current_checksum = hashlib.md5(content).hexdigest()
                
                if current_checksum != last_checksum:
                    filename = f"{SAVE_DIR}/image_{get_timestamp()}.{extension}"
                    
                    with open(filename, "wb") as f:
                        f.write(content)
                    
                    print(f"✅ Saved as {extension.upper()}: {filename}")
                    last_checksum = current_checksum
            
        except Exception:
            pass

        time.sleep(1.0)

if __name__ == "__main__":
    main()






# import os
# import time
# import subprocess
# import hashlib

# SAVE_DIR = "images"
# if not os.path.exists(SAVE_DIR):
#     os.makedirs(SAVE_DIR)

# def get_timestamp():
#     return time.strftime("%Y-%m-%d_%H-%M-%S")

# def main():
#     print("📌 Monitoring Clipboard via XWayland Bridge (Silent)...")
    
#     last_checksum = None
    
#     # We poll faster (1.0s) because xclip usually doesn't trigger UI flickers
#     poll_interval = 1.0 

#     while True:
#         try:
#             # 1. Check TARGETS first using xclip (Lightweight)
#             # This asks XWayland: "What formats are currently in the clipboard?"
#             # -selection clipboard: standard Ctrl+C buffer
#             # -t TARGETS: list mime types
#             # -o: output to stdout
#             check_proc = subprocess.run(
#                 ['xclip', '-selection', 'clipboard', '-t', 'TARGETS', '-o'], 
#                 capture_output=True, 
#                 text=True, 
#                 timeout=0.5
#             )

#             # 2. Check if PNG image data is present
#             if 'image/png' in check_proc.stdout:
                
#                 # 3. Grab the actual image data to verify uniqueness
#                 # We pipe it directly to python to hash it, preventing duplicates
#                 image_proc = subprocess.run(
#                     ['xclip', '-selection', 'clipboard', '-t', 'image/png', '-o'], 
#                     capture_output=True, 
#                     timeout=2.0
#                 )
                
#                 # Calculate checksum to avoid saving the same image endlessly
#                 image_data = image_proc.stdout
#                 current_checksum = hashlib.md5(image_data).hexdigest()
                
#                 if current_checksum != last_checksum:
#                     filename = f"{SAVE_DIR}/image_{get_timestamp()}.png"
                    
#                     with open(filename, "wb") as f:
#                         f.write(image_data)
                    
#                     print(f"✅ Image Saved: {filename}")
#                     last_checksum = current_checksum
            
#         except subprocess.TimeoutExpired:
#             # Clipboard might be locked by another app momentarily
#             pass
#         except Exception as e:
#             # xclip returns error code 1 if selection is empty/cleared
#             pass

#         time.sleep(poll_interval)

# if __name__ == "__main__":
#     main()
