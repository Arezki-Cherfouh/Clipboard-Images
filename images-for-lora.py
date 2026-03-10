import os
import time
import subprocess
import hashlib

SAVE_DIR = "images"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def get_next_filename():
    # Find the highest existing number
    existing_files = [f for f in os.listdir(SAVE_DIR) if f.endswith('.png') or f.endswith('.svg')]
    numbers = [int(f.split('.')[0]) for f in existing_files if f.split('.')[0].isdigit()]
    next_num = max(numbers) + 1 if numbers else 1
    return f"{next_num:03d}"

def main():
    print("📌 Monitoring Clipboard (Counter Mode)...")
    last_checksum = None
    
    while True:
        try:
            check_proc = subprocess.run(
                ['xclip', '-selection', 'clipboard', '-t', 'TARGETS', '-o'], 
                capture_output=True, text=True, timeout=0.5
            )
            targets = check_proc.stdout

            target_format = None
            extension = None

            if 'image/svg+xml' in targets:
                target_format = 'image/svg+xml'
                extension = 'svg'
            elif 'image/png' in targets:
                target_format = 'image/png'
                extension = 'png'
            
            if target_format:
                image_proc = subprocess.run(
                    ['xclip', '-selection', 'clipboard', '-t', target_format, '-o'], 
                    capture_output=True, timeout=2.0
                )
                
                content = image_proc.stdout
                current_checksum = hashlib.md5(content).hexdigest()
                
                if current_checksum != last_checksum:
                    # Get counter-based filename
                    base_name = get_next_filename()
                    
                    # Save image
                    img_filename = os.path.join(SAVE_DIR, f"{base_name}.{extension}")
                    with open(img_filename, "wb") as f:
                        f.write(content)
                    
                    # Create matching empty text file
                    txt_filename = os.path.join(SAVE_DIR, f"{base_name}.txt")
                    open(txt_filename, 'w').close()
                    
                    print(f"✅ Saved: {base_name}.{extension} and {base_name}.txt")
                    last_checksum = current_checksum
            
        except Exception:
            pass

        time.sleep(1.0)

if __name__ == "__main__":
    main()