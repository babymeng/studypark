#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def ml_test1():
    #read data from html,ftp,file.
    california_housing_dataframe = pd.read_csv("california_housing_train.csv", sep=",")

    #statistic mean,std,min,max and so on.
    ret = california_housing_dataframe.describe()
    
    print(california_housing_dataframe.head())

    #generate diagram
    california_housing_dataframe['housing_median_age'].hist()

    #show diagram
    plt.show()

    population = california_housing_dataframe['population'].describe()
    print(population)
def ml_test():
    '''
    Pandas practice
    '''
    citys = ['San Francisco', 'San Jose', 'Sacramento']
    num   = [852469, 1015785, 485199]
    
    city_names = pd.Series(citys)
    population = pd.Series(num)
    print(population.apply(lambda val: val%val))

    print(np.log(population))

    print(city_names)
    print(population)

    cities = pd.DataFrame({'City names':city_names, 'Population':population})
    print(cities, '\n')
    print(cities['City names'], '\n')

    cities['Area square miles'] = pd.Series([46.87, 176.53, 97.92])
    cities['Population density'] = cities['Population'] / cities['Area square miles']

    print(cities)

    cities['Is wide and has saint name'] = (cities['Area square miles'] > 50) & cities['City names'].apply(lambda name: name.startswith('San'))

    print(cities)

    

if __name__ == '__main__':
    ml_test1()
