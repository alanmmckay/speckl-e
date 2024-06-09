import trimesh
import numpy as np
import requests
import tempfile
import os
import subprocess

def estimate_scale_factor(model, target_size='medium'):
    """
    Estimates the scaling factor based on the target size.
    """
    size_mapping = {
        'small': 50.0,
        'medium': 100.0,
        'large': 150.0
    }
    bounding_box = model.bounding_box.extents
    current_max_dimension = np.max(bounding_box)
    target_dimension = size_mapping.get(target_size, 100.0)
    return target_dimension / current_max_dimension

def scale_model(input_obj_path, output_obj_path, target_size='medium'):
    """
    Scales the 3D model to the desired size.
    """
    model = trimesh.load(input_obj_path)
    scale_factor = estimate_scale_factor(model, target_size)
    model.apply_scale(scale_factor)
    model.export(output_obj_path)
    print(f"Model scaled to {target_size} size and saved to {output_obj_path}")

def scale_filament_length(filament_length, scale_factor, target_size):
    """
    Scales the filament length based on the target size and scale factor.
    """
    size_mapping = {
        'small': 50.0,
        'medium': 100.0,
        'large': 150.0
    }
    target_multiplier = size_mapping.get(target_size, 1.0)
    return filament_length * scale_factor * target_multiplier

