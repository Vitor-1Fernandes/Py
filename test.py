from scipy.stats import *
import pandas as pd


def scipyTests(dataset: str, columns:list[int] = None, alpha: float=0.05, criteria:list = 0, alternative:str = None, greaterOrLess:str = None) ->None:

    """ Verify normality, analyse variety and try hypotesiss test"""

    df = pd.read_csv(dataset)
    columnsName = df.columns.to_list()

    # Split group
    col1 = columnsName[columns[0]-1]
    # Calculate mean
    col2 = columnsName[columns[1]-1]

    # Set group flag splitter
    if alternative == 'num':
        dfGroup1 = df[df[col1] > criteria[0]]
        dfGroup2 = df[df[col1] < criteria[0]]

    elif alternative == 'str':
            dfGroup1 = df[df[col1] == criteria[0]]
            dfGroup2 = df[df[col1] == criteria[1]]

    print(f'\nSimple Means (Not valid for comparison)\n \n dfGroup1 = {dfGroup1[col2].mean()} \n dfGroup2 = {dfGroup2[col2].mean()} \n')
# ______________________________________________________________________________________________________________________________________

# Set distribuition using shapiro

    test, pShapiro1 = shapiro(dfGroup1[col2])
    test, pShapiro2 = shapiro(dfGroup2[col2])
    
    dist = 'normal' if pShapiro1 > alpha and pShapiro2 > alpha else 'not normal'

# Set variety using levene 

    test, pLevene = levene(dfGroup1[col2], dfGroup2[col2])

    variety = 'Homocedástica' if pLevene > alpha else 'Heterocedástica'
# ______________________________________________________________________________________________________________________________________

# Set test method based on previous results


    if dist == 'normal':

        if variety == 'Homocedástica':
            return print(f'Distribuition {dist} and Variety {variety} (Use ttest_ind) \n\nIs H0 refusable? {"Yes" if ttest_ind(dfGroup1[col2], dfGroup2[col2], alternative=greaterOrLess)[1] < alpha else "No"}')

        if variety == 'Heterocedástica': 
            return print(f'Distribuition {dist} and Variety {variety} (Use ttest_ind(equal_var=False)) \n\nIs H0 refusable? {"Yes" if ttest_ind(dfGroup1[col2], dfGroup2[col2], alternative=greaterOrLess, equal_var=False)[1] < alpha else "No"}')


    if dist == 'not normal':
            return print(f'Distribuition {dist} and Variety {variety} (Use mannwhitneyu) \n\nIs H0 refusable? {"Yes" if mannwhitneyu(dfGroup1[col2], dfGroup2[col2], alternative=greaterOrLess)[1] < alpha else "No"}  \n')
     

#_______________________________________________________________________________________________________________________________________

# H0 = Older (> 7) moldems doesn't have more lights blinking
# H1 = Older (> 7) moldems have less more blinking

# scipyTests('dataset_wifi_alien.csv', columns=[2, 3], criteria=[7], alternative='num', greaterOrLess='greater')

# H0 = Older (> 7) moldems doesn't have less lights blinking
# H1 = Older (> 7) moldems have less lights blinking

# scipyTests('dataset_wifi_alien.csv', columns=[2, 3], criteria=[7], alternative='num', greaterOrLess='less')

# H0 = Cat lovers (> 2 cats in house) doesn't have less lights blinking
# H1 = Cat lovers (> 2 cats in house) moldems have less lights blinking

# scipyTests('dataset_wifi_alien.csv', columns=[5, 3], criteria=[2], alternative='num', greaterOrLess='less')

# H0 = Cat lovers (> 2 cats in house) doesn't have more lights blinking
# H1 = Cat lovers (> 2 cats in house) moldems have more lights blinking

# scipyTests('dataset_wifi_alien.csv', columns=[5, 3], criteria=[2], alternative='num', greaterOrLess='greater')

# H0 = Pink cable doesn't have more lights blinking than Blue Cable
# H1 = Pink cable have more lights blinking than Blue Cable
# scipyTests('dataset_wifi_alien.csv', columns=[7, 3], criteria=['rosa','azul'], alternative='str', greaterOrLess='greater')

# H0 = Pink cable doesn't have less lights blinking than Blue Cable
# H1 = Pink cable have less lights blinking than Blue Cable
scipyTests('dataset_wifi_alien.csv', columns=[7, 3], criteria=['rosa','azul'], alternative='str', greaterOrLess='less')
