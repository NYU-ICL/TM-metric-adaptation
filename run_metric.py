import argparse

import torch
from piq import haarpsi, multi_scale_ssim

import pycvvdp
from pycvvdp.utils import PU
from pycvvdp.video_source import numpy2torch_frame

METRICS = ("HaarPSI", "MS-SSIM")

def PU21(I, Y_peak=10000.0):
    pu = PU()
    PU_max = pu.encode(torch.as_tensor(Y_peak))
    I_PU = pu.encode(I) / PU_max
    return I_PU.clamp(min=0.0)

def predict_quality(T_photometric, R_photometric, metric="HaarPSI"):
    """Inputs are [1,3,H,W] tensors of linear RGB in cd/m^2."""
    T = PU21(T_photometric)
    R = PU21(R_photometric)

    # Select different metric
    if metric == "HaarPSI":
        return haarpsi(T, R, data_range=1.)
    elif metric == "MS-SSIM":
        return multi_scale_ssim(T, R, data_range=1.)
    raise ValueError(f"Unknown metric '{metric}'")

def parse_args():
    parser = argparse.ArgumentParser(description="Predict the quality of a tone-mapped image.")
    parser.add_argument("--test", default="example_media/Castle.png", help="tone-mapped SDR test image")
    parser.add_argument("--ref", default="example_media/Castle.exr", help="HDR reference image, linear values in cd/m^2")
    parser.add_argument("--metric", choices=METRICS, help="metric to run (default: all)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    device = "cpu"

    I_T = pycvvdp.load_image_as_array(args.test)
    I_R = pycvvdp.load_image_as_array(args.ref)

    dm_T = pycvvdp.vvdp_display_photo_eotf(
        Y_peak=200, contrast=200/.3, source_colorspace="sRGB", EOTF="2.2",
    )
    dm_R = pycvvdp.vvdp_display_photo_eotf(
        Y_peak=1000, contrast=1000000, source_colorspace="BT.709-linear",
    )

    # Integer images are scaled to 0-1, then each display model converts to photometric units
    T_photometric = dm_T.forward(numpy2torch_frame(I_T, 0, device)).squeeze(2)
    R_photometric = dm_R.forward(numpy2torch_frame(I_R, 0, device)).squeeze(2)

    for metric in ([args.metric] if args.metric else METRICS):
        Q = predict_quality(T_photometric, R_photometric, metric=metric)
        print(f"{metric}: {Q.item():.4f}")
