# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 12:56:59 2022

@author: bergeru
"""

import numpy as np
import scipy.sparse as sps
import porepy as pp
import pandas
import os


def write_to_csv(out, path, name):
    header = "Kxx,Kyy,W5,D5,L,A,X,Y,band_length,a,sigma,Kf_aKm"
    if not out.shape[1] == len(header.split(",")):
        header = ""
    os.makedirs(path, exist_ok=True)
    np.savetxt(
        os.path.join(path, name),
        out,
        header=header,
        comments="",
        delimiter=",",
    )
    return 1


def set_unique_file_name(folder, name, file_extension=".csv"):
    i = 0
    while i < 1000:
        exists = os.path.isfile(folder + "/" + name + "_run_" + str(i) + file_extension)
        if not exists:
            return name + "_run_" + str(i)
        i += 1
    raise ValueError(
        "Could not set unique file name. Reached maximum value of unique names"
    )

def merge_csv(path, prefix):
    files = [f for f in os.listdir(path) if f[-4:] == ".csv"]
    data_frames = []
    for name_idx, f in enumerate(files):
        if not prefix in f:
            continue
        df_loc = pandas.read_csv(os.path.join(path, f))
        data_frames.append(df_loc)
    df = pandas.concat(data_frames, ignore_index=True)
    return df


def band_density_params(W5):
    # Estimate band density:
    D5 = 13.33  # Averaged band density across the whole damage zone
    # Assuming D5 is independent of W5:
    L = 5 - D5
    A = D5 - L * (np.log(W5) - 1)
    return A, L, D5


def upscale(g, data, disc, p):

    data_dict = data.get_data()
    flux = data_dict[pp.DISCRETIZATION_MATRICES][data.keyword][disc.flux_matrix_key]
    bound_flux = data_dict[pp.DISCRETIZATION_MATRICES][data.keyword][disc.bound_flux_matrix_key]
    p_bound = data_dict[pp.PARAMETERS][data.keyword]["bc_values"]

    q = flux * p + bound_flux * p_bound
#    q *= area

    p_in = p_bound[data_dict["inflow_faces"]].mean()
    p_out = p_bound[data_dict["outflow_faces"]].mean()
    
    delta_p = np.abs(p_in - p_out)

    fi, _, sgn = sps.find(g.cell_faces)
    inflow_faces = data_dict['inflow_faces'][fi]
    influx = -(q[fi] * sgn)[inflow_faces].sum()

    if data.params['flow_dir'] == 0:
        L = data.domain()["xmax"] - data.domain()["xmin"]
        H = data.domain()["ymax"] - data.domain()["ymin"]
    elif data.params['flow_dir'] == 1:
        H = data.domain()["xmax"] - data.domain()["xmin"]
        L = data.domain()["ymax"] - data.domain()["ymin"]
    else:
        raise ValueError('Invalid flow direction {}, must be 0, or 1'.format(data.params['flow_dir']))

    K = influx * L / delta_p / H
    return K