# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 23:45:58 2023

@author: rajul
"""

# import numpy as np
import pandas as pd
import time

starting_time = time.time()

path = r'E:\MTP\Bias correction/Bias_Corrected_EC_Earth3/Raw_Splitted_Files/Raw_Splitted_Files'
writer  = pd.ExcelWriter(f'{path}/Change_Analysis_all_variable.xlsx', engine = 'xlsxwriter')
workbook = writer.book

for var in ['pr','tasmax','tasmin']:
    # if var == 'tasmax':
    df = pd.read_csv(f'{path}/{var}/Historical/{var}_Historical_1985_2014.csv',header = None)
    
    # elif var == 'tasmin':
    #     df = pd.read_csv('E:\MTP\Bias correction\IMD_Tmin_1985_2014.csv',header = None)
    
    # else:
    #     df = pd.read_csv('E:\MTP\Bias correction\IMD_pr_1985_2014.csv',header = None)
        
    
    df = df.T
    df.drop(0, axis = 1,inplace = True)
    df.drop(1,axis = 1,inplace = True)
    df.drop(0,axis = 0,inplace = True)
    from datetime import date, timedelta
    def daterange(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)
    
    
    # value1 = datetime.date(1976,1,1)
    # dat1   = [date for date in daterange(date(1985,1,1),date(2015,1,1))]
    df.columns = [date for date in daterange(date(1985,1,1),date(2015,1,1))]
    
    df = df.mean()
    df = df.rename_axis('Date').reset_index()
    df.Date = pd.to_datetime(df.Date)
    
    if var != 'pr': Yearly_mean = df.resample('Y', on= 'Date').mean()
    else: Yearly_mean = df.resample('Y', on= 'Date').sum()
    
    Historical_mean = Yearly_mean.mean()
    Historical_mean = Historical_mean[0]
    df = pd.DataFrame()
    
    Final_df = pd.DataFrame()
    Final_df['Scenarios'] = ['Base Period' , '2015-2044' , '2045-2074', '2071-2100']
    Final_df.set_index('Scenarios', inplace = True)
    
    Final_df['ssp126'] = [0.0 , 0.0 , 0.0, 0.0]
    Final_df['ssp245'] = [0.0 for i in range(4)]
    Final_df['ssp370'] = [0.0 for i in range(4)]
    Final_df['ssp585'] = [0.0 for i in range(4)]
    
    Final_df['ssp126']['Base Period'] = Historical_mean
    
    
    

    for scenario in ['ssp126', 'ssp245','ssp370','ssp585']: 
        data  = pd.read_csv(f'{path}/{var}/{scenario}/{var}_{scenario}_2015_2044.csv', header = None)
        df = data.T
        data = pd.DataFrame()
        df.drop(0, axis = 1,inplace = True)
        df.drop(1,axis = 1,inplace = True)
        df.drop(0,axis = 0,inplace = True)
        # from datetime import date, timedelta
        # def daterange(start_date, end_date):
        #     for n in range(int((end_date - start_date).days)):
        #         yield start_date + timedelta(n)
        
        
        # value1 = datetime.date(1976,1,1)
        # dat1   = [date for date in daterange(date(1985,1,1),date(2015,1,1))]
        df.columns = [date for date in daterange(date(2015,1,1),date(2045,1,1))]
        
        df = df.mean()
        df = df.rename_axis('Date').reset_index()
        df.Date = pd.to_datetime(df.Date)
        
        if var != 'pr': Yearly_mean = df.resample('Y', on= 'Date').mean()
        else: Yearly_mean = df.resample('Y', on= 'Date').sum()
        
        # Yearly_mean = df.resample('Y', on= 'Date').mean()
        Historical_mean = Yearly_mean.mean()
        Historical_mean = Historical_mean[0]
        Final_df[f'{scenario}']['2015-2044'] = Historical_mean
        
        
        
        data  = pd.read_csv(f'{path}/{var}/{scenario}/{var}_{scenario}_2045_2074.csv', header = None)
        df = data.T
        data = pd.DataFrame()
        df.drop(0, axis = 1,inplace = True)
        df.drop(1,axis = 1,inplace = True)
        df.drop(0,axis = 0,inplace = True)
        # from datetime import date, timedelta
        # def daterange(start_date, end_date):
        #     for n in range(int((end_date - start_date).days)):
        #         yield start_date + timedelta(n)
        
        
        # value1 = datetime.date(1976,1,1)
        # dat1   = [date for date in daterange(date(1985,1,1),date(2015,1,1))]
        df.columns = [date for date in daterange(date(2045,1,1),date(2075,1,1))]
        
        df = df.mean()
        df = df.rename_axis('Date').reset_index()
        df.Date = pd.to_datetime(df.Date)
        
        if var != 'pr': Yearly_mean = df.resample('Y', on= 'Date').mean()
        else: Yearly_mean = df.resample('Y', on= 'Date').sum()
        
        # Yearly_mean = df.resample('Y', on= 'Date').mean()
        Historical_mean = Yearly_mean.mean()
        Historical_mean = Historical_mean[0]
        Final_df[f'{scenario}']['2045-2074'] = Historical_mean
        
        
        data  = pd.read_csv(f'{path}/{var}/{scenario}/{var}_{scenario}_2071_2100.csv', header = None)
        df = data.T
        data = pd.DataFrame()
        df.drop(0, axis = 1,inplace = True)
        df.drop(1,axis = 1,inplace = True)
        df.drop(0,axis = 0,inplace = True)
        # from datetime import date, timedelta
        # def daterange(start_date, end_date):
        #     for n in range(int((end_date - start_date).days)):
        #         yield start_date + timedelta(n)
        
        
        # value1 = datetime.date(1976,1,1)
        # dat1   = [date for date in daterange(date(1985,1,1),date(2015,1,1))]
        df.columns = [date for date in daterange(date(2071,1,1),date(2101,1,1))]
        
        df = df.mean()
        df = df.rename_axis('Date').reset_index()
        df.Date = pd.to_datetime(df.Date)
        
        
        if var != 'pr': Yearly_mean = df.resample('Y', on= 'Date').mean()
        else: Yearly_mean = df.resample('Y', on= 'Date').sum()
        
        
        # Yearly_mean = df.resample('Y', on= 'Date').mean()
        Historical_mean = Yearly_mean.mean()
        Historical_mean = Historical_mean[0]
        Final_df[f'{scenario}']['2071-2100'] = Historical_mean
    
    df = pd.DataFrame()
    Change = pd.DataFrame()
    
    Change['Period'] =  ['2015-2044','2045-2074', '2071-2100']
    Change.set_index('Period', inplace = True)
    
    Change['ssp126'] = [0.0, 0.0, 0.0]
    Change['ssp245'] = [0.0, 0.0, 0.0]
    Change['ssp370'] = [0.0, 0.0, 0.0]
    Change['ssp585'] = [0.0, 0.0, 0.0]
    
    for ssp in ['ssp126', 'ssp245', 'ssp370' , 'ssp585']:
        Change[ssp]['2015-2044'] =  Final_df[ssp]['2015-2044'] - Final_df['ssp126']['Base Period']
        
        Change[ssp]['2045-2074'] =  Final_df[ssp]['2045-2074'] - Final_df['ssp126']['Base Period']
        Change[ssp]['2071-2100'] =  Final_df[ssp]['2071-2100'] - Final_df['ssp126']['Base Period']
        
        
    Percentage = pd.DataFrame()
    Percentage['Period'] =  ['2015-2044','2045-2074', '2071-2100']
    Percentage.set_index('Period', inplace = True)
    
    Percentage['ssp126'] = [0.0, 0.0, 0.0]
    Percentage['ssp245'] = [0.0, 0.0, 0.0]
    Percentage['ssp370'] = [0.0, 0.0, 0.0]
    Percentage['ssp585'] = [0.0, 0.0, 0.0]
    
    for ssp in ['ssp126', 'ssp245', 'ssp370' , 'ssp585']:
        Percentage[ssp]['2015-2044'] =  Change[ssp]['2015-2044']*100/Final_df['ssp126']['Base Period']
        
        Percentage[ssp]['2045-2074'] =  Change[ssp]['2045-2074']*100/Final_df['ssp126']['Base Period']
        
        Percentage[ssp]['2071-2100'] =  Change[ssp]['2071-2100']*100/Final_df['ssp126']['Base Period']
        
    
    
    Final_df.to_excel(writer,sheet_name = f'{var}',startrow=0, startcol = 0)
    Change.to_excel(writer,sheet_name = f'{var}',startrow=7, startcol = 0,header = None)
    Percentage.to_excel(writer,sheet_name = f'{var}',startrow=11, startcol = 0,header = None)

print('Time taken for processing in mins:', (time.time() - starting_time)/60)
writer.save()
writer.close()
# print('Time taken for processing in mins:',(time.time() - starting_time)/60)