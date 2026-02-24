import time
import os
import sys
import hashlib

# Configuration
SAVE_DIR = "images"

def ensure_image_folder():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

def get_timestamp():
    return time.strftime("%Y-%m-%d_%H-%M-%S")

# ==========================================
#  LINUX LOGIC (Uses xclip via subprocess)
# ==========================================
def monitor_linux():
    import subprocess
    
    print("🐧 Linux detected.")
    print(f"📌 Monitoring Clipboard via xclip (SVG & PNG Support)...")
    
    # Check if xclip is installed
    try:
        subprocess.run(['xclip', '-version'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("❌ Error: 'xclip' is not installed. Please run: sudo apt install xclip")
        return

    last_checksum = None
    ensure_image_folder()

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
            # 3. FALLBACK: Check if it's a standard PNG
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
                # Create a checksum to compare content, not just existence
                current_checksum = hashlib.md5(content).hexdigest()
                
                if current_checksum != last_checksum:
                    filename = f"{SAVE_DIR}/image_{get_timestamp()}.{extension}"
                    
                    with open(filename, "wb") as f:
                        f.write(content)
                    
                    print(f"✅ Saved as {extension.upper()}: {filename}")
                    last_checksum = current_checksum
            
        except Exception as e:
            # Squelch errors during polling, print only if specific debugging needed
            pass

        time.sleep(1.0)

# ==========================================
#  WINDOWS / MAC LOGIC (Uses Pillow)
# ==========================================
def monitor_win_mac():
    try:
        from PIL import ImageGrab
        import io
    except ImportError:
        print("❌ Error: Pillow library not found.")
        print("👉 Please install it: pip install Pillow")
        return

    print(f"💻 {sys.platform} detected.")
    print("📌 Monitoring Clipboard via Pillow... (Ctrl+C to stop)")
    
    ensure_image_folder()
    last_bytes = None

    while True:
        try:
            img = ImageGrab.grabclipboard()

            # Check if we got an image (and not a list of file paths)
            if img is not None and not isinstance(img, list):
                
                # BUG FIX: Compare Bytes, not Object Identity
                # Convert image to bytes in memory to check content
                with io.BytesIO() as output:
                    img.save(output, format="PNG")
                    current_bytes = output.getvalue()
                
                if current_bytes != last_bytes:
                    filename = f"{SAVE_DIR}/image_{get_timestamp()}.png"
                    img.save(filename, "PNG")
                    print(f"✅ Saved image -> {filename}")
                    
                    last_bytes = current_bytes # Update the 'last' state
            
            time.sleep(0.8)

        except KeyboardInterrupt:
            print("\nStopped.")
            break
        except Exception as e:
            print(f"⚠️ Error: {e}")

# ==========================================
#  MAIN ENTRY POINT
# ==========================================
def main():
    if sys.platform.startswith("linux"):
        monitor_linux()
    else:
        # Handles 'win32' (Windows) and 'darwin' (macOS)
        monitor_win_mac()

if __name__ == "__main__":
    main()