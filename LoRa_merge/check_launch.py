# -*- coding: utf-8 -*-
"""
@author: Min Lun Wu
"""
import numpy as np

# %%
def launch_check(P,check_nu=10,P_above=900):
    # P=P[P>990]
    first_P=-1
    output_condition = (len(P)>check_nu+10) & (max(P)>P_above) & ((max(P)-min(P))>300)
    
    if output_condition :
        for num in range(len(P)-(check_nu+1)):
            if P[num]>P_above:
                down_P=0
                for af in range(0,check_nu):
                    if P[num+af] > P[num+af+1]:
                        down_P=down_P+1
                        if down_P>=int(check_nu):
                            first_P=num
                            break
                if first_P != -1:
                    break
                
        if first_P == -1:
            P_max_check=max(P)-1
            P_to_ground=abs(P-np.mean(P[P>=P_max_check])).values.astype(int)
            first_P=np.where(P_to_ground>1)[0][1]

    return first_P

