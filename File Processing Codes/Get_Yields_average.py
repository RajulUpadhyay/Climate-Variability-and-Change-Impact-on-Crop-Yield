# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 03:09:04 2023

@author: rajul
"""

import pandas as pd
data_H = pd.DataFrame()
data_nf_126 = pd.DataFrame()
data_ff_126 = pd.DataFrame()
data_nf_245 = pd.DataFrame()
data_ff_245 = pd.DataFrame()
data_nf_370 = pd.DataFrame()
data_ff_370 = pd.DataFrame()
data_nf_585 = pd.DataFrame()
data_ff_585 = pd.DataFrame()

Historical = pd.DataFrame()
near_future = pd.DataFrame()
far_future = pd.DataFrame()

nf_change = pd.DataFrame()
ff_change = pd.DataFrame()

District_Name=['Balod','Baloda','Balrampur','Bametara','Bastar','Bijapur','Bilaspur','DakshinBastar','Dhamtari','Durg','Gariaband','Janjgir','Jashpur','Kabeerdham','Kondagaon','Korba','Koriya','Mahasamund','Mungeli','Narayanpur','Raigarh','Raipur','Rajnandgaon','Sukma','Surajpur','Surguja','Uttarbastar']
d_coordinates = r'E:\MTP\New_District_coordinates'

write_path = 'E:\MTP\DSSAT\Batch_Files'
error = []
for district in range(len(District_Name)):
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

                try: file = pd.read_fwf(f'{directory}/Plantsum.OUT',skiprows = 3)
                except:
                    error.append((District_Name[district],row))
                    continue
                
                
                if scenario == 'Historical':
                    data_H = pd.concat([data_H,file['HWAM']], axis = 1)
                
                elif scenario == 'near_future': 
                    if ssp == 'ssp126':
                        data_nf_126 = pd.concat([data_nf_126,file['HWAM']], axis = 1)
                
                    elif ssp == 'ssp245':
                        data_nf_245 = pd.concat([data_nf_245,file['HWAM']], axis = 1)
                    
                    elif ssp == 'ssp370':
                        data_nf_370 = pd.concat([data_nf_370,file['HWAM']], axis = 1)
                    
                    else:
                        data_nf_585 = pd.concat([data_nf_585,file['HWAM']], axis = 1)
                
                else:
                
                    if ssp == 'ssp126':
                        data_ff_126 = pd.concat([data_ff_126,file['HWAM']], axis = 1)
                
                    elif ssp == 'ssp245':
                        data_ff_245 = pd.concat([data_ff_245,file['HWAM']], axis = 1)
                    
                    elif ssp == 'ssp370':
                        data_ff_370 = pd.concat([data_ff_370,file['HWAM']], axis = 1)
                    
                    else:
                        data_ff_585 = pd.concat([data_ff_585,file['HWAM']], axis = 1)
                        
        Historical['Historical'] = data_H.mean(axis = 1)
        
        near_future['ssp126'] = data_nf_126.mean(axis = 1)
        near_future['ssp245'] = data_nf_245.mean(axis = 1)
        near_future['ssp370'] = data_nf_370.mean(axis = 1)
        near_future['ssp585'] = data_nf_585.mean(axis = 1)
        
        far_future['ssp126'] = data_ff_126.mean(axis = 1)
        far_future['ssp245'] = data_ff_245.mean(axis = 1)
        far_future['ssp370'] = data_ff_370.mean(axis = 1)
        far_future['ssp585'] = data_ff_585.mean(axis = 1)
        
        Historical.to_excel(f'{write_path}/{District_Name[district]}/Historical_new.xlsx', index = None)
        near_future.to_excel(f'{write_path}/{District_Name[district]}/Near_Future_new.xlsx', index = None)
        far_future.to_excel(f'{write_path}/{District_Name[district]}/Far_Future_new.xlsx', index = None)
        
        yield_Historical = Historical['Historical'].mean()
        
        yield_nf_ssp126 = near_future['ssp126'].mean()
        yield_nf_ssp245 = near_future['ssp245'].mean()
        yield_nf_ssp370 = near_future['ssp370'].mean()
        yield_nf_ssp585 = near_future['ssp585'].mean()
        
        yield_ff_ssp126 = far_future['ssp126'].mean()
        yield_ff_ssp245 = far_future['ssp245'].mean()
        yield_ff_ssp370 = far_future['ssp370'].mean()
        yield_ff_ssp585 = far_future['ssp585'].mean()
        
        nf_change['ssp126'] = [ 100*(yield_Historical - yield_nf_ssp126)/yield_Historical ]
        nf_change['ssp245'] = [ 100*(yield_Historical - yield_nf_ssp245)/yield_Historical ]
        nf_change['ssp370'] = [ 100*(yield_Historical - yield_nf_ssp370)/yield_Historical ]
        nf_change['ssp585'] = [ 100*(yield_Historical - yield_nf_ssp585)/yield_Historical ]
        
        ff_change['ssp126'] = [ 100*(yield_Historical - yield_ff_ssp126)/yield_Historical ]
        ff_change['ssp245'] = [ 100*(yield_Historical - yield_ff_ssp245)/yield_Historical ]
        ff_change['ssp370'] = [ 100*(yield_Historical - yield_ff_ssp370)/yield_Historical ]
        ff_change['ssp585'] = [ 100*(yield_Historical - yield_ff_ssp585)/yield_Historical ]
        
        nf_change.to_excel(f'{write_path}/{District_Name[district]}/Near_Future_change_new.xlsx', index = None)
        ff_change.to_excel(f'{write_path}/{District_Name[district]}/Far_Future_change_new.xlsx', index = None)
        
        
        nf_change = pd.DataFrame()
        ff_change = pd.DataFrame()

        data_H = pd.DataFrame()
        data_nf_126 = pd.DataFrame()
        data_ff_126 = pd.DataFrame()
        data_nf_245 = pd.DataFrame()
        data_ff_245 = pd.DataFrame()
        data_nf_370 = pd.DataFrame()
        data_ff_370 = pd.DataFrame()
        data_nf_585 = pd.DataFrame()
        data_ff_585 = pd.DataFrame()
        
        Historical = pd.DataFrame()
        near_future = pd.DataFrame()
        far_future = pd.DataFrame()

# import pandas as pd
# import subprocess

# import time
# start_time = time.time()

# District_Name=['Balod','Baloda','Balrampur','Bametara','Bastar','Bijapur','Bilaspur','DakshinBastar','Dhamtari','Durg','Gariaband','Janjgir','Jashpur','Kabeerdham','Kondagaon','Korba','Koriya','Mahasamund','Mungeli','Narayanpur','Raigarh','Raipur','Rajnandgaon','Sukma','Surajpur','Surguja','Uttarbastar']
# d_coordinates = r'E:\MTP\New_District_coordinates'

# write_path = 'E:\MTP\DSSAT\Batch_Files'

# data_H = pd.DataFrame()
# data_nf = pd.DataFrame()
# data_ff  = pd.DataFrame()

# for district in range(len(District_Name)):
    
#     # df_H = pd.read_excel(f'{write_path}/{District_Name[district]}/Historical_new.xlsx')
#     # data_H = pd.concat([data_H,df_H], axis = 0)
    
#     df_nf = pd.read_excel(f'{write_path}/{District_Name[district]}/Near_Future_change_new.xlsx')
#     data_nf = pd.concat([data_nf,df_nf], axis = 0)
    
#     df_ff = pd.read_excel(f'{write_path}/{District_Name[district]}/Far_Future_change_new.xlsx')
#     data_ff = pd.concat([data_ff,df_ff], axis = 0)
    
                
# data_nf.to_excel(f'{write_path}/')       
        