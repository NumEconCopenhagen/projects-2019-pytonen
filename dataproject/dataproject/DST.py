#IMPORT PACKAGES  
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pydst
pd.set_option("display.max_columns", None) # To see all columns

dst = pydst.Dst(lang='en')

#IMPORT DATA FROM DST 
Emp = dst.get_data(table_id = 'RAS201', variables={'OMRÅDE':['*'], 'TID':['*'], 'ALDER':['*'], 'HERKOMST': ['*'], 'KØN': ['*'], 'SOCIO': ['*']})

#DELETE COLUMNS THAT WE DON'T NEED AND RENAME VARIABLES
for v in ['ALDER', 'KØN', 'HERKOMST']: 
    del Emp[v]
Emp = Emp.rename(columns = {'TID':'Year', 'OMRÅDE': 'Region', 'SOCIO': 'Status', 'INDHOLD': 'Number of Persons'})


# DELETE ROWS THAT ARE NOT REGIONS 
I = Emp['Region'].str.contains(r'^(?:(?!Region|All Denmark).)*$') #Finds rows that does not contain Region or All Denmark
Emp.drop(Emp[I].index, inplace=True)    
print(Emp)


# AGGRATE DATA TO REGION PER YEAR PER STATUS 
Agg_Emp=Emp.groupby(['Region', 'Year', 'Status'])['Number of Persons'].sum().reset_index()
Agg_Emp.head()



# Create line chart for Regions and All Denmark
TOT=Agg_Emp.groupby(['Region', 'Year'])['Number of Persons'].sum()

Status_Emp = Agg_Emp['Status'] == 'Employed'
Status_Emp.head()

TOT_Emp = Agg_Emp 

Joined = pd.merge(TOT_Emp.reset_index(), TOT.reset_index(),how = 'inner', on = ['Region', 'Year'])
print(Joined)
