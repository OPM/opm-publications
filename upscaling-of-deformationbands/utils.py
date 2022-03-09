# -*- coding: utf-8 -*-
"""
Module for calculating effective permeability of deformation bands. See the
paper

Berge et.al. "Impact of deformation bands on fault-related fluid flow in
field-scale simulations""

for details.

@author: Runar L. Berge
"""


import numpy as np


def band_density_params(W5):
    # Estimate band density:
    D5 = 13.33  # Averaged band density across the whole damage zone
    # Assuming D5 is independent of W5:
    L = 5 - D5
    A = D5 - L * (np.log(W5) - 1)
    return A, L, D5