# TIFF to CZI Converter

This Python script converts TIFF images (commonly exported from microscopy imaging software) into Zeiss `.czi` files, preserving color channels and allowing custom channel order and naming. It leverages the `tifffile` and `pylibCZIrw` libraries to efficiently manage microscopy data for visualization in Zeiss ZEN software.

## Features

- Supports conversion of TIFF images into Zeiss CZI format.
- Automatically adjusts images to exactly three channels (padding or trimming as needed).
- Customizable channel naming (default: EGFP, Rhoda, Cy5).
- Easy swapping of channel order directly within the script.

## Requirements

- Python (3.8+ recommended)
- NumPy
- tifffile
- pylibCZIrw

Install dependencies using pip:

```bash
pip install numpy tifffile pylibCZIrw
```

## Usage

Place your TIFF files into the `newFISH` directory. If this directory does not exist, the script will create it automatically. Then run:

```bash
python convert_to_czi.py
```

The generated `.czi` files will be placed into the `output` directory.

## Customizing Channel Order

The script allows easy swapping or reordering of channels by modifying the following line:

```python
channels = channels[[1, 0, 2], :, :]  # Swap channels 0 and 1
```

Change the indices to rearrange channels as desired.

## Customizing Channel Names

Adjust the channel names displayed in ZEN by modifying:

```python
channel_names = {
    0: "EGFP",
    1: "Rhoda",
    2: "Cy5"
}
```

Update the names according to your experimental labels.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [pylibCZIrw](https://github.com/zeiss-microscopy/pylibCZIrw)
- [tifffile](https://github.com/cgohlke/tifffile)

## Contact

For questions or contributions, please open an issue or pull request on GitHub.