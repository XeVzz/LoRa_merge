# -*- coding: utf-8 -*-
"""
@author: Min Lun Wu
"""
from pathlib import Path
import numpy as np
import pandas as pd
import os
import dateutil.parser
from datetime import datetime, timedelta
from relat_pos import cac_dis_ang
from matplotlib import pyplot as plt
from check_launch import launch_check

#%% data path
dpath='./LoRa/'
opath='./no_file/'
Path(opath).mkdir(exist_ok= True)

files = [_ for _ in os.listdir(dpath) if "LoRa" in _ and _.endswith(".csv")]
LoRa_data=pd.DataFrame()
clm=['Time','tmp1','PacketID','T','RH','P','Volt','Lon','Lat','Height','sat','rssi','tmp2','channel','speed','SNR','dir','stid']

#%% all merge
print ("Merge all LoRa data...")

for i in range(len(files)) :
    LoRa_file=open(dpath+files[i],'r',encoding="utf-8")
    err_val=['cvf','NA','inf']
    tmp=pd.read_csv(LoRa_file,names=clm,na_values=err_val)
    LoRa_data=pd.concat([LoRa_data,tmp]).drop_duplicates().reset_index(drop=True)
    LoRa_file.close()  

# show progress
    prog=(i+1)/len(files)
    print('\r'+'['+'='*int(prog*75)+'>'+'-'*(75-int(prog*75))+'] '+str('%d%%'%(prog*100)),end='',flush=True)
    if prog==1:
        print('\r'+'['+'='*int(prog*75)+'>'+'-'*(75-int(prog*75))+'] '+'DONE!!',end='')
        print('')

#ST_id_list=np.unique(LoRa_data['stid'].astype('int64'))
ST_id_list=np.unique(LoRa_data['stid'])
ST_id_list=ST_id_list[~np.isnan(ST_id_list)]

print ("")
print ("Found","< %s >" %str(len(ST_id_list)),"ST number, ready to output.")
print ("")

#%%
print ("================ start output =================")
vdc=0
for ST_id in ST_id_list :
    ST_id=int(ST_id)
    id_split=LoRa_data.query('stid == @ST_id').index.tolist()    
    nu_data=LoRa_data.iloc[id_split].sort_values(by='Time').drop_duplicates(subset ="Time").reset_index(drop=True)

    if len(nu_data) < 20:
        print ("Storm Tracker NO: " + '%-6s' %ST_id +"Data Length: "+'%-6s' %str(len(nu_data))+"(Data too few, skip output)")
        continue

    time=nu_data['Time'].apply(lambda x: dateutil.parser.parse(x)+timedelta(hours=8))
    time_op=time.apply(lambda x :x.strftime("%Y/%m/%d %H:%M:%S.%f"))
    channel=nu_data['channel']
    PacketID=nu_data['PacketID']
    T=nu_data['T'].astype(float)/100.
    RH=nu_data['RH'].astype(float)/10.
    P=nu_data['P'].astype(float)/100.
    Volt=nu_data['Volt'].astype(float)/1023*1.1*2.
    rssi=nu_data['rssi'].astype(float)/100.
    lat=nu_data['Lat'].astype(float)/100000.
    lon=nu_data['Lon'].astype(float)/100000.
    h=nu_data['Height'].astype(float)/100.
    sat=nu_data['sat']
    SNR=nu_data['SNR'].astype(float)/100.
    speed=nu_data['speed'].astype(float)/100.
    direction=nu_data['dir'].astype(float)/100.

    first_P=launch_check(P,10,800)

    # if abs(P[first_P] - min(P)) < 100:
    if first_P < 0:
        print ("Storm Tracker NO: "+'%-6s' %ST_id +"Data Length: "+'%-6s' % str(len(nu_data))+"(no launching record)")
        continue

    vdc=vdc+1
    lat_ref, lon_ref, alt_ref = lat[first_P], lon[first_P], h[first_P]
    ftime=time[first_P]

    dis,ang = cac_dis_ang(lat_ref, lon_ref, alt_ref, lat, lon, h)

    nu_op_data=pd.concat([time_op,channel,PacketID,T,RH,P,Volt,rssi,lat,lon,h,dis,sat,SNR,speed,direction,ang],axis=1).reset_index(drop=True)
    nu_op_data.columns=['Time','channel','PacketID','Temperature(degree C)','Humidity(%)','Pressure(hPa)','Voltage(V)','RSSI','Lat','Lon','Height(m)','Distance(km)','Sat','SNR','Speed(km/hr)','Direction(degree)','angle(degree)']

    launch_time=time[first_P].strftime("%Y/%m/%d %H:%M:%S")
    print ("Storm Tracker NO: " +'%-6s' %ST_id+"Data Length: "+'%-6s' %str(len(nu_data))+"-->launch at: "+launch_time+" (#%s)" %str(first_P))


    fname='no_'+str(ST_id)+'_'+ftime.strftime("%Y%m%d%H")+'.csv'
    nu_op_data.to_csv(opath+fname,index=False)

print ("================ DONE!! =================")
print ("")
print ("Got","< %s >" %str(vdc),"valid ST_no file output.")

