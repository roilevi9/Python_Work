import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import numpy as np

#tips = sns.load_dataset('tips')
#print(tips.head())

# Create a Seaborn plot
# sns.displot(tips.total_bill, bins= 20)
# plt.show()

# עושה מספר גרפים, כל גרף הוא בדיקת קורלציה בין שדה למשנהו
#sns.pairplot(tips)

#sns.regplot(data=tips, x="total_bill",y='tip')

#sns.lmplot(data=tips, x="total_bill",y='tip', col='time', hue='sex')

#sns.lmplot(data=tips, x="total_bill",y='tip', hue='smoker')

#sns.lmplot(data=tips, x="total_bill",y='tip', hue='day')

#sns.catplot(data=tips, kind='bar', x='day', y="total_bill")

#sns.catplot(data=tips, kind='bar', x='day', y="total_bill", hue='smoker')

#sns.countplot(data=tips, x='smoker')

#sns.countplot(data=tips, x='sex')

#sns.barplot(data=tips, x='smoker', y="total_bill")

#sns.boxplot(data=tips, x='smoker', y="total_bill")

#sns.boxplot(data=tips, x='smoker', y="total_bill", hue='sex')

#sns.violinplot(data=tips, x='day', y='total_bill')

#sns.violinplot(data=tips, x='day', y="total_bill", hue='smoker', split=True)
#plt.show()


#penguins = sns.load_dataset('penguins')
#print(penguins.shape)
#penguins.dropna(inplace=True)
#print(penguins.head())
#print(penguins.shape)
#print()
#flipper_value_by_bill = penguins.pivot_table(values="flipper_length_mm",
#                                             index='bill_length_mm',
#                                             columns='bill_depth_mm')
#print(flipper_value_by_bill)

# sns.heatmap(flipper_value_by_bill)
# plt.show()

#total_bill_by_sex_smoker = tips.pivot_table(values="total_bill",
#                                            index='sex',
#                                            columns='smoker')
#print(total_bill_by_sex_smoker)
# sns.heatmap(total_bill_by_sex_smoker, cmap='coolwarm')
# plt.show()

# Data Cleaning - dummies
# df = pd.DataFrame({'height': [1.80, 1.70, 1.77, 1.90],
#                    'speed': [8, 4, 7, 9],
#                    'age': [12, 55, 24, 30],
#                    'country': ['Israel', 'Brazil', 'England', 'Greece'],
#                    'basketball_level': [4, 5, 7, 9]})
# country = pd.get_dummies(df['country'])
# print(df, "\n", country)
# df = pd.concat([df, country], axis=1)
# df.drop(['country'], inplace=True, axis=1)
# print(df)

data = pd.read_csv('Ecommerce Customers.csv')
print(data.columns, "\n")
# print(data.head(), "\n")
#
# print(data.describe())

# sns.pairplot(data)
# plt.show()

non_numeric_columns = data.select_dtypes(exclude='number').columns
#print(non_numeric_columns)

numeric_data = data.select_dtypes(include='number')
correlation_matrix = numeric_data.corr()
#print(correlation_matrix)
#sns.heatmap(correlation_matrix)
# plt.show()

regressor = LinearRegression()
x = data[['Avg. Session Length', 'Time on App',  'Time on Website', 'Length of Membership']]
y = data['Yearly Amount Spent']
#print(x, "\n", y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
# print('x train: ', x_train.shape, '\n', 'y train: ', y_train.shape)
# print('x test: ', x_test.shape, '\n', 'y test: ', y_test.shape)
# print(data.corr())
regressor.fit(x_train, y_train)

y_pred = regressor.predict(x_test)
#print(y_pred)
# sns.regplot(y_test, y_pred)
# plt.show()

mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
# print(rmse)
#
# print(regressor.coef_)

df = pd.DataFrame(['Avg. Session Length', 'Time on App',  'Time on Website', 'Length of Membership'], regressor.coef_, columns=['feature'])
print(df)
