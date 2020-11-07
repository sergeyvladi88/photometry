#! /usr/bin/env python3

import plotly.graph_objects as go
import pandas as pd 
import math as m
import numpy as np
import ies
import sys

def spher2cartesianC(I, polar_angles, azimut_angles):
    x = I * np.sin(polar_angles) * np.cos(azimut_angles)
    y = I * np.sin(polar_angles) * np.sin(azimut_angles)
    z = - I * np.cos(polar_angles)
    return x, y, z


if __name__ == '__main__':
    fid = open(sys.argv[1] , encoding='cp1251')
    ies_data = ies.reader(fid)
    LID = pd.DataFrame(ies_data['I_TABLE'])

    C = [m.radians(float(i)) for i in LID.columns]
    C = np.array(C)

    gamma = np.array(np.radians(LID.index))
    I = LID.values

    gamma_grid, C_grid = np.meshgrid(gamma, C)
    X, Y, Z = spher2cartesianC(I.T,gamma_grid, C_grid)


    fig = go.Figure(data=go.Surface(x=X, y=Y, z=Z,showscale=False))
    fig.update_layout(title='Фотометрическое тело', autosize=False,
                      width=600, height=600,
                      margin=dict(l=65, r=50, b=65, t=90))

    fig.show()
