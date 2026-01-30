# SAHQR: Saliency-Aware Hybrid Quantum Image Representation

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/Qiskit-0.45.0-purple.svg)](https://qiskit.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## Overview

This repository contains the implementation of **SAHQR (Saliency-Aware Hybrid Quantum Image Representation)**, a novel content-adaptive quantum image encoding scheme that leverages saliency detection to achieve efficient image compression while preserving diagnostically relevant regions.

## Paper

**Title:** SAHQR: Saliency-Aware Hybrid Quantum Image Representation for Medical Imaging Applications

**Target Journal:** Springer Neural Processing Letters

**Authors:** Mohd Mufiz Arbee

## Key Features

- **Content-Adaptive Encoding**: Unlike existing methods that treat all pixels uniformly, SAHQR adapts encoding precision based on visual saliency
- **Saliency Detection**: Gradient-based saliency detection identifies visually important regions
- **Hybrid Encoding Strategy**: 
  - Salient regions: Full 8-bit precision encoding
  - Non-salient regions: Compressed 4-bit encoding
- **Comprehensive Evaluation**: Compared against 10 state-of-the-art quantum image representation methods

## Methods Compared

| Method | Description |
|--------|-------------|
| FRQI | Flexible Representation of Quantum Images |
| NEQR | Novel Enhanced Quantum Representation |
| GQIR | Generalized Quantum Image Representation |
| MCQI | Multi-Channel Quantum Images |
| QRMW | Quantum Representation for Multi-Wavelength Images |
| EFRQI | Enhanced Flexible Representation of Quantum Images |
| 2D-QSNA | 2D Quantum State Normalization Approach |
| INEQR | Improved Novel Enhanced Quantum Representation |
| QPIE | Quantum Probability Image Encoding |
| QLR | Quantum Log-polar Representation |
| **SAHQR** | **Saliency-Aware Hybrid Quantum Representation (Proposed)** |

## Evaluation Parameters

1. **P1**: Qubits Required
2. **P2**: Circuit Depth
3. **P3**: Gate Count
4. **P4**: Encoding Time
5. **P5**: Scalability Factor
6. **P6**: Information Loss
7. **P7**: Compression Ratio
8. **P8**: Memory Overhead
9. **P9**: Gate Complexity
10. **P10**: Implementation Complexity

## Dataset

- **Source**: Medical Imaging NetCDF (MINC) format
- **Size**: 6,097 medical images
- **Preprocessing**: Resized to 16×16 pixels, normalized to [0, 1]

## Repository Structure

```
SAHQR/
├── implementations/
│   ├── sahqr_encoder.py          # SAHQR encoding implementation
│   ├── quantum_methods.py        # All 11 quantum methods implemented
│   ├── saliency_detection.py     # Gradient-based saliency detection
│   └── utils.py                  # Utility functions
├── results/
│   ├── tables/                   # Statistical results (CSV)
│   ├── figures/                  # Publication-quality figures
│   └── statistical_tests/        # Significance test results
├── FINAL_SAHQR.ipynb             # Complete experimental notebook
└── README.md
```

## Installation

```bash
# Clone the repository
git clone https://github.com/MArbeeGit/SAHQR.git
cd SAHQR

# Install dependencies
pip install -r requirements.txt
```

## Requirements

```
numpy>=1.22
scipy>=1.10
matplotlib>=3.7
qiskit>=0.45.0
nibabel>=5.0
scikit-image>=0.21
pandas>=2.0
```

## Usage

### Basic SAHQR Encoding

```python
from implementations.sahqr_encoder import SAHQREncoder

# Load image
image = load_medical_image("path/to/image.mnc")

# Initialize encoder
encoder = SAHQREncoder(alpha=1.0)  # Saliency threshold parameter

# Encode image
quantum_circuit, metrics = encoder.encode(image)

# Get circuit metrics
print(f"Qubits: {metrics['qubits']}")
print(f"Gate Count: {metrics['gates']}")
print(f"Circuit Depth: {metrics['depth']}")
```

### Running Full Comparison

```python
from implementations.quantum_methods import compare_all_methods

# Compare all 11 methods on dataset
results = compare_all_methods(
    dataset_path="path/to/dataset",
    output_dir="results/"
)
```

## Results Highlights

| Method | Qubits | Gates (Mean) | Depth (Mean) | Compression |
|--------|--------|--------------|--------------|-------------|
| FRQI | 9 | 121.6 | 113.6 | 2.06 |
| NEQR | 16 | 312.4 | 305.4 | 0.45 |
| **SAHQR** | **17** | **578.4** | **571.4** | **0.24** |

- SAHQR achieves the best compression ratio while maintaining content awareness
- Statistical significance confirmed at p < 0.001 for all comparisons

## Citation

If you use this code in your research, please cite:

```bibtex
@article{arbee2026sahqr,
  title={SAHQR: Saliency-Aware Hybrid Quantum Image Representation for Medical Imaging Applications},
  author={Arbee, Mohd Mufiz},
  journal={Neural Processing Letters},
  year={2026},
  publisher={Springer}
}
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

**Mohd Mufiz Arbee**
- Email: [arbee864@gmail.com]
- GitHub: [MArbeeGit]

## Acknowledgments

- Qiskit development team for the quantum computing framework
- Montreal Neurological Institute for the MINC medical imaging format
