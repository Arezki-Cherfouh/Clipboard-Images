# Clipboard-Images

A background clipboard monitor that automatically exports images and vectors to your disk.

## Features
- **Auto-Detect**: Supports `image/png` and `image/svg+xml`.
- **Deduplication**: Uses MD5 hashing to ensure you don't save the same clip twice.
- **Timestamped**: Files are saved as `image_YYYY-MM-DD_HH-MM-SS`.
- **Lightweight**: Minimal CPU overhead using polling via `xclip`.

## Prerequisites
You must have `xclip` installed on your system:
```bash
sudo apt install xclip  # Debian/Ubuntu
sudo pacman -S xclip    # Arch

```

## Usage

1. Clone the repo.
2. Run the script: `python3 main.py`.
3. Any image you "Copy" or "Print Screen" will appear in the `/images` folder.

