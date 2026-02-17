import matplotlib.pyplot as plt
import numpy as np
from skimage import filters
import os

# Ensure directory exists
output_dir = 'SAHQR_Results/figures'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

import nibabel as nib

# 1. Load the actual MINC image
minc_path = r'group4/05/2D/6u.2dus.00016sm.mnc'
try:
    nimg = nib.load(minc_path)
    data = nimg.get_fdata()
    # Handle dimensions - take middle slice if 3D, or use as is if 2D
    if len(data.shape) >= 2:
        # If 3D, take middle slice from the first dimension (often z or t in medical imaging, but varies)
        # MINC is often (z, y, x) or (x, y, z). Let's start with a safe heuristic or just take the middle of the largest dimension?
        # A clearer heuristic: if 3D, slice the specific index.
        # Let's try to just slice the first dimension index 0 if it's "2D" but stored in 3D structure,
        # or middle if it's a volume.
        # User path says "2D", so it's likely a 2D slice.
        if len(data.shape) == 2:
            img = data
        elif len(data.shape) == 3:
            # Assume (slice, h, w) or (h, w, slice). Usually MINC2 is (z,y,x)
            # Let's pick middle slice of the smallest dimension, usually depth
            # But "2D" folder suggests flat.
            # Safe bet: squeeze it.
            img = data[:, :, 0] if data.shape[2] == 1 else data[data.shape[0]//2, :, :]
            # If that fails visually, we'll know.
            # Actually, simply taking the middle of axis 0 is often safe for single-slice volumes.
            # Let's just blindly take slice 0 if it's really "2D" content.
            if data.shape[0] == 1:
                img = data[0, :, :]
            elif data.shape[2] == 1:
                img = data[:, :, 0]
            else:
                 img = data[data.shape[0]//2, :, :]
    else:
        raise ValueError("Image dimensions not supported")
    
    # Normalize to 0-1
    img = (img - np.min(img)) / (np.max(img) - np.min(img))
    
except Exception as e:
    print(f"Error loading MINC file: {e}")
    # Fallback only if file requires it, but user gave specific file.
    # Let's re-raise to fail fast so we can fix.
    raise e

# 2. Compute Saliency (Sobel)
grad = filters.sobel(img)
# Robust normalization to make salient regions pop (red)
# Saturate top 2% to ensure we utilize the full heatmap range
p98 = np.percentile(grad, 98)
if p98 > 0:
    saliency = np.clip(grad / p98, 0, 1)
else:
    saliency = grad
    
# 3. Create the Plot
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Plot A: Original
axes[0].imshow(img, cmap='gray')
axes[0].set_title("(a) Original Medical Image\n(Heterogeneous Content)")
axes[0].axis('off')

# Plot B: Saliency Map
axes[1].imshow(saliency, cmap='jet', vmin=0, vmax=1)
axes[1].set_title("(b) Saliency Map\n(Red = High Importance)")
axes[1].axis('off')

# Plot C: Concept Grid
# Overlay grid
axes[2].imshow(img, cmap='gray', alpha=0.3)
axes[2].set_title("(c) SAHQR Resource Allocation\n(Adaptive Grid)")
axes[2].axis('off')

height, width = img.shape

# Draw coarse grid everywhere (step ~20% of image size)
step_y = max(1, height // 10)
step_x = max(1, width // 10)

for y in range(0, height, step_y):
    axes[2].axhline(y, color='black', linewidth=0.5)
for x in range(0, width, step_x):
    axes[2].axvline(x, color='black', linewidth=0.5)

# Detect ROI for fine grid
# Use simple threshold
threshold = np.mean(saliency) + 2.0 * np.std(saliency) # High threshold to get core
roi_mask = saliency > threshold
if np.any(roi_mask):
    cols = np.any(roi_mask, axis=0)
    rows = np.any(roi_mask, axis=1)
    xmin, xmax = np.where(cols)[0][[0, -1]]
    ymin, ymax = np.where(rows)[0][[0, -1]]
    
    # Add visible padding
    xmin = max(0, xmin - 5)
    xmax = min(width, xmax + 5)
    ymin = max(0, ymin - 5)
    ymax = min(height, ymax + 5)
else:
    # Fallback to center
    ymin, ymax = height // 3, 2 * height // 3
    xmin, xmax = width // 3, 2 * width // 3

# Draw fine grid in ROI (step ~5% of image size)
fine_step_y = max(1, step_y // 4)
fine_step_x = max(1, step_x // 4)

# We want lines strictly inside the ROI box for specific x/y
# Draw horizontal lines in ROI
for y in range(ymin, ymax, fine_step_y):
    axes[2].hlines(y=y, xmin=xmin, xmax=xmax, color='red', linewidth=0.5, alpha=0.8)

# Draw vertical lines in ROI
for x in range(xmin, xmax, fine_step_x):
    axes[2].vlines(x=x, ymin=ymin, ymax=ymax, color='red', linewidth=0.5, alpha=0.8)

plt.tight_layout()
output_path = os.path.join(output_dir, 'Figure1_Motivation.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
print(f"Figure saved to {output_path}")
