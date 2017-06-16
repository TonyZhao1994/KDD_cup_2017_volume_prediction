# -*- coding: utf-8 -*-
"""
Created on Thu May 11 19:12:51 2017

@author: Tony
"""

import math
from datetime import datetime,timedelta
import numpy as np
import pandas
import random

def extract_tg_dir(df_current, tg_id, direction):
    df_tg_dir = df_current[(df_current['tollgate_id']==tg_id) & (df_current['direction']==direction)].\
                reset_index().drop(['index'],axis=1)
    df_tg_dir_new = pandas.DataFrame({})
    for start_time in xrange(len(df_tg_dir)):
        if start_time == 0:
            pass_time0 =datetime.strptime('2016-09-18 23:40:00', "%Y-%m-%d %H:%M:%S")
        else:
            pass_time0 = datetime.strptime(df_tg_dir['time_start'][start_time-1], "%Y-%m-%d %H:%M:%S")
        pass_time1 = datetime.strptime(df_tg_dir['time_start'][start_time], "%Y-%m-%d %H:%M:%S")
        while True:
            if (pass_time1-pass_time0).seconds == 1200:
                insert = pandas.DataFrame([df_tg_dir.loc[start_time]])
                df_tg_dir_new = df_tg_dir_new.append(insert,ignore_index=True)
                break
            else:
                insert = pandas.DataFrame([df_tg_dir.loc[start_time]])
                pass_time0 = pass_time0 + timedelta(minutes=20)
                insert['time_start'] = str(pass_time0)
                insert['volume'] = 0
                insert['model0'] = 1
                insert['model1'] = 1
                insert['model2'] = 1
                insert['model3'] = 1
                insert['model4'] = 1
                insert['model5'] = 1
                insert['model6'] = 1
                insert['model7'] = 1
                insert['model0'] = 1
                insert['type0'] = 1
                insert['type1'] = 1
                insert['has_etc1'] = 1
                df_tg_dir_new = df_tg_dir_new.append(insert,ignore_index=True)
    return df_tg_dir_new

def update_vacancy_volume(df_tg_dir, df_fill):
    for i in xrange(len(df_tg_dir)):
        if df_tg_dir['volume'][i] == 0:
            temp = df_fill[(df_fill['tollgate_id'] == df_tg_dir['tollgate_id'][i])\
                                                   &(df_fill['direction'] == df_tg_dir['direction'][i])\
                                                   &(df_fill['time_start'] == df_tg_dir['time_start'][i])]['volume'].values[0]
            df_tg_dir.loc[i, ['volume']] = temp
            df_tg_dir.loc[i, ['model1']] = 0.9*temp
            df_tg_dir.loc[i, ['model2']] = 0.1*temp
            df_tg_dir.loc[i, ['type0']] = 0.8*temp
            df_tg_dir.loc[i, ['type1']] = 0.2*temp
            df_tg_dir.loc[i, ['has_etc1']] = 0.3*temp
    return df_tg_dir

def extract_test_tg_dir(df_current, tg_id, direction):
    df_tg_dir = df_current[(df_current['tollgate_id']==tg_id) & (df_current['direction']==direction)].\
                reset_index().drop(['index'],axis=1)
    return df_tg_dir

def add_last2h_dimension(df_tg_dir, key):
    lv=[0]*6
    lv[0] = []
    lv[1] = []
    lv[2] = []
    lv[3] = []
    lv[4] = []
    lv[5] = []
    lv_mean = []
    lv_var = []
    lv_max = []
    lv_min = []
    for i in xrange(len(df_tg_dir)-6):
        if i/6 == 0:
            lv[i%6].append(df_tg_dir[key][i])
            lv[i%6].append(df_tg_dir[key][i])
            lv[i%6].append(df_tg_dir[key][i])
            lv[i%6].append(df_tg_dir[key][i])
            lv[i%6].append(df_tg_dir[key][i])
            lv[i%6].append(df_tg_dir[key][i])
        j = 6
        p = 3
        if ((i%72 == 42) | (i%72 == 43) | (i%72 == 44) | (i%72 == 45) | (i%72 == 46) | (i%72 == 47)):
            while p!=0:
                lv[i%6].append(df_tg_dir[key][i])
                p = p - 1
            p = 3
            while p!=0:
                lv[i%6].append(df_tg_dir[key][i+3])
                p = p - 1
            p = 3
        elif ((i%72 == 48) | (i%72 == 49) | (i%72 == 50) | (i%72 == 51) | (i%72 == 52) | (i%72 == 53)):
            while p!=0:
                lv[i%6].append(df_tg_dir[key][i-3])
                p = p - 1
            p = 3
            while p!=0:
                lv[i%6].append(df_tg_dir[key][i])
                p = p - 1
            p = 3
        else:
            while j!=0:
                lv[i%6].append(df_tg_dir[key][i])
                j = j - 1
    for jj in xrange(len(df_tg_dir)):
        temp_list = np.array([lv[0][jj], lv[1][jj], lv[2][jj], lv[3][jj], lv[4][jj], lv[5][jj]])    
        lv_mean.append(temp_list.mean())
        lv_var.append(temp_list.var())
    df_tg_dir[key+'lv0'] = lv[0]
    df_tg_dir[key+'lv1'] = lv[1]
    df_tg_dir[key+'lv2'] = lv[2]
    df_tg_dir[key+'lv3'] = lv[3]
    df_tg_dir[key+'lv4'] = lv[4]
    df_tg_dir[key+'lv5'] = lv[5]
    df_tg_dir[key+'lv_mean'] = lv_mean
    df_tg_dir[key+'lv_var'] = lv_var
    return df_tg_dir

def add_last2h_test_dimension(df_tg_dir, key):
    lv_6_8 = [0]*6
    lv_15_17 = [0]*6
    lv_6_8[0] = []
    lv_6_8[1] = []
    lv_6_8[2] = []
    lv_6_8[3] = []
    lv_6_8[4] = []
    lv_6_8[5] = []
    lv_15_17[0] = []
    lv_15_17[1] = []
    lv_15_17[2] = []
    lv_15_17[3] = []
    lv_15_17[4] = []
    lv_15_17[5] = []
    for i in xrange(len(df_tg_dir)):
        if int(pandas.to_datetime(df_tg_dir['time_start'][i]).hour) < 12:
            lv_6_8[i%6].append(df_tg_dir[key][i])
        else:
            lv_15_17[i%6].append(df_tg_dir[key][i])
    return lv_6_8,lv_15_17

def add_time_dimension(df_input, df_timewindow):
    m_list=[]
    weekday_list=[]
    time_list=[]
    hour_list = []
    date_list = []
    for i in xrange(len(df_input)):
        start_time = datetime.strptime(df_timewindow[i], "%Y-%m-%d %H:%M:%S")
        m_list.append(start_time.month)
        hour_list.append(start_time.hour)
        date_list.append(start_time.day)
        if str(start_time.date()) == '2016-10-08':
            weekday_list.append(3)
        elif str(start_time.date()) == '2016-10-09':
            weekday_list.append(4)
        else:
            weekday_list.append(start_time.weekday())
        time_list.append(start_time.hour*3 + (start_time.minute/20))
    df_input['month'] = m_list
    df_input['weekday'] = weekday_list
    df_input['time'] = time_list
    df_input['hour'] = hour_list
    df_input['date'] = date_list
    return df_input

def transfer_volume(df_temp2):
    df_transfer = df_temp2.drop(['volume'],axis=1)
    df_transfer['volume'] = df_temp2['volume']
    return df_transfer

def holiday_judge(df_current, df_timewindow):
    judge_list=[]
    for i in xrange(len(df_current)): 
        start_time = datetime.strptime(df_timewindow[i], "%Y-%m-%d %H:%M:%S")
        if (start_time.month == 10) and ((start_time.day/8) == 0) and (df_current['direction'][i] == 0):
            judge_list.append(1)
        else:
            judge_list.append(0)
    df_current['holiday_ornot'] = judge_list
    return df_current

def holiday_judge_out(df_current, df_timewindow):
    judge_list=[]
    for i in xrange(len(df_current)): 
        start_time = datetime.strptime(df_timewindow[i], "%Y-%m-%d %H:%M:%S")
        if (start_time.month == 10) and ((start_time.day/4) == 0) and (df_current['direction'][i] == 0):
            judge_list.append(1)
        else:
            judge_list.append(0)
    df_current['holiday_ornot_out'] = judge_list
    return df_current

def holiday_judge_in(df_current, df_timewindow):
    judge_list=[]
    for i in xrange(len(df_current)): 
        start_time = datetime.strptime(df_timewindow[i], "%Y-%m-%d %H:%M:%S")
        if (start_time.month == 10) and ((start_time.day == 4) or (start_time.day == 5) or (start_time.day == 6)\
                                    or (start_time.day == 7)) and (df_current['direction'][i] == 1):
            judge_list.append(1)
        else:
            judge_list.append(0)
    df_current['holiday_ornot_in'] = judge_list
    return df_current

def insert_weather(df_current, df_timewindow, df_weather):
    pre_list = []
    wind_list = []
    tempra_list = []
    humidity_list = []
    a = df_timewindow.str.split(' ',expand=True)[0]
    b = df_timewindow.str.split(' ',expand=True)[1]
    c = b.str.split(':',expand=True)[0]
    for i in xrange(len(df_current)):
        date = a[i]
        hour = c[i]
        temp0 = df_weather[(df_weather['date']==date) & (df_weather['hour']==(int(hour)/3)*3)]['precipitation']
        temp1 = df_weather[(df_weather['date']==date) & (df_weather['hour']==(int(hour)/3)*3)]['wind_speed']
        temp2 = df_weather[(df_weather['date']==date) & (df_weather['hour']==(int(hour)/3)*3)]['temperature']
        temp3 = df_weather[(df_weather['date']==date) & (df_weather['hour']==(int(hour)/3)*3)]['rel_humidity']
        '''
        if len(temp0) == 0:
            temp0 = 0
        if len(temp1) == 0:
            temp1 = 0
        if len(temp2) == 0:
            temp2 = 0
        if len(temp3) == 0:
            temp3 = 0
        '''
        if ((float(temp0) > 0) and (float(temp0) < 2.5)):
            temp0 = 1
        elif float(temp0) >= 2.5:
            temp0 = 2
        if (float(temp1) <= 0.4):
            temp1 = 0
        elif ((float(temp1) > 0.4) and (float(temp1) <= 1.5)):
            temp1 = 1
        elif ((float(temp1) > 1.5) and (float(temp1) <= 5)):
            temp1 = 2
        elif (float(temp1) > 5):
            temp1 =3
        pre_list.append(float(temp0)) 
        wind_list.append(float(temp1))
        tempra_list.append(float(temp2))
        humidity_list.append(float(temp3))
    df_current['precipitation'] = pre_list
    df_current['wind_speed'] = wind_list
    df_current['temperature'] = tempra_list
    df_current['humidity'] = humidity_list
    return df_current

def insert_onehot(df, key):
    df_temp = pandas.get_dummies(df[key]) 
    length = df_temp.shape[1]
    df_temp.columns=[i for i in xrange(length)]
    for i in xrange(length):
        df.insert(0, key+'%d'%i, df_temp[i])
    return df
