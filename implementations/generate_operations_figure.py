"""
SAHQR Image Operations Demonstration
Shows image transformations (rotations, flipping) before and after SAHQR processing
"""

import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
from skimage import filters
from scipy.ndimage import rotate
import os

# Ensure output directory exists
output_dir = 'SAHQR_Results/figures'
os.makedirs(output_dir, exist_ok=True)

# ============================================================================
# 1. Load the medical image
# ============================================================================
minc_path = r'group4/07/2D/8v.2dus.00002sm.mnc'
nimg = nib.load(minc_path)
data = nimg.get_fdata()

# Handle dimensions
if len(data.shape) == 2:
    img = data
elif len(data.shape) == 3:
    if data.shape[0] == 1:
        img = data[0, :, :]
    elif data.shape[2] == 1:
        img = data[:, :, 0]
    else:
        img = data[data.shape[0]//2, :, :]
else:
    img = data

# Normalize to 0-1
img = (img - np.min(img)) / (np.max(img) - np.min(img) + 1e-8)

# Resize to 16x16 for SAHQR processing (as per the paper methodology)
from skimage.transform import resize
img_small = resize(img, (16, 16), anti_aliasing=True)

print(f"Original image shape: {img.shape}")
print(f"Resized for SAHQR: {img_small.shape}")

# ============================================================================
# 2. Define Image Transformation Functions
# ============================================================================
def rotate_90(image):
    return np.rot90(image, k=1)

def rotate_180(image):
    return np.rot90(image, k=2)

def rotate_270(image):
    return np.rot90(image, k=3)

def flip_horizontal(image):
    return np.fliplr(image)

def flip_vertical(image):
    return np.flipud(image)

# ============================================================================
# 3. SAHQR Encoding Simulation (Simplified for demonstration)
# ============================================================================
def compute_saliency(image):
    """Compute gradient-based saliency map"""
    grad = filters.sobel(image)
    p98 = np.percentile(grad, 98)
    if p98 > 0:
        saliency = np.clip(grad / p98, 0, 1)
    else:
        saliency = grad
    return saliency

def sahqr_encode_decode(image, alpha=1.0):
    """
    Simplified SAHQR encoding and decoding simulation.
    - Salient regions: Full precision (8-bit)
    - Non-salient regions: Compressed (4-bit)
    
    Returns the reconstructed image after SAHQR processing.
    """
    # Compute saliency
    saliency = compute_saliency(image)
    
    # Determine threshold
    threshold = np.mean(saliency) + alpha * np.std(saliency)
    
    # Create masks
    salient_mask = saliency >= threshold
    non_salient_mask = ~salient_mask
    
    # Encode
    # Salient: 8-bit precision (256 levels) - no loss
    # Non-salient: 4-bit precision (16 levels) - quantization
    img_encoded = image.copy()
    
    # For salient regions: full precision (no change in simulation)
    # For non-salient regions: reduce to 4-bit then back to 8-bit
    levels_4bit = 16
    img_encoded[non_salient_mask] = np.round(image[non_salient_mask] * (levels_4bit - 1)) / (levels_4bit - 1)
    
    return img_encoded, salient_mask

# ============================================================================
# 4. Create Figure: Before SAHQR (Original Full-Resolution Transformations)
# ============================================================================
transformations = [
    ("Original", lambda x: x),
    ("Rotate 90°", rotate_90),
    ("Rotate 180°", rotate_180),
    ("Rotate 270°", rotate_270),
    ("Flip Horizontal", flip_horizontal),
    ("Flip Vertical", flip_vertical),
]

fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes = axes.flatten()

for idx, (name, transform) in enumerate(transformations):
    # Use ORIGINAL full-resolution image
    transformed = transform(img)
    axes[idx].imshow(transformed, cmap='gray')
    axes[idx].set_title(f"(a{idx+1}) {name}", fontsize=10)
    axes[idx].axis('off')

plt.suptitle("Image Transformations Before SAHQR Encoding (Original Resolution)", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Figure_Operations_Before_SAHQR.png'), dpi=300, bbox_inches='tight')
print("Saved: Figure_Operations_Before_SAHQR.png")
plt.close()

# ============================================================================
# 5. Create Figure: After SAHQR (16x16 Encoded)
# ============================================================================
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes = axes.flatten()

for idx, (name, transform) in enumerate(transformations):
    # First resize to 16x16, apply transformation, then SAHQR encode
    transformed = transform(img_small)
    encoded, _ = sahqr_encode_decode(transformed)
    
    axes[idx].imshow(encoded, cmap='gray')
    axes[idx].set_title(f"(b{idx+1}) {name}", fontsize=10)
    axes[idx].axis('off')

plt.suptitle("Image Transformations After SAHQR Processing (16x16)", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'Figure_Operations_After_SAHQR.png'), dpi=300, bbox_inches='tight')
print("Saved: Figure_Operations_After_SAHQR.png")
plt.close()

# ============================================================================
# 6. Create Combined Figure (Before: Original, After: 16x16 SAHQR)
# ============================================================================
fig, axes = plt.subplots(2, 6, figsize=(18, 6))

# Row 1: Before SAHQR (Original Full Resolution)
for idx, (name, transform) in enumerate(transformations):
    transformed = transform(img)  # Full resolution
    axes[0, idx].imshow(transformed, cmap='gray')
    axes[0, idx].set_title(name, fontsize=9)
    axes[0, idx].axis('off')

# Row 2: After SAHQR (16x16)
for idx, (name, transform) in enumerate(transformations):
    transformed = transform(img_small)  # 16x16
    encoded, _ = sahqr_encode_decode(transformed)
    axes[1, idx].imshow(encoded, cmap='gray')
    axes[1, idx].axis('off')

# Add row labels
fig.text(0.02, 0.72, 'Before SAHQR\n(Original)', ha='center', va='center', fontsize=10, fontweight='bold')
fig.text(0.02, 0.28, 'After SAHQR\n(16x16)', ha='center', va='center', fontsize=10, fontweight='bold')

plt.suptitle("Geometric Transformations: Before and After SAHQR Encoding", fontsize=14, fontweight='bold')
plt.tight_layout(rect=[0.05, 0, 1, 0.96])
plt.savefig(os.path.join(output_dir, 'Figure_Operations_Combined.png'), dpi=300, bbox_inches='tight')
print("Saved: Figure_Operations_Combined.png")
plt.close()

# ============================================================================
# 7. Calculate and print quality metrics
# ============================================================================
from skimage.metrics import structural_similarity as ssim

print("\n" + "="*60)
print("Quality Metrics: SSIM between Before and After SAHQR")
print("="*60)

for name, transform in transformations:
    original = transform(img_small)
    after_sahqr, _ = sahqr_encode_decode(original)
    ssim_value = ssim(original, after_sahqr, data_range=1.0)
    print(f"{name:20s}: SSIM = {ssim_value:.6f}")

print("="*60)
print("All figures saved to SAHQR_Results/figures/")
