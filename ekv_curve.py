#! /usr/bin/env python3

import plotly.graph_objects as go
import pandas as pd 
import math as m
import numpy as np
import ies
import sys


if __name__ == '__main__':
    fid = open(sys.argv[1] , encoding='cp1251')
    ies_data = ies.reader(fid)
    LID = pd.DataFrame(ies_data['I_TABLE'])
    LID[360] = LID[0]
    
    C = LID.keys()
    I = LID.values
    maxidx = np.where(I==I.max())
    Imax = I[maxidx[0][0],:]
    fig = go.Figure(data= go.Scatterpolar(r = Imax, theta = C))
    fig.update_layout(showlegend=False,template="plotly_dark")

    fig.show()
