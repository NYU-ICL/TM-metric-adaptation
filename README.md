<div align="center">

<h1>Adapting Quality Metrics to Tone Mapping</h1>

<p><b>SIGGRAPH 2026 Conference Papers</b></p>

[**Kenneth Chen**](https://kenchen10.github.io/)<sup>1</sup>&ensp;
[**Dongyeon Kim**](https://dongyeon93.github.io)<sup>2</sup>&ensp;
[**Yuta Asano**](https://scholar.google.com/citations?user=N0WYkZkAAAAJ&hl=en&oi=ao)<sup>3</sup>&ensp;
[**Alexandre Chapiro**](https://achapiro.github.io/)<sup>3</sup>&ensp;
[**Qi Sun**](https://qisun.me/)<sup>1</sup>&ensp;
[**Rafał K. Mantiuk**](https://www.cl.cam.ac.uk/~rkm38/index.html)<sup>2</sup>

<sup>1</sup> <a href="https://www.immersivecomputinglab.org/research/"><img height="40" src="assets/nyu.png" align="middle" alt="New York University"></a>
&emsp;&emsp;
<sup>2</sup> <img height="32" src="assets/cambridge.png" align="middle" alt="University of Cambridge">
&emsp;&emsp;
<sup>3</sup> <img height="32" src="assets/meta.png" align="middle" alt="Meta">

<a href="https://kenchen10.github.io/projects/tmometric/index.html"><img src="https://img.shields.io/badge/Project-Page-blue" alt="Project page"></a>
<a href="https://doi.org/10.1145/3799902.3811107"><img src="https://img.shields.io/badge/Paper-ACM%20DL-red" alt="Paper"></a>
<a href="https://www.repository.cam.ac.uk/items/2f7c9a2a-ffe5-4d61-92b2-f6cb4928f119"><img src="https://img.shields.io/badge/Data-Cambridge%20Repository-green" alt="Data"></a>

<img src="assets/sig26-rep-img.png" width="90%" alt="Display-encoded HDR reference and tone-mapped test images pass through display models and a perceptual transfer function before the quality metric">

</div>

<sub>In tone mapping, the absolute luminance of HDR reference and tone-mapped test can differ significantly. To accurately predict quality, our display model maps display-encoded content to photometric values, given the specifications of the display. The colormap represents the photometric values in nits. Next, a perceptual transfer function, <i>P</i>() maps these values to a shared display-encoded representation (e.g. 0-1), usable by the quality metric.</sub>

## Abstract

Tone mapping evaluation is difficult because of the substantial differences in absolute luminance between high dynamic range (HDR) reference and tone-mapped standard dynamic range (SDR) test content. To address this challenge, we collected a new tone mapping evaluation dataset, focused on fundamental tone mapping operations, and combined it with several existing tone mapping quality assessment datasets. Rather than introducing new specialized metrics designed for tone-mapped content, we instead developed a set of techniques to adapt existing metrics for tone-mapped content. Our approach models the photometric differences between HDR reference and SDR test displays for accurate metric predictions. The technique consists of two steps: first, a display model converts display-encoded content to photometric values; second, these values are re-encoded using a perceptual transfer function for both HDR and tone-mapped images. We systematically evaluated both general-purpose image and video quality metrics with our adaptations and those specifically designed for tone mapping. With these adjustments, general-purpose metrics perform much better for tone mapping evaluation, consistently outperforming previously established specialized techniques. Additionally, we modified the ColorVideoVDP metric to be sensitive to absolute luminance changes, resulting in ColorVideoVDP-tm, which shows greatly improved performance and accepts photometric values as input. These results highlight the robustness of our adaptation technique and provide an improved protocol for evaluating future tone mapping quality metrics. Refer to our supplementary webpage for all data and stimuli.

## Dependencies

The code in this repository relies on [ColorVideoVDP](https://github.com/gfxdisp/ColorVideoVDP); please follow their installation instructions. Example metrics are provided by `piq`:

```bash
pip install piq
```

> [!NOTE]
> ColorVideoVDP-tm requires version 0.6.0, which is currently available on the [`dev_0_6_0`](https://github.com/gfxdisp/ColorVideoVDP/tree/dev_0_6_0) branch.

## Usage

By default, the scripts run all of their metrics on an example image from [our dataset](https://www.repository.cam.ac.uk/items/2f7c9a2a-ffe5-4d61-92b2-f6cb4928f119):

```bash
# Adapted metrics
python run_metric.py

# ColorVideoVDP-tm
python run_metric_cvvdp-tm.py
```

To use your own images or select a metric:

```bash
python run_metric.py --test test.png --ref reference.exr --metric HaarPSI
python run_metric_cvvdp-tm.py --test test.png --ref reference.exr --metric cvvdp
```

| Argument | Description |
| --- | --- |
| `--test` | Tone-mapped SDR test image |
| `--ref` | HDR reference image, with linear values in cd/m<sup>2</sup> and the same resolution as the test |
| `--metric` | `HaarPSI` or `MS-SSIM`; also `cvvdp` (ColorVideoVDP-tm) in `run_metric_cvvdp-tm.py`. Runs all if omitted |

For example, with the provided Castle images:

```bash
python run_metric.py --test example_media/Castle.png --ref example_media/Castle.exr --metric HaarPSI
# HaarPSI: 0.9404

python run_metric_cvvdp-tm.py --test example_media/Castle.png --ref example_media/Castle.exr --metric cvvdp
# cvvdp: 7.1709
```

The display models are set in the scripts; adjust them to match your displays.

## Data

User study stimuli, raw data and results scaled to Just-Objectionable-Difference (JOD) units for our work can be found [here](https://www.repository.cam.ac.uk/items/2f7c9a2a-ffe5-4d61-92b2-f6cb4928f119).

## Acknowledgements

Thank you to the user study participants for their time and to the anonymous reviewers for their insightful feedback.

## Contact

Contact [Kenneth Chen](https://kenchen10.github.io) ([kennychen@nyu.edu](mailto:kennychen@nyu.edu)) with any questions about the codebase or data.

## Citation

If you find this project helpful to your research, please consider citing us:

```bibtex
@inproceedings{
    chen2026adapting,
    author = {Chen, Kenneth and Kim, Dongyeon and Asano, Yuta and Chapiro, Alexandre and Sun, Qi and Mantiuk, Rafa\l{} K},
    title = {Adapting Quality Metrics to Tone Mapping},
    year = {2026},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3799902.3811107},
    doi = {10.1145/3799902.3811107},
    booktitle = {Proceedings of the Special Interest Group on Computer Graphics and Interactive Techniques Conference Conference Papers},
    series = {SIGGRAPH Conference Papers '26}
}
```
