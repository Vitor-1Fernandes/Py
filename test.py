
"""O Mago mais Habilidoso é aquele com maior desempenho agregado, valor este a ser descoberto combinando precisão, potência, controle, dificuldade da tarefa, resistência do alvo, sucesso e penalizando dano colateral e tempo de execução na métrica única "soma_skills". Depois de somar essa métrica por mago, Albus Dumbledore e Severus Snape ficaram estatisticamente empatados no topo. Rodei um teste de hipótese comparando Snape e os demais (ciente de ~12% de erro acumulado, por isso usei apenas como triagem para identificar contra quem testar, não como prova estatística), o que apontou Dumbledore como único concorrente próximo. Para desempatar, apliquei um teste de hipótese comparando os dois em controle_pct, já que para desempate esta é a variável mais importante para saber se o mago tem habilidade o suficiente para controlar os efeitos produzidos. Ao verificar normalidade (Shapiro-Wilk) e homocedasticidade (Levene), o t-test rejeitou H0 (p=0,0067 < 0,01), confirmando Snape como o mais habilidoso"""


from scipy.stats import *
import pandas as pd

df = pd.read_csv('checkpoint_magos_dados.csv')
df["soma_skills"] = df["precisao_pct"] + df["potencia_pct"] + df["controle_pct"] + (df["dificuldade"] * 2) + df["resistencia_alvo"] + (df["sucesso"] * 10) - (df["dano_colateral"]*10)  - df["tempo_execucao_s"]

df.to_csv('1checkpoint_magos_dados.csv')

namesList2 = df['mago'].tolist()
namesList1 = df['mago'].tolist()

namesList = list(dict(zip(namesList1,namesList2)).keys())

dictCount = {}
for name in namesList:

    dfName = df[df['mago'] == name]
    soma_skill = int(dfName["soma_skills"].sum())

    dictCount[name] = soma_skill

# print(dfName)
# print(dictCount)

df.to_excel("salvar.xlsx")

def scipyTests(dataset: str, columns:list[int] = None, alpha: float=0.01, criteria:list = 0, alternative:str = None, greaterOrLess:str = None, printCol:bool = False) ->None:

    """ Verify normality, analyse variety and try hypotesiss test"""

    df = pd.read_csv(dataset)
    columnsName = df.columns.to_list()

    # Split group
    col1 = columnsName[columns[0]-1]
    # Calculate mean
    col2 = columnsName[columns[1]-1]

    print(f"\n {col1, col2}") if printCol else print("\n")

    # Set group flag splitter
    if alternative == 'num':
        dfGroup1 = df[df[col1] > criteria[0]]
        dfGroup2 = df[df[col1] < criteria[0]]

        print(dfGroup1)

    elif alternative == 'str':
            dfGroup1 = df[df[col1] == criteria[0]]
            dfGroup2 = df[df[col1] == criteria[1]]

    # print(f'\nSimple Means (Not valid for comparison)\n \n dfGroup1 = {dfGroup1[col2].mean()} \n dfGroup2 = {dfGroup2[col2].mean()} \n')
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
            # print(f'Distribuition {dist} and Variety {variety} (Use ttest_ind) \n\nIs H0 refusable? {"Yes" if ttest_ind(dfGroup1[col2], dfGroup2[col2], alternative=greaterOrLess)[1] < alpha else "No"}')
            
            # print(ttest_ind(dfGroup1[col2], dfGroup2[col2], alternative=greaterOrLess)[1])

            return True if ttest_ind(dfGroup1[col2], dfGroup2[col2], alternative=greaterOrLess)[1] < alpha else False

        if variety == 'Heterocedástica': 
            # print(f'Distribuition {dist} and Variety {variety} (Use ttest_ind(equal_var=False)) \n\nIs H0 refusable? {"Yes" if ttest_ind(dfGroup1[col2], dfGroup2[col2], alternative=greaterOrLess, equal_var=False)[1] < alpha else "No"}')

            # print(ttest_ind(dfGroup1[col2], dfGroup2[col2], alternative=greaterOrLess, equal_var=False)[1])

            return True if ttest_ind(dfGroup1[col2], dfGroup2[col2], alternative=greaterOrLess, equal_var=False)[1] < alpha else False


    if dist == 'not normal':
            # print(f'Distribuition {dist} and Variety {variety} (Use mannwhitneyu) \n\nIs H0 refusable? {"Yes" if mannwhitneyu(dfGroup1[col2], dfGroup2[col2], alternative=greaterOrLess)[1] < alpha else "No"}  \n')

            # print(mannwhitneyu(dfGroup1[col2], dfGroup2[col2], alternative=greaterOrLess)[1])

            return True if mannwhitneyu(dfGroup1[col2], dfGroup2[col2], alternative=greaterOrLess)[1] < alpha else False
     

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
# scipyTests('dataset_wifi_alien.csv', columns=[7, 3], criteria=['rosa','azul'], alternative='str', greaterOrLess='less')


for name in namesList:
    # H0 = Snape "soma_skill" is not greater than {name} 
    # H1 = Snape "soma_skill" is greater than {name} 
    print(f"For Snape vs {name} Is H0 refusable? {scipyTests('1checkpoint_magos_dados.csv', columns=[4, 18], criteria=['Severus Snape', name], alternative='str', greaterOrLess='greater')}")

# H0 = Snape "controle_pct" is not greater than Albus Dumbledore
# H1 = Snape "controle_pct" is greater than Albus Dumbledore

# It got a tie, using 'controle_pct' to break the untie
print(f"\n For Snape vs Albus Dumbledore Is H0 refusable? {scipyTests('1checkpoint_magos_dados.csv', columns=[4, 15], criteria=['Severus Snape', "Albus Dumbledore"], alternative='str', greaterOrLess='greater')}\n")