# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.13.0
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Read and Plot CAN trace data collected via Peak Adapter
#     Name : Sanghyeok Lee
#     Created date : July 31, 2021 (Saturday) 05:41 pm
#     Updated : September 26, 2021 (Sunday) 10:47 am
#     Updated : Octoboer 09, 2021 (Saturday) 02:07 pm
#     Updated : Octoboer 24, 2021 (Sunday) 05:34 pm
#     Updated : December 30, 2021 (Thursday) 10:45 am in Jeju Island
#     
#     
#     

# ## What I have to figure out..
# 1. save the header and backup it
# 2. save the others into a data frame
# 3. multipacket data...?

# ### pandas.read_csv
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
#
# pandas.read_csv(filepath_or_buffer, sep=NoDefault.no_default, delimiter=None, header='infer', names=NoDefault.no_default, index_col=None, usecols=None, squeeze=False, prefix=NoDefault.no_default, mangle_dupe_cols=True, dtype=None, engine=None, converters=None, true_values=None, false_values=None, skipinitialspace=False, skiprows=None, skipfooter=0, nrows=None, na_values=None, keep_default_na=True, na_filter=True, verbose=False, skip_blank_lines=True, parse_dates=False, infer_datetime_format=False, keep_date_col=False, date_parser=None, dayfirst=False, cache_dates=True, iterator=False, chunksize=None, compression='infer', thousands=None, decimal='.', lineterminator=None, quotechar='"', quoting=0, doublequote=True, escapechar=None, comment=None, encoding=None, encoding_errors='strict', dialect=None, error_bad_lines=None, warn_bad_lines=None, on_bad_lines=None, delim_whitespace=False, low_memory=True, memory_map=False, float_precision=None, storage_options=None)[source]
#
#

# ## Let's find a row number where data part starts

# read the CAN trace file without any attributes 
import pandas as pd
can_trc_file_location = '/Users/sanghyeoklee/Desktop/Sanghyeok/Study/data/100D-9B/P2021-06-30_14-59-35_659.trc'
TRC_raw = pd.read_csv(can_trc_file_location,header=None)
# if "header=0", the first row will be read as a column name
print('  read CAN trace file(----.trc) completed \n')
print(' type : ',type(TRC_raw)) #dataframe
print(f'  size : {TRC_raw.shape} \n')
print('  info : \n',TRC_raw.info())

TRC_raw.head(n=20)

TRC_raw.tail()

## Find a row number where data part starts
# save the column as a series
# test
print( TRC_raw[0][0] )
print( TRC_raw[0][1] )
TRC_raw_series = TRC_raw[0]
print(f'type(TRC_raw_series) : {type(TRC_raw_series)}')

# everylines of the header of CAN tracef file starts with " ; "
len_TRC_raw_series = len(TRC_raw_series)
row_data_start=0
for i in range(0, len_TRC_raw_series + 1):
    if TRC_raw_series[i].find(';') == -1:
        row_data_start = i
        break
print('row_data_start : ', row_data_start)


# ### Let's save the header

# save the header part of entire raw data as a series
TRC_header = TRC_raw[0][0:row_data_start]
print(f'type(TRC_header) : {type(TRC_header)}')
TRC_header

# ### Let's extract a vector of column names from the header
# Row 10~12 is column name of the data
#
# ;-------------------------------------------------------------------------------
# ;   Message   Time    Bus  Type   ID    Reserved
# ;   Number    Offset  |    |      [hex] |   Data Length Code
# ;   |         [ms]    |    |      |     |   |    Data [hex] ...
# ;   |         |       |    |      |     |   |    |
# ;---+-- ------+------ +- --+-- ---+---- +- -+-- -+ -- -- -- -- -- -- --

# +
# test
a=TRC_header[10]
print(f'type(a) : {type(a)}')
a_split = a.split()
print(f'a.split() : {a.split()}')
print(f'type(a_split) : {type(a_split)}')
print('- '*20)





# +
# Let's start now!
# I am going to use a nested list (a list of a list)
column_name_start = 10
column_name_end = 12
Column_Name_split = [];

for i in range(column_name_start, column_name_end+1):
    #print(f'TRC_header[{i}].split : {TRC_header[i].split()}')
    TRC_header[i] = TRC_header[i].replace('|','')
    TRC_header[i] = TRC_header[i].replace(';','')
    Column_Name_split.append(TRC_header[i].split() )

print('----- Split Result')    
for i in range(0, column_name_end-column_name_start+1):
    print(Column_Name_split[i])

print('- '*20)
print(f'type : {type(Column_Name_split)}')
print(f'shape : {len(Column_Name_split)}')
print('- '*20)

Column_Name=[]
Column_Name.append(''.join( [ Column_Name_split[0][0], ' ', Column_Name_split[1][0] ]))  #Message Number
Column_Name.append(''.join( [ Column_Name_split[0][1], ' ', Column_Name_split[1][1] ]))  # Time Offset
Column_Name.append(Column_Name_split[0][2] ) # Bus
Column_Name.append(Column_Name_split[0][3])  # Type
Column_Name.append(Column_Name_split[0][4])  # ID
Column_Name.append(Column_Name_split[0][5])  # Reserved
Column_Name.append(''.join ( [ Column_Name_split[1][3], ' ', Column_Name_split[1][4], ' ', Column_Name_split[1][5]]))  # Data Length Code
Column_Name.append(Column_Name_split[2][1])

print('----- Manually Combine Words for Column Name - Result')
print(f'Column_Name : {Column_Name}')





# # Let's use Numpy Array instead of nested list
# import numpy as np
# Column_Name=np.array(TRC_header[column_name_start].split())
# print('Column_Name 2 (ndarray): ',Column_Name)
# print(f'type : {type(Column_Name)}')
# print(f'shape : {np.shape(Column_Name)}')
# # print(f'np.shape(Column_Name)[0] : {np.shape(Column_Name)[0]}')
# # print(f'len(TRC_header[11].split()) : {len(TRC_header[11].split())}')

# for i in range(column_name_start+1, column_name_end+1):
#     temp_list = TRC_header[i].split()
#     if np.shape(Column_Name)[0] < len(temp_list)
        
#     else
#         Column_Name  = np.append(Column_Name, )

    


# print('Column_Name 3: ',Column_Name)
# print(f'type : {type(Column_Name)}')
# print(f'shape : {np.shape(Column_Name)}')

# print(TRC_header[10].split())
# print(TRC_header[11].split())




# +
# Save the date in the header
# check how long it has been since the data was collected

print('. . ' * 7)
# date stamp
import datetime

row_date = 0
for i in range(0, row_data_start):
    if TRC_header[i].find('Start time') != -1:
        row_date = i
        break
# ;   Start time: 6/30/2021 14:59:35.673.6
# 0123456789012345678901234567890123456789
# print(f'TRC_list[row_date][15:25] : {TRC_list[row_date][15:25]}')
trc_date_year = int(TRC_header[row_date][21:25])
trc_date_month = int(TRC_header[row_date][15:17])
trc_date_day = int(TRC_header[row_date][18:20])
trc_date_hour = int(TRC_header[row_date][26:28])
trc_date_min = int(TRC_header[row_date][29:31])
trc_date_sec = int(TRC_header[row_date][32:34])
print(
    f'year/month/day hour:min:sec = {trc_date_year} / {trc_date_month} / {trc_date_day}  {trc_date_hour} : {trc_date_min} : {trc_date_sec}')
trc_date = datetime.datetime(trc_date_year, trc_date_month, trc_date_day, trc_date_hour, trc_date_min, trc_date_sec)
print(f'This data was collected {trc_date}')
print(f'It has been {trc_date.today() - trc_date}')
# -

# ## Let's read *.trc file again with  attributes
#
# ;   Message   Time    Bus  Type   ID    Reserved
# ;   Number    Offset  |    |      [hex] |   Data Length Code
# ;   |         [ms]    |    |      |     |   |    Data [hex] ...
# ;   |         |       |    |      |     |   |    |
# ;---+-- ------+------ +- --+-- ---+---- +- -+-- -+ -- -- -- -- -- -- --
#      1)         0.115 1  Rx    1CEBF900 -  8    46 E7 0A 3F 8E 7B 80 00
#      2)         0.413 1  Rx    1CEBF900 -  8    47 00 1A C0 42 C7 F8 8A
#      3)         0.413 1  Rx    1CEFF900 F9 497  81 00 03 03 00 00 10 01 E8 00 00 1A E0 00 00 19 00 FF FF FE 1E 00 0B 41 97 EB 1D 00 00 00 00 21 7A 1D B0 00 00 0E 00 0E 00 00 00 19 00 00 02 FF D8 00 00 C0 00 00 05 FF A0 00 0B 05 DC 00 00 FF F8 50 00 FF 4B 49 40 FF F8 50 00 00 00 00 00 00 00 1A 90 00 00 4D BC 00 00 FF FF FF 6D 00 45 43 55 00 00 10 BD 3F D4 D1 6C 1E DE 32 00 25 80 41 97 EB 1D 00 9D E7 0A 3F 5B 61 00 00 00 1A E0 42 C7 75 5E 00 00 1A CC 00 00 19 00 FF FF FE 22 00 0B 41 97 DA 1E 00 00 00 00 21 8E 1D 4C 00 00 0E 00 0E 00 00 00 19 00 00 02 FF D8 00 00 C0 00 00 05 FF A0 00 0B 05 DC 00 00 FF F8 B0 00 FF 4C C9 40 FF F8 B0 00 00 00 00 00 00 00 1A 90 00 00 4D BF 00 00 FF FF FF 75 00 45 4B 31 00 00 10 C7 3F D4 F2 CD 1E DE 32 00 25 80 41 97 DA 1E 00 9D E7 0A 3F 8E 7B 80 00 00 1A C0 42 C7 F8 8A 00 00 1A C3 00 00 19 00 FF FF FE 3A 00 0B 41 99 39 4F 00 00 00 00 22 18 1D 4C 00 00 0E 00 0E 00 00 00 19 00 00 02 FF D8 00 00 C0 00 00 05 FF A0 00 0B 05 DC 00 00 FF FA F0 00 FF 55 C8 C0 FF FA F0 00 00 00 00 00 00 00 1A 90 00 00 4D BF 00 00 FF FF FF 9F 00 45 B5 30 00 00 11 0C 3F D4 AF 20 1E DE 32 00 25 80 41 99 39 4F 00 9D E7 0A 3F 01 F1 00 00 00 1A C0 42 C6 C2 7E 00 00 1A C8 00 00 19 00 FF FF FE 3C 00 0B 41 99 4F 32 00 00 00 00 22 20 1D B0 00 00 0E 00 0E 00 00 00 19 00 00 02 FF D8 00 00 C0 00 00 05 FF A0 00 0B 05 DC 00 00 FF FB 20 00 FF 56 88 C0 FF FB 20 00 00 00 00 00 00 00 1A 90 00 00 4D BC 00 00 FF FF FF A3 00 45 B7 45 00 00 11 10 3F D4 A0 8F 1E D6 32 00 25 80 41 99 4F 32 00 9D E7 0A 3F 8E 7B 80 00 00 1A C0 42 C7 F8 8A
#      4)         1.615 1  Rx    1CEC00F9 -  8    13 F1 01 47 FF 00 EF 00
#      5)         1.645 1  Rx    18ECF900 -  8    11 02 01 FF FF 00 EF 00
#      6)         1.675 1  Rx    18FEF100 -  8    DF FF FF C0 00 00 00 C0
#      7)         1.907 1  Rx    0CF00400 -  8    40 88 90 C9 1A 00 04 90
#      8)         2.558 1  Rx    18EB00F9 -  8    01 81 00 A3 00 00 13 34
#      9)         2.573 1  Rx    18EB00F9 -  8    02 60 05 98 1C 00 02 FF

# +
TRC_read = pd.read_csv(can_trc_file_location
                       , sep = ' '
                       #, delimiter = ' '
                       , header = None
                       , names = Column_Name
                       , index_col = False
                       , engine = 'python'
                       , skipinitialspace = True
                       , skiprows = row_data_start
                       , na_filter = False
                       , compression = None
                       , error_bad_lines = False
                       , warn_bad_lines = True 
                       #, delim_whitespace=True
                      )

# header : since this CAN trace file has multiple header rows, I extracted a column name vector from the rows.
# index_col : "Message Number" column is same as index but it is expresed as 1), 2), 3).... 
#              So, I will not use it as an index
# engine : python, not C
# skiprows : skip the header rows to read only data part without header rows
# na_filter : since there is no NA values in CAN trace file, I set this to False to improve performance of reading
# compression : we are not using on-the-fly decompression
# error_bad_lines : let's drop bad lines 
# warn_bad_lines : but have warnings for bad lines
# delim_whitespace : the seperator of CAN trace file is space, so set this to True
# skipinitialspacebool : Skip spaces after delimiter


print('  read CAN trace file(----.trc) completed \n')
print(' type : ',type(TRC_read)) #dataframe
print(f'  size : {TRC_read.shape} \n')
print('  info : \n',TRC_read.info())

TRC_read.head(n=10)
# damn... Data bytes were not read except 1st data byte




# -

# ### Let's save data bytes to another data frame
#  - How to handle multipacket bytes? 
#  
#    we already saved the whole trc file as a string
#   
#  

TRC_raw[0][row_data_start:row_data_start+5]


# Let's create a series which contains only data bytes"
TRC_data_only = TRC_raw[0][row_data_start:]
print(f'type of TRD_data_only : {type(TRC_data_only)}')
TRC_data_only.head()


# +
# Let's cut out non-data part
print(f'first row :\n{TRC_data_only.iloc[0]}')
len_non_data = len('     1)         0.115 1  Rx    1CEBF900 -  8    ')
print(f'Length of non-data characters : {len_non_data} ')

len_data_rows = len(TRC_data_only)
print(f'number of rows of data part : {len_data_rows}')
print(f'len_TRC_raw_series : {len_TRC_raw_series}')
print(f'row_data_start : {row_data_start}')

#test
# print(f'fifth row : \n{ TRC_data_only.iloc[5] }')
# print(f'slice the fifth row : \n{TRC_data_only.iloc[5][len_non_data:] }')


for i in range(0,len_data_rows+1):
    TRC_data_only[i]= TRC_data_only.iloc[i][len_non_data:]

# +
# make sure multi packets are not missing 
TRC_data_only.head(15)

# Now let's replace the "data" column with this series
TRC_read['Data'] = TRC_data_only
TRC_read.head()

# -

#check single packet 
TRC_read['Data'][0]

#check double packet 
TRC_read['Data'][2]

# ### Now data pre-processing has been completed !!
#
# ## Let's plot 
#
# Try this first : Plot Engine Speed 
#     PGN 61444, SPN 190 (SP position in PG : 4~5 , length : 2bytes, scaling : 0.125 rpm, offset : 0 rpm)
#
# Try this later :  Plot with an input of SPN ( find its PGN, start position, length, scaling, offset from J1939DA)
#
# ### I need to filter the data with a given SPN

# +
# Filtering
import numpy as np

PGN_1_dec = 61444
PGN_1_source_address = 0
PGN_1_source_address_hex = hex(PGN_1_source_address)[2:].upper().zfill(2)
# print(f'PGN_1_source_address_hex : {PGN_1_source_address_hex}')
# SPN_1 = 644
SPN_1_start_byte = 4
SPN_1_start_bit = 1
SPN_1_length_bit = 16 # 2 bytes
SPN_1_scale = 0.125
SPN_1_offset = 0
PGN_1_hex = hex(PGN_1_dec)[2:].upper().zfill(4) # remove "0x", make all the alphabets capitals 
# print(f'PGN_1_hex : {PGN_1_hex}')

#test 
# print('-- test --')
# print(TRC_read['ID'][42])  #1CEBF900
# print(TRC_read['ID'][42][2:6]) #PGN
# print(TRC_read['ID'][42][6:8]) #Source Address
# print(TRC_read['ID'][42][2:6].find(PGN_1_hex) != -1)
# print(TRC_read['ID'][42][6:8].find(PGN_1_source_address_hex) != -1)

# print(type(TRC_read['ID'][0]))
# print(len_data_rows)
# print(str(TRC_read))
# Create a vector for boolean indexing. I am going to filter the data with boolean indexing

FilterByPGN_1 =np.zeros((len_data_rows,1),dtype=bool)
# print(len(FilterByPGN_1))
for i in range(1, len_data_rows):
    FilterByPGN_1[i] = (TRC_read['ID'][i][2:6].find(PGN_1_hex) != -1 ) & (TRC_read['ID'][i][6:8].find(PGN_1_source_address_hex) != -1)


DF_PGN_1 = TRC_read[FilterByPGN_1]
print(str(DF_PGN_1))

