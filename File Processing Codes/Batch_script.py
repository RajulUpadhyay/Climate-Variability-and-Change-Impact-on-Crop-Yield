# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 02:45:30 2023

@author: rajul
"""

# import os     
import pandas as pd
import subprocess

import time
start_time = time.time()

District_Name=['Balod','Baloda','Balrampur','Bametara','Bastar','Bijapur','Bilaspur','DakshinBastar','Dhamtari','Durg','Gariaband','Janjgir','Jashpur','Kabeerdham','Kondagaon','Korba','Koriya','Mahasamund','Mungeli','Narayanpur','Raigarh','Raipur','Rajnandgaon','Sukma','Surajpur','Surguja','Uttarbastar']
d_coordinates = r'E:\MTP\New_District_coordinates'

write_path = 'E:\MTP\DSSAT\Batch_Files'

for district in range(len(District_Name)):
    # print(District_Name[district])
    d_corr = pd.read_csv(f'{d_coordinates}/{District_Name[district]}.csv')
    rows,cols = d_corr.shape
    
    for row in range(rows):
    
        E , N = d_corr.loc[row][0],d_corr.loc[row][1]
        if E == 81.5 and N == 21.25:
            continue
        
        for ssp in ['Historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585']:
  
            if ssp == 'Historical': 
                scenarios = ['Historical']
            else: 
                scenarios = ['near_future', 'far_future']
            
            for scenario in scenarios:
    
                directory = f'{write_path}\{District_Name[district]}\{row}\{ssp}'
                
                if scenario == 'near_future': 
                    directory =f'{write_path}\{District_Name[district]}\{row}\{ssp}\{scenario}'

                    
                elif scenario == 'far_future': 
                    directory =f'{write_path}\{District_Name[district]}\{row}\{ssp}\{scenario}'
                   
                else: 
                    pass
                    
                p = subprocess.Popen('C:DSSAT48\DSCSM048.EXE CSCER048 B DSSBatch.v48', cwd=directory)
                p.wait()


quit_time = time.time()
print('Time taken to quit:', (quit_time - start_time)/60)
# obs = pd.read_excel('E:\MTP\Research Papers/Chhattisgarh.xlsx',sheet_name='Wheat')
# obs_data = obs.loc[318:331]['Yield (Tonnes/Hectare)']
# obs_data = obs_data*1000
# data_H = pd.DataFrame()
# Historical = pd.DataFrame()

# import warnings
# warnings.filterwarnings("ignore")

# District_Name=['Raipur']
# d_coordinates = r'E:\MTP\New_District_coordinates'

# write_path = 'E:\MTP\DSSAT\Batch_Files'
# error = []
# for district in range(len(District_Name)):
#     d_corr = pd.read_csv(f'{d_coordinates}/{District_Name[district]}.csv')
#     rows,cols = d_corr.shape
    
#     for row in range(rows):
    
#         E , N = d_corr.loc[row][0],d_corr.loc[row][1]
#         if E == 81.5 and N == 21.25:
#             continue
        
#         for ssp in ['Historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585']:
  
#             if ssp == 'Historical': 
#                 scenarios = ['Historical']
#             else: 
#                 scenarios = ['near_future', 'far_future']
            
#             for scenario in scenarios:
    
#                 directory = f'{write_path}\{District_Name[district]}\{row}\{ssp}'
                
#                 if scenario == 'near_future': 
#                     directory =f'{write_path}\{District_Name[district]}\{row}\{ssp}\{scenario}'

                    
#                 elif scenario == 'far_future': 
#                     directory =f'{write_path}\{District_Name[district]}\{row}\{ssp}\{scenario}'
                   
#                 else: 
#                     pass

#                 try: file = pd.read_fwf(f'{directory}/Plantsum.OUT',skiprows = 3)
#                 except:
#                     error.append((District_Name[district],row))
#                     continue
                
                
#                 if scenario == 'Historical':
#                     data_H = pd.concat([data_H,file['HWAM']], axis = 1)
#     Historical['Historical'] = data_H.mean(axis = 1)

# data_H.rename_columns = ['site_0', 'site_1', 'site_2', 'site_3']
# data_H = data_H.set_axis(['site_0', 'site_1', 'site_2', 'site_3'], axis=1, inplace=False)
# from scipy import stats


# site_0 = data_H.loc[20:]['site_0']
# site_1 = data_H.loc[20:]['site_1']
# site_2 = data_H.loc[20:]['site_2']
# site_3 = data_H.loc[20:]['site_3']
# site_avg = Historical.loc[20:]['Historical']

# from sklearn.metrics import r2_score
 
# coefficient_of_dermination_0 = r2_score(obs_data,site_0)

# res = stats.linregress(obs_data,site_0)
# r2_0 = res.rvalue

# coefficient_of_dermination_1 = r2_score(obs_data,site_1)

# res = stats.linregress(obs_data,site_1)
# r2_1 = res.rvalue

# coefficient_of_dermination_2 = r2_score(obs_data,site_2)

# res = stats.linregress(obs_data,site_2)
# r2_2 = res.rvalue

# coefficient_of_dermination_3 = r2_score(obs_data,site_3)

# res = stats.linregress(obs_data,site_3)
# r2_3 = res.rvalue

# coefficient_of_dermination_avg = r2_score(obs_data,site_avg)

# res = stats.linregress(obs_data,site_avg)
# r2_avg = res.rvalue


# print('The max r2 achieved is:',max(coefficient_of_dermination_0,coefficient_of_dermination_1,coefficient_of_dermination_2,coefficient_of_dermination_3,coefficient_of_dermination_avg))

# print('The max r2 excel achieved is:',max(r2_0,r2_1,r2_2,r2_3,r2_avg))