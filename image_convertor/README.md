# Image Convertor

Convert one or more images to a different format using Pillow. Supports all formats registered by PIL (PNG, JPEG, WebP, BMP, TIFF, GIF, and more).

## Prerequisites

- **Python 3.10+**
- **Pillow**

Install the dependency:

```bash
pip install Pillow
```

## Usage

```bash
python main.py <input_path> [<input_path> ...] <output_extension> [options]
```

### Arguments

| Argument | Description |
|---|---|
| `input_path` | One or more paths to input image files |
| `output_extension` | Target format (e.g. `png`, `jpeg`, `webp`) |

### Options

| Flag | Default | Description |
|---|---|---|
| `--output-dir` | `converted` | Directory where converted files are saved |
| `--overwrite` | off | Overwrite files that already exist in the output directory |
| `--dry-run` | off | Preview what would happen without writing any files |

## Examples

Convert a single image to WebP:

```bash
python main.py photo.jpg webp
```

Convert multiple images to PNG and save to a custom folder:

```bash
python main.py a.jpg b.bmp png --output-dir out
```

Preview conversions without writing files:

```bash
python main.py photo.jpg png --dry-run
```

Overwrite existing output files:

```bash
python main.py photo.png jpeg --overwrite
```

## Output

Converted files are placed in the output directory (default: `converted/`) alongside the script. The original filename is preserved with the new extension.

```
converted/
  photo.jpeg
```
