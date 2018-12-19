import re
import plotly
import plotly.graph_objs as go
from plotly import tools
from collections import Counter

nan = float('nan')

input_file = '../filereader/vgsales.csv'


def getYear(line):
    result = re.split(r',', line, maxsplit=1)
    Year = re.findall(r'[1-3][0-9]{3}', result[0])
    return Year[0], result[1]


def getPlatform(line):
    result = re.split(r',', line, maxsplit=1)
    Platform = result[0].strip()
    return Platform, result[1]


def getName(line):
    result = re.split(r',', line, maxsplit=1)
    return result[0], result[1]


def getRank(line):
    result = re.split(r',', line, maxsplit=1)
    return result[0], result[1]


current_line = 0
i = 0
try:

    with open(input_file, encoding="utf8", mode='r') as file:
        file.readline()
        line_number = 1
        dataset = {}
        for line in file:
            i += 1

            columns = line.split(',')

            Rank, line = getRank(line)
            Name, line = getName(line)
            Platform, line = getPlatform(line)
            try:
                Year, line = getYear(line)
            except IndexError:
                Year = 'Unknown'
            if Year not in list(dataset.keys()):
                dataset[Year] = {}

            if Platform not in list(dataset[Year].keys()):
                dataset[Year][Platform] = dict()

            if Name not in dataset[Year][Platform]:
                dataset[Year][Platform][Name] = Rank
    #           print(dataset)
    print(dataset)
except IOError:
    print('Error with file', IOError.errno, IOError.strerror)
except ValueError:
    print('Error in line', current_line, ValueError)

input_file = '../filereader/vgsales.csv'
with open(input_file, encoding="utf8", mode='r') as file:
    file.readline()

    count_of_game = dict()

    for line in file:
        columns = line.split(',')
        Name = columns[1]
        Year = columns[3]

        if Year not in count_of_game:
            count_of_game[Year] = list()
        if Name not in count_of_game[Year]:
            count_of_game[Year].append(Name)
    print(count_of_game)

v = -1
count = []
while v != 541:
    v += 1
    count.append(len((count_of_game[Year])[v]))

print(list(count_of_game.keys()))
print(count)
scat = go.Scatter(x=list(count_of_game.keys()),
                  y=count,
                  name='Year - count of game')

with open(input_file, encoding="utf8", mode='r') as file:
    file.readline()

    platforms = list()

    for line in file:
        columns = line.split(',')
        Platform = columns[2]

        platforms.append(Platform)
    print(platforms)

platforms1 = Counter(platforms)
print(platforms1)

pie = go.Pie(labels=list(platforms1.keys()),
             values=list(platforms1.values()))

with open(input_file, encoding="utf8", mode='r') as file:
    file.readline()

    rank = dict()

    for line in file:
        columns = line.split(',')

        Rank = columns[0]
        Platform = columns[2]

        if Platform not in rank:
            rank[Platform] = set()

        rank[Platform].add(float(Rank))
    print(rank)

max_rank = list()
for Platform in rank:
    maximum = max(rank[Platform])
    max_rank.append(maximum)
print(max_rank)

bar = go.Bar(x=list(rank.keys()),
             y=max_rank)

fig = tools.make_subplots(rows=2, cols=2)

fig.append_trace(bar, 1, 1)

fig.append_trace(pie, 1, 2)

fig.append_trace(scat, 2, 1)

plotly.offline.plot(fig, filename="myplotly.html")







