# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 13:59:49 2022

@author: bergeru
"""

import numpy as np
import utils
import scipy.integrate as integrate




def effective_permeability_layered(rho_x, Kb_aKm, band_length, sigma):
    """
    Calculate the effective permeability using a layered model.

    Parameters
    ----------
    rho_x : float or array
        Density of deformation bands along a scanline in x-direction
    Kb_aKm : float
        Scaled permeability ratio between deformation bands and host rock.
    band_length : float or array
        Length of deformation bands.
    sigma : TYPE
        Standard deviation of deformation band rotation.

    Returns
    -------
    Kx : float or array
        Effective permeability in x-direction.
    Ky : float or array
        Effective permeability in y-direction.

    """
    rho_x = np.asarray(rho_x)
    # Avoid dividing by 0 (rho=0 just gives us rock matrix permeability)
    rho_x[rho_x<1e-8] = -1
    # The expected value of the rotation
    theta = sigma * np.sqrt(2) / np.sqrt(np.pi)
    rho_y = rho_x * np.sin(theta) / np.cos(theta)
    rho = rho_x / (np.cos(theta) * band_length)

    # Chain length:
    Axb, Ayb = chain_length(rho, band_length, sigma)
    Axm = 1 / rho_x
    Aym = 1 / rho_y

    cast = np.isinf(Ayb)
    Axb[cast] = 1
    Ayb[cast] = 1
    Axm[cast] = 0
    Aym[cast] = 0
    # permeability x-direction
    Y = Axb + Axm
    Kf = 1 / (1 + Kb_aKm**-1 * rho_x)
    Kx = (Kf * Axb + Axm) / Y

    # permeability y-direction
    
    X = Ayb + Aym
    Kf = 1 / (1 + Kb_aKm**-1 * rho_y * np.sin(theta))

    Ky = (Kf * Ayb + Aym) / X

    # if density is negative use rock matrix permeability
    Kx[rho_x < 0] = 1
    Ky[rho_x < 0] = 1
    return Kx, Ky


def effective_permeability_harmonic(rho_x, Kb_aKm, sigma):
    """
    Calculate the effective permeability using a layered model.

    Parameters
    ----------
    rho_x : float or array
        Density of deformation bands along a scanline in x-direction
    Kb_aKm : float
        Scaled permeability ratio between deformation bands and host rock.
    sigma : TYPE
        Standard deviation of deformation band rotation.

    Returns
    -------
    Kx : float or array
        Effective permeability in x-direction.
    Ky : float or array
        Effective permeability in y-direction.

    """
    theta = sigma * np.sqrt(2) / np.sqrt(np.pi)
    Kxh = 1 / (1 + Kb_aKm**-1 * rho_x)
    Kyh = 1 / (1 + Kb_aKm**-1 * rho_x * np.sin(theta) / np.cos(theta))
    return Kxh, Kyh


def damage_zone_permeability(throw=None, W5=None, Kb_aKm=1e-1, band_length=2, sigma=np.pi/12, nbins=100):
    """
    Calculate the effective permeability over the whole damage zone using the
    layered model
    """
    if W5 is None and (not throw is None):
        W5 = damage_zone_width(throw)
    elif throw is None and (not W5 is None):
        pass
    else:
        raise ValueError("You must set either throw OR W5")
    # Damage zone width:
    A, L, _ = utils.band_density_params(W5)
    X = np.exp(-A / L)
    # Integrate the permeability over the damage zone:
    # discretize segment
    x = np.linspace(0, X, nbins)
    # use midtpoint (mostly to avoid infinite value at 0)
    x = (x[:-1] + x[1:]) / 2
    dx = np.diff(x)
    assert np.allclose(dx, dx[0])
    dx = dx[0]
    segment_length = X - 0
    # Calculate pointwise perm
    rho_x = A + L * np.log(x)
    Kxp, Kyp = effective_permeability_layered(rho_x, Kb_aKm, band_length, sigma)
    # Harmonic average in x-direction
    Kx = segment_length / np.sum(dx / Kxp)

    # Arithmetic average in y-direction
    Ky = np.mean(Kyp)
    
    return Kx, Ky


def damage_zone_width(throw):
    # Estimate damage zone width from throw. Average value from Schueller (2013), Fig 6
    return 1.74 * throw ** 0.43

def damage_zone_width_full(throw):
    # Estimate damage zone width from throw. Average value from Schueller (2013), Fig 6
    W5 = damage_zone_width(throw)
    A, L, _ = utils.band_density_params(W5)
    return np.exp(-A / L)


def chain_length(rho, band_length, sigma):
    theta = sigma * np.sqrt(2) / np.sqrt(np.pi)
    p_cross = probability_cross_normal(rho, band_length, sigma)
    Ecross = p_cross / (1 - p_cross)**2
    # Expected lenght of chain in x- and y-direction
    Ayb = np.sin(theta) * band_length + np.sqrt(0.5 * np.sin(theta) * band_length * Ecross)
    Axb = np.cos(theta) * band_length + np.sqrt(0.5 * np.cos(theta) * band_length * Ecross)
    return Axb, Ayb


def expected_number_of_crossings(rho_x, band_length, theta):
    # # probability that a segment contains a crossing:
    sigma = theta * np.sqrt(np.pi) / np.sqrt(2)
    p_cross = probability_cross_normal(rho_x / (band_length * np.cos(theta)), band_length, sigma)
    mus = -np.log(1 - p_cross)
    return mus


def probability_no_cross_normal(rho, band_length, sigma):
    def f(x, y, sigma):
        weight = np.abs(np.sin(x-y)) / (sigma**2 * 2 * np.pi)
        e0 = np.exp(-0.5 * (x / sigma)**2)
        e1 = np.exp(-0.5 * (y / sigma)**2)
        return weight * e0 * e1

    p, err = integrate.dblquad(f, -np.inf, np.inf, lambda x: -np.inf, lambda x: np.inf, [sigma])
    return np.exp(-band_length**2 * p * rho)


def probability_cross_normal(rho, band_length, sigma):
    return 1 - probability_no_cross_normal(rho, band_length, sigma)


def probability_cross_uniform(rho, band_length, theta=0):
    return 1 - np.exp(-band_length**2 * 2 / np.pi * rho)


if __name__ == "__main__":
    print(damage_zone_permeability(500, None, 0.1))
    print(damage_zone_width_full(500))
    
