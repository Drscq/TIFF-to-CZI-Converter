import numpy as np
import tifffile
from pylibCZIrw import czi  # Zeiss library for writing CZI
import os
# import numpy as np
# import tifffile
# from pylibCZIrw import czi

print("CWD:", os.getcwd())

def convert_tif_to_czi(input_file, output_file, output_dir="output"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_czi_path = os.path.join(output_dir, output_file)

    # 1. Load the TIFF image
    img = tifffile.imread(input_file)

    # If the TIFF is (Y, X, C) with up to 4 channels (e.g., RGB), transpose to (C, Y, X).
    if img.ndim == 3 and img.shape[-1] <= 4:
        channels = np.transpose(img, (2, 0, 1))
    else:
        channels = img

    # We want exactly 3 channels total: EGFP, Rhoda, Cy5
    TARGET_CHANNELS = 3
    if channels.ndim != 3:
        raise ValueError(f"Expected a 3D array (C, Y, X). Got shape {channels.shape}.")

    current_channels = channels.shape[0]

    # 2. Trim or pad to 3 channels
    if current_channels > TARGET_CHANNELS:
        channels = channels[:TARGET_CHANNELS, :, :]
    elif current_channels < TARGET_CHANNELS:
        needed = TARGET_CHANNELS - current_channels
        zeros = np.zeros_like(channels[0])
        extra_stack = np.stack([zeros]*needed, axis=0)
        channels = np.concatenate([channels, extra_stack], axis=0)

    # 3. Swap channel 0 and channel 1
    channels = channels[[1, 0, 2], :, :]

    # 4. Write to a new CZI file
    with czi.create_czi(output_czi_path) as czi_file:
        for ch in range(TARGET_CHANNELS):
            data_plane = channels[ch]
            czi_file.write(data=data_plane, plane={'C': ch})

        # 5. Set channel names
        channel_names = {0: "EGFP", 1: "Rhoda", 2: "Cy5"}
        czi_file.write_metadata(channel_names=channel_names)

    print(f"Created '{output_czi_path}' with channels swapped between 0 and 1.")


# Example usage
input_dir = "newFISH"
output_dir = "output"
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
input_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith(".tif")]
for input_file in input_files:
    print(f"Converting '{input_file}' to CZI...")
    desired_output_file = os.path.splitext(os.path.basename(input_file))[0] + ".czi"
    convert_tif_to_czi(input_file, output_dir=output_dir, output_file=desired_output_file)
    print("Done.")
