import pandas as pd
dict = {
    'Name':['Priyang', 'Aadhya', 'Krisha', 'Vedant', "parshv", 'Mittal', 'Archana'],
    'Marks':[98, 89, 99, 87, 90, 83, 99],
    'Gender':["Male", "Female", 'Female', 'Male', 'Male', 'Female', 'Female']
    }

ds = pd.DataFrame(dict)


# 1. Display top 3 rows of the dataset
print(ds.head(3))

# 2. Display last 3 rows of the dataset
print(ds.tail(3))

# 3. Find shape of our dataset (Number os rows and Number of columns)
print("Number fo Rows : ", ds.shape[0])
print("Number fo Columns : ",ds.shape[1])
print('\n')

# 4. Get information about our dataset like Total numbers of rows, Total number of columns,
# Datatypes of each column and memory requirements.
print(ds.info())

# 5. Check null values in the dataset

print(ds.isnull())
print('\n')
# It calculate the null value
print(ds.isnull().sum())
print('\n')
# Null value count coloumn wise
print(ds.isnull().sum(axis=0))
print('\n')
# Null value count row wise
print(ds.isnull().sum(axis=1))
print('\n')

# 6. Get overall statistics about the dataframe.
print(ds.describe())
print('\n')
print(ds.describe(include='all'))

# 7. Find unique values from the gender column
print(ds['Gender'].unique())

# 8. Find the number fo unique values from the gender column
print(ds['Gender'].nunique())

# 9. Display count of unique values in gender column
print(ds['Gender'].value_counts())

# 10 . Find total number of students having marks between 90 to 100 using between method
print(ds[ds['Marks']>=90])
print('\n')
print(ds[(ds['Marks']>=90) and (ds['Marks']<=100)]) 