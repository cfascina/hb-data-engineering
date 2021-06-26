import collections
import requests
import pandas as pd
import sys

# url = 'http://loterias.caixa.gov.br/wps/portal/loterias/landing/lotofacil/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOLNDH0MPAzcDbz8vTxNDRy9_Y2NQ13CDA0sTIEKIoEKnN0dPUzMfQwMDEwsjAw8XZw8XMwtfQ0MPM2I02-AAzgaENIfrh-FqsQ9wBmoxN_FydLAGAgNTKEK8DkRrACPGwpyQyMMMj0VAcySpRM!/dl5/d5/L2dBISEvZ0FBIS9nQSEh/pw/Z7_HGK818G0K85260Q5OIRSC42046/res/id=historicoHTML/c=cacheLevelPage/=/'
url = sys.argv[1]

r = requests.get(url)

df = pd.read_html(r.text)
df = df[0].copy()

n_available = list(range(1, 26))
n_even = list(range(2, 26, 2))
n_odd = list(range(1, 26, 2))
n_prime = [2, 3, 5, 7, 11, 13, 17, 19, 23]

combinations = []
occurrences = {
    '01': 0,
    '02': 0,
    '03': 0,
    '04': 0,
    '05': 0,
    '06': 0,
    '07': 0,
    '08': 0,
    '09': 0,
    '10': 0,
    '11': 0,
    '12': 0,
    '13': 0,
    '14': 0,
    '15': 0,
    '16': 0,
    '17': 0,
    '18': 0,
    '19': 0,
    '20': 0,
    '21': 0,
    '22': 0,
    '23': 0,
    '24': 0,
    '25': 0
}
fields = [
    'Bola1',
    'Bola2',
    'Bola3',
    'Bola4',
    'Bola5',
    'Bola6',
    'Bola7',
    'Bola8',
    'Bola9',
    'Bola10',
    'Bola11',
    'Bola12',
    'Bola13',
    'Bola14',
    'Bola15'
]

for index, row in df.iterrows():
    o_even = 0
    o_odd = 0
    o_prime = 0

    for field in fields:
        if row[field] in n_even:
            o_even += 1
        if row[field] in n_odd:
            o_odd += 1
        if row[field] in n_prime:
            o_prime += 1
        if row[field] == 1:
            occurrences['01'] += 1
        if row[field] == 1:
            occurrences['01'] += 1
        if row[field] == 2:
            occurrences['02'] += 1
        if row[field] == 3:
            occurrences['03'] += 1
        if row[field] == 4:
            occurrences['04'] += 1
        if row[field] == 5:
            occurrences['05'] += 1
        if row[field] == 6:
            occurrences['06'] += 1
        if row[field] == 7:
            occurrences['07'] += 1
        if row[field] == 8:
            occurrences['08'] += 1
        if row[field] == 9:
            occurrences['09'] += 1
        if row[field] == 10:
            occurrences['10'] += 1
        if row[field] == 11:
            occurrences['11'] += 1
        if row[field] == 12:
            occurrences['12'] += 1
        if row[field] == 13:
            occurrences['13'] += 1
        if row[field] == 14:
            occurrences['14'] += 1
        if row[field] == 15:
            occurrences['15'] += 1
        if row[field] == 16:
            occurrences['16'] += 1
        if row[field] == 17:
            occurrences['17'] += 1
        if row[field] == 18:
            occurrences['18'] += 1
        if row[field] == 19:
            occurrences['19'] += 1
        if row[field] == 20:
            occurrences['20'] += 1
        if row[field] == 21:
            occurrences['21'] += 1
        if row[field] == 22:
            occurrences['22'] += 1
        if row[field] == 23:
            occurrences['23'] += 1
        if row[field] == 24:
            occurrences['24'] += 1
        if row[field] == 25:
            occurrences['25'] += 1

    combinations.append(\
        'Even: ' + str(o_even) + \
        ' / Odd: ' + str(o_odd) + \
        ' / Prime: ' + str(o_prime))

n_freq = [
    ['01', occurrences['01']],
    ['02', occurrences['02']],
    ['03', occurrences['03']],
    ['04', occurrences['04']],
    ['05', occurrences['05']],
    ['06', occurrences['06']],
    ['07', occurrences['07']],
    ['08', occurrences['08']],
    ['09', occurrences['09']],
    ['10', occurrences['10']],
    ['11', occurrences['11']],
    ['12', occurrences['12']],
    ['13', occurrences['13']],
    ['14', occurrences['14']],
    ['15', occurrences['15']],
    ['16', occurrences['16']],
    ['17', occurrences['17']],
    ['18', occurrences['18']],
    ['19', occurrences['19']],
    ['20', occurrences['20']],
    ['21', occurrences['21']],
    ['22', occurrences['22']],
    ['23', occurrences['23']],
    ['24', occurrences['24']],
    ['25', occurrences['25']]
]

n_freq.sort(key = lambda x: x[1])

counter = collections.Counter(combinations)
result = pd.DataFrame(counter.items(), columns = ['Combination', 'Frequency'])
result['Percentage'] = result['Frequency'] / result['Frequency'].sum()
result = result.sort_values(by = 'Percentage')

print('''
    Most frequent number: {}
    Less frequent number: {}
    Most frequent combination: {} ({}%)
'''.format(
    n_freq[-1][0],
    n_freq[-0][0],
    result['Combination'].values[-1],
    int((result['Percentage'].values[-1] * 100) * 100) / 100
    )
)
