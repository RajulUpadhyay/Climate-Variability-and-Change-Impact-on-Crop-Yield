# -*- coding: utf-8 -*-
"""
Created on Tue Feb  7 15:58:04 2023

@author: rajul
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 22:47:09 2023

@author: rajul
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
for var in ['pr']:
# for var in ['pr']:
    corr_file  = pd.read_excel(f'E:/MTP/Bias correction/Analysis/pr_new_corrected_3.xlsx', sheet_name='Sheet1')
    corr_file_change = pd.read_excel(f'E:/MTP/Bias correction/Analysis/pr_new_corrected_3.xlsx', sheet_name='Sheet2')
    raw_file = pd.read_excel(f'E:/MTP/Bias correction/Analysis/{var}_raw_new.xlsx', sheet_name='Sheet1')
    raw_file_change  = pd.read_excel(f'E:/MTP/Bias correction/Analysis/{var}_raw_new.xlsx', sheet_name='Sheet2')
    
        
    
    plt.rcParams.update({'font.size': 7})
    plt.rcParams['figure.figsize'] = [10, 4]
    figure, axis = plt.subplots(1,2)
    figure.subplots_adjust(hspace=0.4, wspace=0.3)
    
    
    for file in range(2):
        if file == 0: 
            loop = 0
            file = raw_file
            change = raw_file_change
        else: 
            loop = 1 
            file = corr_file
            change = corr_file_change
    
        
        # axis.hold(True)
        
        
        x = np.array(file[:]['Unnamed: 0'])
        Observed = np.array(file[:]['Observed'])
        Historical = np.array(file[:]['Historical'])
        
        
        if loop == 0:
            axis[loop].set_title("Raw Data",fontname="Times New Roman", size=16,fontweight="bold")
        else:
            axis[loop].set_title("Corrected Data",fontname="Times New Roman", size=16,fontweight="bold")
        axis[loop].plot(x, Observed, color='black', label='Observed')
        axis[loop].plot(x, Historical, color='dimgrey', label='Historical')
        
        
        for scenario in ['ssp126', 'ssp245', 'ssp370', 'ssp585']:
            
            
            Near_Future = np.array(file[:][f'{scenario}_Near future'])
            Future = np.array(file[:][f'{scenario}_Future'])
            Far_Future = np.array(file[:][f'{scenario}_Far future'])
            
            change_Near_Future = np.array(change[:][f'{scenario}_Near future'])
            change_Future = np.array(change[:][f'{scenario}_Future'])
            change_Far_Future = np.array(change[:][f'{scenario}_Far future'])
            
            
            if scenario == 'ssp126':
                color_1 = '#90EE90'
                color_2 = '#32CD32'
                color_3 = '#228B22'
            
            elif scenario == 'ssp245':
                color_1 = '#FFFFE0'
                color_2 = '#FFFF00'
                color_3 = '#9B870C'
                
            elif scenario == 'ssp370':
                color_1 = '#FFA07A'
                color_2 = '#CC5500'
                color_3 = '#8B2500'
            
            else:
                color_1 = '#FFB6C1'
                color_2 = '#FF0000'
                color_3 = '#8B0000'
                
            axis[loop].plot(x, Near_Future, color=color_1, label=f'{scenario} Near Future')
            axis[loop].plot(x, Future, color=color_2, label=f'{scenario} Future')
            axis[loop].plot(x, Far_Future, color=color_3, label=f'{scenario} Far Future')
            axis[loop].set_xlabel("Month",fontname="Times New Roman", size=10,fontweight="bold")
            axis[loop].set_ylabel("Temperature (°C)",fontname="Times New Roman", size=10,fontweight="bold")
            
            # axis.hold(True)
            
            # ax2 =  axis[loop].twinx()
            
            # ax2.bar(x,change_Far_Future, color='darksalmon',width=0.5,label='Far Future', bottom=0)
            # ax2.bar(x,change_Future, color='cyan',width=0.5,label='Future', bottom=0)
            # ax2.bar(x,change_Near_Future, color='grey',width=0.5,label='Near Future', bottom=0)
            # ax2.set_ylabel("Percentage Change",fontname="Times New Roman", size=10,fontweight="bold")
            
            
            # if var == 'pr': ax2.set_ylim(-35,130)
            # elif var == 'tasmin': ax2.set_ylim(-10,70)
            # else:ax2.set_ylim(-10,30)
            # ax2.legend(fontsize=5,loc = 'upper left')
        axis[loop].legend(fontsize=5)
        axis[loop].set_facecolor("#E0FFFF")
        # axis.hold(True)
    # axis.hold(False)
    plt.savefig(f'E:/MTP/Bias correction/Analysis/plot_alltogether_{var}_.png', dpi=350)