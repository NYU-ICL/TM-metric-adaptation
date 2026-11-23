import argparse

import torch
from piq import haarpsi, multi_scale_ssim
from tqdm import tqdm

import pycvvdp
from pycvvdp.utils import PU

METRICS = ("cvvdp", "HaarPSI", "MS-SSIM")

def PU21(I, Y_peak=10000.0):
    pu = PU()
    PU_max = pu.encode(torch.as_tensor(Y_peak))
    I_PU = pu.encode(I) / PU_max
    return I_PU.clamp(min=0.0)

def predict_quality(vs, metric="cvvdp", device="cpu"):
    if metric == "cvvdp":
        cvvdp = pycvvdp.cvvdp(device=torch.device(device))
        quality, _ = cvvdp.predict_video_source(vs)
        return quality.item()
    elif metric == "HaarPSI":
        metric_fn = haarpsi
    elif metric == "MS-SSIM":
        metric_fn = multi_scale_ssim
    else:
        raise ValueError(f"Unknown metric '{metric}'")

    _, _, N_frames = vs.get_video_size()
    quality = 0.0
    for ff in tqdm(range(N_frames)):
        # Convert to photometric units then apply PU21
        T = PU21(vs.get_test_frame(ff, device=device, colorspace="RGB2020").squeeze(2))
        R = PU21(vs.get_reference_frame(ff, device=device, colorspace="RGB2020").squeeze(2))
        quality += metric_fn(T, R, data_range=1.).item() / N_frames
    return quality

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

    # Separate display models for test and reference (requires pycvvdp>=0.6.0)
    vs = pycvvdp.video_source.video_source_array(
        I_T,
        I_R,
        0,
        dim_order='HWC',
        display_photometry=("sdr_4k_30", "standard_hdr_linear"),
    )

    for metric in ([args.metric] if args.metric else METRICS):
        Q = predict_quality(vs, metric=metric, device=device)
        print(f"{metric}: {Q:.4f}")
