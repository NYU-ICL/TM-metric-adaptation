import torch
from piq import haarpsi, multi_scale_ssim
from pyiqa import create_metric
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
    elif metric == "DISTS":
        metric = create_metric('dists', device=device)
    
    _, _, N_frames = vs.get_video_size()
    colorspaceT = "RGB2020"
    colorspaceR = "RGB2020"
    quality = 0.0
    for ff in tqdm(range(N_frames)):
        # Convert to photometric units then apply PU21
        T = PU21(vs.get_test_frame(ff, device=device, colorspace=colorspaceT).squeeze(2))
        R = PU21(vs.get_reference_frame(ff, device=device, colorspace=colorspaceR).squeeze(2))
        
        # Select different metric
        if metric == "HaarPSI":
            quality += haarpsi(T, R, data_range=1.) / N_frames
        elif metric == "MS-SSIM":
            quality += multi_scale_ssim(T, R, data_range=1.) / N_frames
        elif metric == "DISTS":
            quality += metric(T, R) / N_frames
    return quality

if __name__ == "__main__":
    test_fname = "example_media/C1_Drago1.png"
    ref_fname = "example_media/C1.hdr"
    I_T = pycvvdp.load_image_as_array(test_fname)
    I_R = pycvvdp.load_image_as_array(ref_fname)
    
    disp_photo_R = pycvvdp.display_model.vvdp_display_photo_eotf(Y_peak=4000, source_colorspace='BT.709', contrast=4000/.03, EOTF="linear")
    disp_photo_T = pycvvdp.display_model.vvdp_display_photo_eotf(Y_peak=200, source_colorspace='sRGB', contrast=1000, EOTF="sRGB")
    vs = pycvvdp.video_source.video_source_array(
        I_T, 
        I_R, 
        0,
        dim_order='HWC',
        test_display_photometry=disp_photo_T, 
        reference_display_photometry=disp_photo_R,
    )
    
    Q = predict_quality(vs, metric="MS-SSIM", device="cpu")
    print(Q)