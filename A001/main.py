import requests
import pandas as pd

url = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbz8vTxNDRy9_Y2NQ13CDA0sTIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN_FydLAGAgNTKEK8DkRrACPGwpyQyMMMj0VAcySpRM!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K85260Q5OIRSC42046/res/id=historicoHTML/c=cacheLevelPage/=/'

r = requests.get(url)

df = pd.read_html(r.text)
df = df[0].copy()

n_available = list(range(1, 26))
n_even = list(range(2, 26, 2))
n_odd = list(range(1, 26, 2))
n_prime = [2, 3, 5, 7, 11, 13, 17, 19, 23]

combinations = []

n_01 = 0
n_02 = 0
n_03 = 0
n_04 = 0
n_05 = 0
n_06 = 0
n_07 = 0
n_08 = 0
n_09 = 0
n_10 = 0
n_11 = 0
n_12 = 0
n_13 = 0
n_14 = 0
n_15 = 0
n_16 = 0
n_17 = 0
n_18 = 0
n_19 = 0
n_20 = 0
n_21 = 0
n_22 = 0
n_23 = 0
n_24 = 0
n_25 = 0

fields = [
    'Bola1',  'Bola2',  'Bola3',  'Bola4',  'Bola5',
    'Bola6',  'Bola7',  'Bola8',  'Bola9',  'Bola10',
    'Bola11', 'Bola12', 'Bola13', 'Bola14', 'Bola15'
]

for index, row in df.iterrows():
    even = 0
    odd = 0
    prime = 0

    for field in fields:
        if row[field] in n_even:
            even += 1
        if row[field] in n_odd:
            odd += 1
        if row[field] in n_prime:
            prime += 1
        if row[field] == 1:
            n_01 += 1
        if row[field] == 2:
            n_02 += 1
        if row[field] == 3:
            n_03 += 1
        if row[field] == 4:
            n_04 += 1
        if row[field] == 5:
            n_05 += 1
        if row[field] == 6:
            n_06 += 1
        if row[field] == 7:
            n_07 += 1
        if row[field] == 8:
            n_08 += 1
        if row[field] == 9:
            n_09 += 1
        if row[field] == 10:
            n_10 += 1
        if row[field] == 11:
            n_11 += 1
        if row[field] == 12:
            n_12 += 1
        if row[field] == 13:
            n_13 += 1
        if row[field] == 14:
            n_14 += 1
        if row[field] == 15:
            n_15 += 1
        if row[field] == 16:
            n_16 += 1
        if row[field] == 17:
            n_17 += 1
        if row[field] == 18:
            n_18 += 1
        if row[field] == 19:
            n_19 += 1
        if row[field] == 20:
            n_20 += 1
        if row[field] == 21:
            n_21 += 1
        if row[field] == 22:
            n_22 += 1
        if row[field] == 23:
            n_23 += 1
        if row[field] == 24:
            n_24 += 1
        if row[field] == 25:
            n_25 += 1

    combinations.append(str(even) + '-e' + str(odd) + '-o' + str(prime) + '-p')
