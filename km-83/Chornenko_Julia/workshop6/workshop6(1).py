import re
import plotly
import plotly.graph_objs as go
from plotly import tools
nan=float('nan')

input_file='../filereader/vgsales.csv'

def getYear(line):
    result=re.split(r',', line, maxsplit=1)
    Year=re.findall(r'[1-3][0-9]{3}',result[0])
    return Year[0], result[1]

def getPlatform(line):
    result = re.split(r',', line, maxsplit=1)
    Platform=result[0].strip()
    return Platform, result[1]


def getName(line):
    result = re.split(r',', line, maxsplit=1)
    return result[0], result[1]

def getRank(line):
    result = re.split(r',', line, maxsplit=1)
    return result[0], result[1]

current_line=0
i = 0
try:

    with open(input_file, encoding="utf8", mode='r') as file:
        file.readline()
        line_number=1
        dataset={}
        for line in file:
            i+=1

            columns=line.split(',')
            
            Rank, line = getRank(line)
            Name, line = getName(line)
            Platform, line = getPlatform(line)
            try:
                Year, line = getYear(line)
            except IndexError:
                Year = 'Unknown'
            if Year not in list(dataset.keys()):
                dataset[Year]={}
                    
            if Platform not in list(dataset[Year].keys()):
                dataset[Year][Platform]=dict()

            if Name not in dataset[Year][Platform]:
                dataset[Year][Platform][Name] = Rank
#           print(dataset)
    print(dataset)
except IOError:
    print('Error with file', IOError.errno, IOError.strerror)
except ValueError:
    print('Error in line', current_line, ValueError)

input_file='../filereader/vgsales.csv'
with open(input_file, encoding="utf8", mode='r') as file:
    file.readline()

    count_of_game=dict()

    for line in file:
        columns = line.split(',')
        Name = columns[1]
        Year = columns[3]

        if Year not in count_of_game:
            count_of_game[Year]=list()
        if Name not in count_of_game[Year]:
            count_of_game[Year].append(Name)
    print(count_of_game)

v=-1
count=[]
while v!=541:
    v+=1
    count.append(len((count_of_game[Year])[v]))




print(count)
graph=[go.Scatter(x=list(count_of_game.keys()),
             y=count,
             name='Year - count of game')]

plotly.offline.plot(graph,filename="1.html")



with open(input_file, encoding="utf8", mode='r') as file:
    file.readline()

    platforms=list()

    for line in file:
        columns = line.split(',')
        Platform = columns[2]


        if Platform not in platforms:
            platforms.append(Platform)
    print(platforms)








