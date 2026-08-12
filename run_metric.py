import torch
from piq import haarpsi, multi_scale_ssim
from tqdm import tqdm

import pycvvdp
from pycvvdp.utils import PU

def PU21(I, Y_peak=10000.0):
    pu = PU()
    PU_max = pu.encode(torch.as_tensor(Y_peak))
    I_PU = pu.encode(I) / PU_max
    return I_PU

def predict_quality(vs, metric="cvvdp", device="cpu"):
    
    if metric == "cvvdp":
        cvvdp = pycvvdp.cvvdp()
        quality, _ = cvvdp.predict_video_source(vs)
        return quality
    
    _, _, N_frames = vs.get_video_size()
    colorspaceT = "RGB2020"
    colorspaceR = "RGB2020"
    quality = 0.0
    for ff in tqdm(range(N_frames)):
        # Convert to photometric units then apply PU21
        T_photometric = vs.get_test_frame(ff, device=device, colorspace=colorspaceT).squeeze(2)
        R_photometric = vs.get_reference_frame(ff, device=device, colorspace=colorspaceR).squeeze(2)
        T = PU21(T_photometric)
        R = PU21(R_photometric)
        
        # Select different metric
        if metric == "HaarPSI":
            quality += haarpsi(T, R, data_range=1.) / N_frames
        elif metric == "MS-SSIM":
            quality += multi_scale_ssim(T, R, data_range=1.) / N_frames

    return quality

if __name__ == "__main__":
    test_fname = "example_media/C1_Drago1.png"
    ref_fname = "example_media/C1.hdr"
    I_T = pycvvdp.load_image_as_array(test_fname)
    I_R = pycvvdp.load_image_as_array(ref_fname)
    
    vs = pycvvdp.video_source.video_source_array(
        I_T, 
        I_R, 
        0,
        dim_order='HWC',
        display_photometry=("sdr_4k_30", "standard_hdr_linear"), 
    )
    
    Q = predict_quality(vs, metric="cvvdp", device="cpu")
    print(Q)