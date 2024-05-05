# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 17:19:38 2023

@author: rajul
"""

import pandas as pd
import pickle
import datetime
# tz_localize(None)
import warnings
warnings.filterwarnings("ignore")


with open('E:/MTP/DSSAT-Old/Random_Forest.pkl', 'rb') as file:
    RF = pickle.load(file)

corr_code = {
    1: 'A',
    2: 'B',
    3: 'C',
    4: 'D',
    5: 'E',
    6: 'F',
    7: 'G',
    8: 'H',
    9: 'I',
    10: 'J',
    11: 'K',
    12: 'L',
    13: 'M',
    14: 'N',
    15: 'O',
    16: 'P',
    17: 'Q',
    18: 'R',
    19: 'S',
    20: 'T'
}
    
def soil_maker(N, E, district, district_code,row):
    def line_one(site_code):
        line_0 = '\n'
        line_1= '{:>11}  FAO         SCL      100  -99'.format(site_code)
        line_2 = '@SITE        COUNTRY          LAT     LONG SCS FAMILY'
        with open('E:\MTP\DSSAT\Database\Standard_Files/SOIL.SOL', 'a') as file:
            for line in [line_0,line_1,line_2]:
                file.write(line+'\n')
            
    def line_two(place,lat,lon):
        line_1 = '{:>7}      India           {:>5}   {:>5} -99'.format(place,lat,lon)
        line_2 = '@ SCOM  SALB  SLU1  SLDR  SLRO  SLNF  SLPF  SMHB  SMPX  SMKE'
        line_3 = '    BL   .09     6    .6    73     1    .8 IB001 IB001 IB001'
        line_4 = '@  SLB  SLMH  SLLL  SDUL  SSAT  SRGF  SSKS  SBDM  SLOC  SLCL  SLSI  SLCF  SLNI  SLHW  SLHB  SCEC  SADC'
        
        with open('E:\MTP\DSSAT\Database\Standard_Files/SOIL.SOL', 'a') as file:
            for line in [line_1,line_2,line_3,line_4]:
                file.write(line+'\n')
    
    def soil(lat,lon):
        data = pd.read_excel('E:/MTP/FAO Soil Data/DSMW/Soil data/0.25x0.25_Soil_Layer_1.xlsx')
        data = data[(data['N']==lat) & (data['E']==lon)]
        
        line_1 = '    30     a  {:>4}  {:>4}  {:>4}   .90  {:>4}  {:>4}  {:>4}  {:>4}  {:>4}     0   -99     8   -99   -99   -99'.format(round(float(data['SLLL']),2),round(float(data['SDUL']),2),round(float(data['SSAT']),2),round(float(data['SSKS']),2),round(float(data['SBDM']),2),round(float(data['SLOC']),2),round(float(data['SLCL']),1),round(float(data['SLSI']),1))
        data = pd.read_excel('E:/MTP/FAO Soil Data/DSMW/Soil data/0.25x0.25_Soil_Layer_2.xlsx')
        data = data[(data['N']==lat) & (data['E']==lon)]
        line_2 = '   100     b  {:>4}  {:>4}  {:>4}   .90  {:>4}  {:>4}  {:>4}  {:>4}  {:>4}     0   -99     8   -99   -99   -99'.format(round(float(data['SLLL']),2),round(float(data['SDUL']),2),round(float(data['SSAT']),2),round(float(data['SSKS']),2),round(float(data['SBDM']),2),round(float(data['SLOC']),2),round(float(data['SLCL']),1),round(float(data['SLSI']),1))
        with open('E:\MTP\DSSAT\Database\Standard_Files/SOIL.SOL', 'a') as file:
            for line in [line_1,line_2]:
                file.write(line+'\n')
    
    if row<10: site_code = '*' + str(district_code) + '0000000' + str(row)
    else: site_code = '*' + str(district_code) + '000000' + str(row)
    line_one(site_code)
    
    line_two(district,N,E)
    soil(N,E)


def create_WTH_file(file, station_name, N, E):
    def three_digit(value):
        value = str(value)
        
        if len(value) == 1:
            return '00' + value
        
        elif len(value) == 2:
            return '0' + value
        
        else: return value


    def prepare_df(file):
        # import numpy as np
        data = file
        
        row,col = data.shape
        
        start_year = data['Year'][1]
        end_year = data['Year'][row-1]
        
        data['Date'] = pd.date_range(start = f'01-01-{start_year}', end = f'31-12-{end_year}', freq= 'D')
        
        data['day_of_year'] = data['Date'].dt.dayofyear
        
        data['new_date'] = ['' for i in range(row)]
        
        for row in range(row):
            data['new_date'][row] = str(data['Year'][row]) + three_digit(data['day_of_year'][row])
        
        final_df = pd.DataFrame()
        final_df['DATE'] = data['new_date']
        final_df['SRAD'] = data['Rad'].map('{:.1f}'.format)
        final_df['TMAX'] = data['MaxT'].map('{:.1f}'.format)
        final_df['TMIN'] = data['MinT'].map('{:.1f}'.format)
        final_df['RAIN'] = data['Rain'].map('{:.1f}'.format)
        
        return final_df
    
    def amp_calc(file):
        df = file.copy()
        row,col = df.shape
        
        start_year = df['Year'][1]
        end_year = df['Year'][row-1]
        
        # Convert date column to datetime object
        df['Date'] = pd.date_range(start = f'01-01-{start_year}',end = f'31-12-{end_year}',freq = 'D')
        
        # Group data by year and month
        grouped = df.groupby([df['Date'].dt.year, df['Date'].dt.month])
        
        # Calculate sum of precipitation for each month
        sum_precip = grouped['Rain'].sum()
        
        # Calculate number of days in each month
        num_days = grouped['Date'].agg(lambda x: len(x.unique()))
        
        # Calculate average monthly precipitation
        amp_p = sum_precip / num_days
        
        # Calculate mean monthly temperature
        df['Month'] = df['Date'].dt.month
        
        # Group the data by month and calculate mean temperature for each month
        monthly_data = df.groupby('Month')[['MaxT', 'MinT']].mean()
        
        # Calculate mean monthly temperature from Tmax and Tmin
        monthly_data['MeanTemp'] = (monthly_data['MaxT'] + monthly_data['MinT']) / 2.0
        
        mean_t = monthly_data['MeanTemp'].mean()
        
        # Calculate daily temperature difference
        df['TempDiff'] = df['MaxT'] - df['MinT']
        
        # Group data by year, month, and day
        grouped = df.groupby([df['Date'].dt.year, df['Date'].dt.month, df['Date'].dt.day])
        
        # Calculate daily temperature difference from mean monthly temperature
        amp_t = grouped['TempDiff'].mean() - mean_t
        
        # Calculate absolute value of daily temperature difference from mean monthly temperature
        amp_t = abs(amp_t)
        
        # Group data by year and month
        grouped = df.groupby([df['Date'].dt.year, df['Date'].dt.month])
        
        # Calculate average monthly temperature difference
        amp_t = grouped['TempDiff'].mean()
        
        # Calculate absolute value of average monthly temperature difference from mean monthly temperature
        amp_t = abs(amp_t - mean_t)
        
        # Calculate AMP
        amp = amp_p + amp_t
        
        # Calculate the mean of amp values
        mean_amp = amp.mean()
        
        # Print the resulting mean value
        # print(mean_amp)
        return '{:.1f}'.format(mean_amp),'{:.1f}'.format(mean_t)
    
    def write_file(df,name,lat,lon,amp,mean_t):
        row, col = df.shape
        
        line_0 = '$WEATHER DATA : {:>4}'.format(name)
        line_1 = ''
        line_2 = '@ INSI      LAT     LONG  ELEV   TAV   AMP REFHT WNDHT'
        line_3 = '  {:>4}    {:>5}    {:>5}   300  {:>4}  {:>4} -99.0 -99.0'.format(name, lat, lon, mean_t, amp)
        line_4 = '@  DATE  SRAD  TMAX  TMIN  RAIN'
        
        
        # line_5 = '1981001  14.3  25.1  11.8   0.0'
        
        with open(f'E:\MTP\DSSAT\Database\Files_wrote\WTH/{name}.WTH', 'a') as file:
            for line in [line_0, line_1,line_2,line_3,line_4]:
                file.write(line+'\n')
                
            for row in range(row):
                # print(line,df['DATE'][row], df['SRAD'][row], df['TMAX'][row], df['TMIN'][row], df['RAIN'][row])
                file.write('{:>7}  {:>4}  {:>4}  {:>4} {:>5}'.format(df['DATE'][row], df['SRAD'][row], df['TMAX'][row], df['TMIN'][row], df['RAIN'][row]) + '\n')
            
    
    name = station_name
    # file = 'E:/MTP/DSSAT/Raipur/Historical/Base_period.xlsx'
    amp,mean_t = amp_calc(file)
    data = prepare_df(file)
    
    write_file(data, name, N, E, amp, mean_t)


def write_CLI(file,name,N,E):
    def get_dataframes(file):
        data = file.copy()
        start = data['Year'][0]
        end = data['Year'][len(data)-1]
        
        start_date = datetime.datetime(start, 1, 1)
        end_date = datetime.datetime(end, 12, 31)
        date_range = pd.date_range(start=start_date, end=end_date)
        
        df = pd.DataFrame(index=date_range)
        data['Year'] = df.index.date
        
        
        
        data['month'] = ''
        data['Rainyday'] = ''
        
        for i in range(len(data)):
            if data['Rain'][i] > 0:
                data['Rainyday'][i] = 1
            else:
                data['Rainyday'][i] = 0
            
        for i in range(len(data)):
            data['month'][i] = str(data['Year'][i])[5:7]
            
        new_data = pd.DataFrame(columns=['Month','SAMN','XAMN','NAMN','RTOT','RNUM'])
        
        new_data['Month'] = data['Day'][:12]
        
        for i in range(len(new_data)):
            new_data['SAMN'][i] = round(data.groupby('month')['Rad'].mean()[i],1)
            new_data['XAMN'][i] = round(data.groupby('month')['MaxT'].mean()[i],1)
            new_data['NAMN'][i] = round(data.groupby('month')['MinT'].mean()[i],1)
            new_data['RTOT'][i] = round(data.groupby('month')['Rain'].mean()[i]*34, 1)
            new_data['RNUM'][i] = round(data.groupby('month')['Rainyday'].sum()[i]/34,1)
            
        
        # *****************************************************************************
        
        dry_data = data[data['Rain']==0]
        wet_data = data[data['Rain']!=0]        
                
        new_data2 = pd.DataFrame(columns=['MTH','SDMN','SDSD','SWMN','SWSD','XDMN','XDSD','XWMN','XWSD','NAMN',
                                          'NASD','ALPHA','RTOT','PDW','RNUM'])
        
        new_data2['MTH'] = data['Day'][:12]
        
        alpha = [0.489, 0.574, 0.362, 0.520, 0.582, 0.345, 0.427, 0.224, 0.399, 0.370, 0.328, 0.216]
        pdw = [0.039, 0.062, 0.051, 0.072, 0.107, 0.284, 0.535, 0.441, 0.297, 0.086, 0.021, 0.019]
        for i in range(len(new_data2)):
                new_data2['SDMN'][i] = round(dry_data.groupby('month')['Rad'].mean()[i],1)
                new_data2['SDSD'][i] = round(dry_data.groupby('month')['Rad'].std()[i],1)
                new_data2['SWMN'][i] = round(wet_data.groupby('month')['Rad'].mean()[i],1)
                new_data2['SWSD'][i] = round(wet_data.groupby('month')['Rad'].std()[i],1)
                new_data2['XDMN'][i] = round(dry_data.groupby('month')['MaxT'].mean()[i],1)
                new_data2['XDSD'][i] = round(dry_data.groupby('month')['MaxT'].std()[i],1)
                new_data2['XWMN'][i] = round(wet_data.groupby('month')['MaxT'].mean()[i],1)
                new_data2['XWSD'][i] = round(wet_data.groupby('month')['MaxT'].std()[i],1)
                new_data2['NAMN'][i] = round(data.groupby('month')['MinT'].mean()[i],1)
                new_data2['NASD'][i] = round(data.groupby('month')['MinT'].std()[i],1)
                new_data2['RTOT'][i] = round(data.groupby('month')['Rain'].mean()[i]*34,1)
                new_data2['RNUM'][i] = round(data.groupby('month')['Rainyday'].sum()[i]/34,1)
                # new_data2['ALPHA'][i],loc,scale = gamma.fit(data.groupby('month')['Rain'])[0]
                new_data2['ALPHA'][i] = alpha[i]
                new_data2['PDW'][i] = pdw[i]
        
        return new_data, new_data2
    
    def amp_calc(file):
        df = file.copy()
        length = len(df)
        row,col = df.shape
        
        start_year = df['Year'][1]
        end_year = df['Year'][row-1]
        
        # Convert date column to datetime object
        df['Date'] = pd.date_range(start = f'01-01-{start_year}',end = f'31-12-{end_year}',freq = 'D')
        
        # Group data by year and month
        grouped = df.groupby([df['Date'].dt.year, df['Date'].dt.month])
        
        # Calculate sum of precipitation for each month
        sum_precip = grouped['Rain'].sum()
        
        # Calculate number of days in each month
        num_days = grouped['Date'].agg(lambda x: len(x.unique()))
        
        # Calculate average monthly precipitation
        amp_p = sum_precip / num_days
        
        # Calculate mean monthly temperature
        df['Month'] = df['Date'].dt.month
        
        # Group the data by month and calculate mean temperature for each month
        monthly_data = df.groupby('Month')[['MaxT', 'MinT']].mean()
        
        # Calculate mean monthly temperature from Tmax and Tmin
        monthly_data['MeanTemp'] = (monthly_data['MaxT'] + monthly_data['MinT']) / 2.0
        
        mean_t = monthly_data['MeanTemp'].mean()
        
        # Calculate daily temperature difference
        df['TempDiff'] = df['MaxT'] - df['MinT']
        
        # Group data by year, month, and day
        grouped = df.groupby([df['Date'].dt.year, df['Date'].dt.month, df['Date'].dt.day])
        
        # Calculate daily temperature difference from mean monthly temperature
        amp_t = grouped['TempDiff'].mean() - mean_t
        
        # Calculate absolute value of daily temperature difference from mean monthly temperature
        amp_t = abs(amp_t)
        
        # Group data by year and month
        grouped = df.groupby([df['Date'].dt.year, df['Date'].dt.month])
        
        # Calculate average monthly temperature difference
        amp_t = grouped['TempDiff'].mean()
        
        # Calculate absolute value of average monthly temperature difference from mean monthly temperature
        amp_t = abs(amp_t - mean_t)
        
        # Calculate AMP
        amp = amp_p + amp_t
        
        # Calculate the mean of amp values
        mean_amp = amp.mean()
        
        # Print the resulting mean value
        # print(mean_amp)
        return '{:.1f}'.format(mean_amp),'{:.1f}'.format(mean_t)  ,length    
    
    def averages_data(file):
        df = file.copy()
        row,col = df.shape
        
        start_year = df['Year'][1]
        end_year = df['Year'][row-1]
        
        # Convert date column to datetime object
        df['Date'] = pd.date_range(start = f'01-01-{start_year}',end = f'31-12-{end_year}',freq = 'D')
        
        df = df.set_index('Date')
        TMXY = df['MaxT'].resample('Y').mean().mean()
        TMNY = df['MinT'].resample('Y').mean().mean()
        RAIY = df['Rain'].resample('Y').sum().mean()
        SRAY = df['Rad'].resample('Y').mean().mean()
        return round(TMXY,1), round(TMNY,1), round(RAIY),round(SRAY,1),start_year, end_year - start_year
    
    
    def write_file(name, lat, lon, tav, amp, new_data, new_data2,length,TMXY, TMNY, RAIY,SRAY,start_year,duration):
                    # name, N, E, tav, amp, new_data, new_data2,length,TMXY, TMNY, RAIY,SRAY,start_year,duration
                # name, 30, 70, tav, amp, new_data, new_data2,length,TMXY, TMNY, RAIY,SRAY,duration
        line_0 = '*CLIMATE:{:>4}'.format(name)
        line_1 = ''
        line_2 = '@ INSI      LAT     LONG  ELEV   TAV   AMP  SRAY  TMXY  TMNY  RAIY'
        line_3 = '  {:>4}    {:>5}    {:>5}   300  {:>4}  {:>4}  {:>4}  {:>4}  {:>4}  {:>4}'.format(name,lat,lon,tav,amp,SRAY,TMXY,TMNY,RAIY)
        line_4 = '@START  DURN  ANGA  ANGB REFHT WNDHT SOURCE'
        line_5 = '  {:>4}    {:>2}  0.25  0.50 -99.0 -99.0 Calculated_from_daily_data'.format(start_year,duration)
        line_6 = '@ GSST  GSDU'
        line_7 = '     1   365'
        line_8 = ''
        line_9 = '*MONTHLY AVERAGES'
        line_10 = '@  MTH  SAMN  XAMN  NAMN  RTOT  RNUM  SHMN  AMTH  BMTH'
        
        with open(f'E:\MTP\DSSAT\Database\Files_wrote\CLI/{name}.CLI', 'a') as file:
            for line in [line_0, line_1,line_2,line_3,line_4, line_5, line_6, line_7, line_8, line_9, line_10]:
                file.write(line+'\n')
                
            for row in range(12):
                file.write('    {:>2}  {:>4}  {:>4}  {:>4} {:>5}  {:>4}   -99 0.250 0.500'.format(new_data['Month'][row], new_data['SAMN'][row], new_data['XAMN'][row], new_data['NAMN'][row], new_data['RTOT'][row], new_data['RNUM'][row]) + '\n')
            
            file.write('\n')
            file.write('*WGEN PARAMETERS' +'\n')
            
            file.write('@  MTH  SDMN  SDSD  SWMN  SWSD  XDMN  XDSD  XWMN  XWSD  NAMN  NASD ALPHA  RTOT   PDW  RNUM' + '\n')
            
            for row in range(12):
                file.write('    {:>2}  {:>4}   {:>3}  {:>4}   {:>3}  {:>4}   {:>3}  {:>4}   {:>3}  {:>4}   {:>3} {:>5} {:>5} {:>5}  {:>4}'.format(new_data2['MTH'][row], new_data2['SDMN'][row],new_data2['SDSD'][row], new_data2['SWMN'][row], 
                                  new_data2['SWSD'][row], new_data2['XDMN'][row],new_data2['XDSD'][row], new_data2['XWMN'][row],
                                  new_data2['XWSD'][row], new_data2['NAMN'][row],new_data2['NASD'][row], new_data2['ALPHA'][row],
                                  new_data2['RTOT'][row], new_data2['PDW'][row],new_data2['RNUM'][row]) + '\n')
            
            file.write('\n')
            
            file.write('*RANGE CHECK VALUES' + '\n')
            file.write('@      SRAD  TMAX  TMIN  RAIN  DEWP  WIND  SUNH   PAR  TDRY  TWET  EVAP  RHUM' + '\n')
            file.write('MIN :   0.5 -30.0 -40.0   0.0 -40.0   0.0   0.0   5.0 -40.0 -40.0   0.0   0.0' + '\n')
            file.write('MAX :  85.0  65.0  45.0 600.0  40.0 500.0 100.0  85.0  40.0  40.0  15.0 100.0' + '\n')
            file.write('RATE:  70.0  20.0  20.0 500.0   5.0 300.0  90.0  70.0  20.0  20.0  15.0  75.0' + '\n')
            
            file.write('\n')
            
            file.write('*FLAGGED DATA COUNT' + '\n')
            file.write('@BEGYR BEGMN BEGDY ENDYR ENDMN ENDDY' + '\n')
            file.write('  {:>4}     1     1  {:>4}    12    31'.format(start_year,start_year+duration) + '\n')
            file.write('@         TOTAL   RAIN   TMAX   TMIN   SRAD   SUNH   DEWP   WIND    PAR   TDRY   TWET   EVAP   RHUM' + '\n')
            file.write(f'Total  :  {4*length}  {length}  {length}  {length}  {length}      0      0      0      0      0      0      0      0' + '\n')
            file.write(f'Valid  :  {4*length}  {length}  {length}  {length}  {length}      0      0      0      0      0      0      0      0' + '\n')
            
            file.write('Missing:      0      0      0      0      0      0      0      0      0      0      0      0      0' + '\n')
            file.write('Error  :      0      0      0      0      0      0      0      0      0      0      0      0      0' + '\n')
            
            file.write('Above  :      0      0      0      0      0      0      0      0      0      0      0      0      0' + '\n')
            file.write('Below  :      0      0      0      0      0      0      0      0      0      0      0      0      0' + '\n')
            file.write('Rate   :      0      0      0      0      0      0      0      0      0      0      0      0      0' + '\n')

    name = name
    # file = 'E:\MTP\DSSAT-OLD\Bametara\ssp126/2021_2060_period.xlsx'
    amp,tav,length = amp_calc(file)
    new_data, new_data2 = get_dataframes(file)
    TMXY, TMNY, RAIY,SRAY,start_year,duration = averages_data(file)
    write_file(name, N, E, tav, amp, new_data, new_data2,length,TMXY, TMNY, RAIY,SRAY,start_year,duration)
        



District_Name=['Balod','Baloda','Balrampur','Bametara','Bastar','Bijapur','Bilaspur','DakshinBastar','Dhamtari','Durg','Gariaband','Janjgir','Jashpur','Kabeerdham','Kondagaon','Korba','Koriya','Mahasamund','Mungeli','Narayanpur','Raigarh','Raipur','Rajnandgaon','Sukma','Surajpur','Surguja','Uttarbastar']
code = ['BA','BD','BL','BM','BT', 'BJ', 'BS','DB', 'DH', 'DU', 'GA', 'JG', 'JS', 'KW', 'KG', 'KO', 'KR', 'MH', 'MU','NR', 'RG', 'RP', 'RJ', 'SU', 'SR', 'SJ', 'UT']
d_coordinates = r'E:\MTP\New_District_coordinates'
w_std_file = 'E:\MTP\DSSAT\Database\Standard_Files'
weather_database = 'E:\MTP\DSSAT\Database\Weather'


pr_Hist = pd.read_csv(f'{weather_database}/Historical/pr_Historical_1981_2014_T.csv')
tasmax_Hist = pd.read_csv(f'{weather_database}/Historical/tasmax_Historical_1981_2014_T.csv')
tasmin_Hist = pd.read_csv(f'{weather_database}/Historical/tasmin_Historical_1981_2014_T.csv')

pr_ssp126_nf = pd.read_csv(f'{weather_database}/ssp126/pr_ssp126_2021_2060_T.csv')
tasmax_ssp126_nf = pd.read_csv(f'{weather_database}/ssp126/tasmax_ssp126_2021_2060_T.csv')
tasmin_ssp126_nf = pd.read_csv(f'{weather_database}/ssp126/tasmin_ssp126_2021_2060_T.csv')

pr_ssp126_ff = pd.read_csv(f'{weather_database}/ssp126/pr_ssp126_2061_2100_T.csv')
tasmax_ssp126_ff = pd.read_csv(f'{weather_database}/ssp126/tasmax_ssp126_2061_2100_T.csv')
tasmin_ssp126_ff = pd.read_csv(f'{weather_database}/ssp126/tasmin_ssp126_2061_2100_T.csv')

pr_ssp245_nf = pd.read_csv(f'{weather_database}/ssp245/pr_ssp245_2021_2060_T.csv')
tasmax_ssp245_nf = pd.read_csv(f'{weather_database}/ssp245/tasmax_ssp245_2021_2060_T.csv')
tasmin_ssp245_nf = pd.read_csv(f'{weather_database}/ssp245/tasmin_ssp245_2021_2060_T.csv')

pr_ssp245_ff = pd.read_csv(f'{weather_database}/ssp245/pr_ssp245_2061_2100_T.csv')
tasmax_ssp245_ff = pd.read_csv(f'{weather_database}/ssp245/tasmax_ssp245_2061_2100_T.csv')
tasmin_ssp245_ff = pd.read_csv(f'{weather_database}/ssp245/tasmin_ssp245_2061_2100_T.csv')

pr_ssp370_nf = pd.read_csv(f'{weather_database}/ssp370/pr_ssp370_2021_2060_T.csv')
tasmax_ssp370_nf = pd.read_csv(f'{weather_database}/ssp370/tasmax_ssp370_2021_2060_T.csv')
tasmin_ssp370_nf = pd.read_csv(f'{weather_database}/ssp370/tasmin_ssp370_2021_2060_T.csv')

pr_ssp370_ff = pd.read_csv(f'{weather_database}/ssp370/pr_ssp370_2061_2100_T.csv')
tasmax_ssp370_ff = pd.read_csv(f'{weather_database}/ssp370/tasmax_ssp370_2061_2100_T.csv')
tasmin_ssp370_ff = pd.read_csv(f'{weather_database}/ssp370/tasmin_ssp370_2061_2100_T.csv')

pr_ssp585_nf = pd.read_csv(f'{weather_database}/ssp585/pr_ssp585_2021_2060_T.csv')
tasmax_ssp585_nf = pd.read_csv(f'{weather_database}/ssp585/tasmax_ssp585_2021_2060_T.csv')
tasmin_ssp585_nf = pd.read_csv(f'{weather_database}/ssp585/tasmin_ssp585_2021_2060_T.csv')

pr_ssp585_ff = pd.read_csv(f'{weather_database}/ssp585/pr_ssp585_2061_2100_T.csv')
tasmax_ssp585_ff = pd.read_csv(f'{weather_database}/ssp585/tasmax_ssp585_2061_2100_T.csv')
tasmin_ssp585_ff = pd.read_csv(f'{weather_database}/ssp585/tasmin_ssp585_2061_2100_T.csv')




error = list()
for district in range(len(District_Name)):
# for district in range(3):
    d_corr = pd.read_csv(f'{d_coordinates}/{District_Name[district]}.csv')
    rows,cols = d_corr.shape
    
    for row in range(rows):
        E , N = d_corr.loc[row][0],d_corr.loc[row][1]
        soil_maker(N, E, District_Name[district], code[district],row)
        
        for ssp in ['Historical', 'ssp126', 'ssp245', 'ssp370', 'ssp585']:
            if ssp == 'Historical': 
                years = [(1981,2014)]
                scenarios = ['Historical']
            else: 
                years = [(2021,2060), (2061,2100)]
                scenarios = ['near_future', 'far_future']
            
            for scenario in scenarios:
                data = pd.read_excel(f'{w_std_file}/{scenario}.xlsx')
                
                if scenario == 'near_future': 
                    years = [2021,2060]
                    if ssp =='ssp126':scenario_code = 'A'
                    if ssp =='ssp245':scenario_code = 'C'
                    if ssp =='ssp370':scenario_code = 'E'
                    if ssp =='ssp585':scenario_code = 'G'
                    
                elif scenario == 'far_future': 
                    years = [2061,2100]
                    if ssp =='ssp126':scenario_code = 'B'
                    if ssp =='ssp245':scenario_code = 'D'
                    if ssp =='ssp370':scenario_code = 'F'
                    if ssp =='ssp585':scenario_code = 'H'
                else: 
                    years = [1981,2014]
                    scenario_code = 'O'
                
                # prep = pd.read_csv(f'{weather_database}/{ssp}/pr_{ssp}_{years[0]}_{years[1]}_T.csv')
                # tasmax = pd.read_csv(f'{weather_database}/{ssp}/tasmax_{ssp}_{years[0]}_{years[1]}_T.csv')
                # tasmin = pd.read_csv(f'{weather_database}/{ssp}/tasmin_{ssp}_{years[0]}_{years[1]}_T.csv')
                
                
                if ssp == 'Historical':
                    prep = pr_Hist
                    tasmax = tasmax_Hist
                    tasmin = tasmin_Hist
                
                if ssp == 'ssp126':
                    if scenario == 'near_future':
                        prep = pr_ssp126_nf
                        tasmax = tasmax_ssp126_nf
                        tasmin = tasmin_ssp126_nf
                    
                    else:
                        prep = pr_ssp126_ff
                        tasmax = tasmax_ssp126_ff
                        tasmin = tasmin_ssp126_ff
                        
                if ssp == 'ssp245':
                    if scenario == 'near_future':
                        prep = pr_ssp245_nf
                        tasmax = tasmax_ssp245_nf
                        tasmin = tasmin_ssp245_nf
                    
                    else:
                        prep = pr_ssp245_ff
                        tasmax = tasmax_ssp245_ff
                        tasmin = tasmin_ssp245_ff
                        
                        
                if ssp == 'ssp370':
                    if scenario == 'near_future':
                        prep = pr_ssp370_nf
                        tasmax = tasmax_ssp370_nf
                        tasmin = tasmin_ssp370_nf
                    
                    else:
                        prep = pr_ssp370_ff
                        tasmax = tasmax_ssp370_ff
                        tasmin = tasmin_ssp370_ff
                        
                if ssp == 'ssp585':
                    if scenario == 'near_future':
                        prep = pr_ssp585_nf
                        tasmax = tasmax_ssp585_nf
                        tasmin = tasmin_ssp585_nf
                    
                    else:
                        prep = pr_ssp585_ff
                        tasmax = tasmax_ssp585_ff
                        tasmin = tasmin_ssp585_ff
                
                
                prep_subset = prep[(prep['E']==E) & (prep['N']==N)]
                prep_subset = prep_subset.reset_index()
                prep_subset = prep_subset.drop('index',axis = 1)
                prep_subset = prep_subset.T
                prep_subset = prep_subset.drop('N',axis = 0)
                prep_subset = prep_subset.drop('E',axis = 0)
                prep_subset = prep_subset.reset_index()
                prep_subset = prep_subset.drop('index',axis = 1)
                try: data['Rain'] = prep_subset[0]
                except:
                    error.append((N,E))
                    continue
                
                tasmax_subset = tasmax[(tasmax['E']==E) & (tasmax['N']==N)]
                tasmax_subset = tasmax_subset.reset_index()
                tasmax_subset = tasmax_subset.drop('index',axis = 1)
                tasmax_subset = tasmax_subset.T
                tasmax_subset = tasmax_subset.drop('N',axis = 0)
                tasmax_subset = tasmax_subset.drop('E',axis = 0)
                tasmax_subset = tasmax_subset.reset_index()
                tasmax_subset = tasmax_subset.drop('index',axis = 1)
                data['MaxT'] = tasmax_subset[0]
                
                tasmin_subset = tasmin[(tasmin['E']==E) & (tasmin['N']==N)]
                tasmin_subset = tasmin_subset.reset_index()
                tasmin_subset = tasmin_subset.drop('index',axis = 1)
                tasmin_subset = tasmin_subset.T
                tasmin_subset = tasmin_subset.drop('N',axis = 0)
                tasmin_subset = tasmin_subset.drop('E',axis = 0)
                tasmin_subset = tasmin_subset.reset_index()
                tasmin_subset = tasmin_subset.drop('index',axis = 1)
                data['MinT'] = tasmin_subset[0]
                
                predictions = RF.predict(data[['MaxT', 'MinT', 'Rain']])
                data['Rad'] = predictions
                
                data_CLI = data.copy()
                station_name = str(code[district]) + scenario_code + corr_code[row+1]
                create_WTH_file(data, station_name, N, E)
                write_CLI(data_CLI, station_name,N,E)