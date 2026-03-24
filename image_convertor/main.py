from PIL import Image
import os
import sys
from dataclasses import dataclass


SUPPORTED_EXTENSIONS = {ext.lstrip('.').lower() for ext in Image.registered_extensions()}


@dataclass
class ConvertResult:
  input: str
  output: str | None
  skipped: bool
  reason: str | None = None


def convert_img(
  input_path: str,
  output_extension: str,
  overwrite: bool = False,
  output_dir: str = 'converted',
  dry_run: bool = False,
) -> ConvertResult:
  ext = output_extension.lstrip('.').lower()

  if ext not in SUPPORTED_EXTENSIONS:
    raise ValueError(f'Unsupported format: {output_extension}. Supported: {sorted(SUPPORTED_EXTENSIONS)}')

  if not os.path.exists(input_path):
    raise FileNotFoundError(f'No such file: {input_path}')

  clean_name = os.path.splitext(os.path.basename(input_path))[0]
  output_path = os.path.join(output_dir, f'{clean_name}.{ext}')

  if os.path.exists(output_path) and not overwrite:
    return ConvertResult(input=input_path, output=output_path, skipped=True, reason='already exists')

  if dry_run:
    return ConvertResult(input=input_path, output=output_path, skipped=True, reason='dry run')

  os.makedirs(output_dir, exist_ok=True)

  with Image.open(input_path) as img:
    img.save(output_path)

  return ConvertResult(input=input_path, output=output_path, skipped=False)


def convert_many(
  input_paths: list[str],
  output_extension: str,
  overwrite: bool = False,
  output_dir: str = 'converted',
  dry_run: bool = False,
) -> list[ConvertResult]:
  return [
    convert_img(p, output_extension, overwrite=overwrite, output_dir=output_dir, dry_run=dry_run)
    for p in input_paths
  ]


if __name__ == '__main__':
  import argparse

  parser = argparse.ArgumentParser(description='Convert images to a different format.')
  parser.add_argument('input_paths', nargs='+', help='One or more input image paths')
  parser.add_argument('output_extension', help='Target format extension (e.g. png, jpeg, webp)')
  parser.add_argument('--overwrite', action='store_true', help='Overwrite existing output files')
  parser.add_argument('--output-dir', default='converted', help='Output directory (default: converted)')
  parser.add_argument('--dry-run', action='store_true', help='Preview output paths without writing files')
  args = parser.parse_args()

  try:
    results = convert_many(
      args.input_paths,
      args.output_extension,
      overwrite=args.overwrite,
      output_dir=args.output_dir,
      dry_run=args.dry_run,
    )
    for r in results:
      status = 'skipped' if r.skipped else 'converted'
      reason = f' ({r.reason})' if r.reason else ''
      print(f'{status}: {r.input} -> {r.output}{reason}')
  except (FileNotFoundError, ValueError) as e:
    print(f'Error: {e}', file=sys.stderr)
    sys.exit(1)
