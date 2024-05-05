# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 17:57:00 2023

@author: rajul
"""
import time

starting_time = time.time()
import pandas as pd
import numpy as np

from datetime import date, timedelta
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
merge_coordinates = pd.read_csv('D:/India_lat_lon_pr.csv')       
# merge_coordinates = pd.read_csv('D:/India_lat_lon_4600.csv')
f_lat = merge_coordinates['N']
f_lon = merge_coordinates['E']

path = r'E:/MTP/Bias correction/Raw EC_Earth3/Corrected_bias_corrected_data/pr_new_corrected_infinite'
# r'E:\MTP\Bias correction\Raw EC_Earth3\Corrected_bias_corrected_data\pr_uncorrected_infinite_values_'
# path = r'D:/Bias_corrected_data'

save_path = r'E:/MTP/Bias correction/Raw EC_Earth3/Corrected_bias_corrected_data'
# save_path = r'E:/MTP/Bias correction/Raw EC_Earth3/Corrected_bias_corrected_data'
# for var in ['tasmax','tasmin']:
for var in ['pr']:
    for scenario in ['ssp126','ssp245', 'ssp370', 'ssp585']: 

        data  = pd.read_csv(f'{path}/{var}/{scenario}/{var}_{scenario}_2015_2044_corrected_2.csv', header = None)  
        data.drop(0,axis = 0,inplace = True)
        data.drop(1,axis = 0,inplace = True)
        data['Date'] = [date for date in daterange(date(2015,1,1),date(2045,1,1))]
        # data.rename(columns= {0 :'Date'}, inplace = True)
        data.set_index('Date',inplace = True)
        
        
        # data[data>=70] = np.nan
        # data[data<-40] = np.nan
        data[data>=350] = np.nan
        data[data<0] = np.nan
        print(data.isnull().values.sum())
        
        data.fillna(method = 'ffill',inplace = True)
        data.fillna(method = 'bfill',inplace = True)
        data.columns = [i for i in range(4964)]
        
        df = pd.DataFrame(columns = [i for i in range(4964)])
        df.loc['N'] = f_lat
        df.loc['E'] = f_lon
        df.columns = [i for i in range(4964)]
        df = df.append(data)
        
        df.to_csv(f'{save_path}/{var}/{scenario}/{var}_{scenario}_2015_2044.csv', header = None)
        df = pd.DataFrame()
        
        data  = pd.read_csv(f'{path}/{var}/{scenario}/{var}_{scenario}_2045_2074_corrected_2.csv', header = None)   
        # data.set_index(0,inplace = True)
        data.drop(0,axis = 0,inplace = True)
        data.drop(1,axis = 0,inplace = True)
        # data.rename(columns= {0 :'Date'}, inplace = True)
        data['Date'] = [date for date in daterange(date(2045,1,1),date(2075,1,1))]
        data.set_index('Date',inplace = True)
        # data[data>=70] = np.nan
        # data[data<-40] = np.nan
        data[data>=350] = np.nan
        data[data<0] = np.nan
        print(data.isnull().values.sum())
        
        data.fillna(method = 'ffill',inplace = True)
        data.fillna(method = 'bfill',inplace = True)
        # print(data.isnull().values.sum())
        data.columns = [i for i in range(4964)]
        
        df = pd.DataFrame(columns = [i for i in range(4964)])
        df.loc['N'] = f_lat
        df.loc['E'] = f_lon
        df.columns = [i for i in range(4964)]
        df = df.append(data)
        
        df.to_csv(f'{save_path}/{var}/{scenario}/{var}_{scenario}_2045_2074.csv', header = None)
        df = pd.DataFrame()
        
        
        data  = pd.read_csv(f'{path}/{var}/{scenario}/{var}_{scenario}_2071_2100_corrected_2.csv', header = None)   
        # data.set_index(0,inplace = True)
        data.drop(0,axis = 0,inplace = True)
        data.drop(1,axis = 0,inplace = True)
        data['Date'] = [date for date in daterange(date(2071,1,1),date(2101,1,1))]
        # data.rename(columns= {0 :'Date'}, inplace = True)
        data.set_index('Date',inplace = True)
        # data[data>=70] = np.nan
        # data[data<-40] = np.nan
        data[data>=350] = np.nan
        data[data<0] = np.nan
        print(data.isnull().values.sum())
        
        data.fillna(method = 'ffill',inplace = True)
        data.fillna(method = 'bfill',inplace = True)
        # print(data.isnull().values.sum())
        
        data.columns = [i for i in range(4964)]
        
        df = pd.DataFrame(columns = [i for i in range(4964)])
        df.loc['N'] = f_lat
        df.loc['E'] = f_lon
        df.columns = [i for i in range(4964)]
        df = df.append(data)
        
        df.to_csv(f'{save_path}/{var}/{scenario}/{var}_{scenario}_2071_2100.csv', header = None)
        df = pd.DataFrame()
# print('This should be last line compiled')
# quit()
# print('fuck')
# year = [(1850,1879),(1865,1894),(1895,1924),(1925,1954),(1955,1984),(1985,2014)]
year = [(1985,2014)]
# for var in ['tasmax','tasmin']:
for var in ['pr']:
    for scenario in ['Historical']:       
        for i in range(len(year)):
            data  = pd.read_csv(f'{path}/{var}/{scenario}/{var}_{scenario}_{year[i][0]}_{year[i][1]}_corrected_2.csv', header = None)
            # data.set_index(0,inplace = True)
            data.drop(0,axis = 0,inplace = True)
            data.drop(1,axis = 0,inplace = True)
            data['Date'] = [date for date in daterange(date(int(f'{year[i][0]}'),1,1),date(int(f'{year[i][1]}')+1,1,1))]
            # data.rename(columns= {0 :'Date'}, inplace = True)
            data.set_index('Date',inplace = True)
            # data[data>=70] = np.nan
            # data[data<-40] = np.nan
            data[data>=350] = np.nan
            data[data<0] = np.nan
            print(data.isnull().values.sum())
            
            data.fillna(method = 'ffill',inplace = True)
            data.fillna(method = 'bfill',inplace = True)
            # print(data.isnull().values.sum())
            
            data.columns = [i for i in range(4964)]
        
            df = pd.DataFrame(columns = [i for i in range(4964)])
            df.loc['N'] = f_lat
            df.loc['E'] = f_lon
            df.columns = [i for i in range(4964)]
            df = df.append(data)
        
            df.to_csv(f'{save_path}/{var}/{scenario}/{var}_{scenario}_{year[i][0]}_{year[i][1]}.csv', header = None)
            df = pd.DataFrame()
            # data  = pd.read_csv(f'{path}/{var}/{scenario}/{var}_{scenario}_{year[i][0]}_{year[i][1]}.csv', header = None)

end_time = time.time()
print('Total time taken in minutes:', (end_time- starting_time)/60)
