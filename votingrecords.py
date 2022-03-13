import wget
from os import path
import sys
import numpy as np
from numpy.polynomial.polynomial import polyfit
import matplotlib.pyplot as plt
##np.set_printoptions(threshold=sys.maxsize)
from mpl_toolkits.mplot3d import Axes3D as axe

url1 = r'https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/42MVDX/MFU99O'
fPathOne = r'C:\\Users\\jscud\\PycharmProjects\\Voting_Record_Analysis\\Information\\presidents.txt'
fPathTwo = r'C:\\Users\\jscud\\PycharmProjects\\Voting_Record_Analysis\\Information\\electoral_color.tsv'
fPathThree = r'C:\\Users\\jscud\\PycharmProjects\\Voting_Record_Analysis\\Information\\electoral_votes.tsv'

states = []
partys = []
years = []


##code commments coming soon, made early in code career, before i understood the importance

def setup():
    if not path.exists(fPathOne):
        wget.download(url1, fPathOne)


def tokenizer(token, string):
    arr_list = []
    i = -1
    n = 0
    for val in string:
        if val == token:
            if i == -1:
                i = n
                arr_list.append(string[:i])
            else:
                arr_list.append(string[(i + 1):n])
                i = n
        n += 1
    return arr_list


def naive(value, data):
    for track in data:
        if track == value:
            return True
    return False


def find_title(title, info):
    for x in range(0, len(info)):
        if title == info[x]:
            return x
    return -1


def collect_votes():
    votes = []
    text = list(open(fPathOne, 'r'))
    for val in range(0, len(text)):
        votes.append(tokenizer('\t', str(text[val])))
    bvoting_info = []
    for valx in range(0, len(votes)):
        vot = [votes[valx][0], votes[valx][2], votes[valx][8], votes[valx][10]]
        ##print(vot, valx, '/', len(votes)-1)
        bvoting_info.append(vot)
    for x in range(1, len(votes)):
        if not naive(bvoting_info[x][0], years):
            years.append(bvoting_info[x][0])
    ##print(years)
    for x in range(1, 3):
        if not naive(bvoting_info[x][2], partys):
            partys.append(bvoting_info[x][2])
    partys.append('Other')
    print(partys)
    for x in range(1, (len(votes))):
        if not naive(bvoting_info[x][1], states):
            states.append(bvoting_info[x][1])
    ##print(states)
    ##print(len(states))
    storage = np.zeros((len(partys), len(states), len(years)))
    ##print(storage)
    for val in range(1, len(bvoting_info)):
        x = 2
        y = find_title(bvoting_info[val][1], states)
        if not find_title(bvoting_info[val][2], partys) == -1:
            x = find_title(bvoting_info[val][2], partys)
        z = find_title(bvoting_info[val][0], years)
        storage[x][y][z] = storage[x][y][z] + int(bvoting_info[val][3])
    return storage


def threedim_plot(p1, p2):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    x = []
    for val in range(0, len(states)):
        x.append(val)
    z = years
    znum = 0
    for zz in z:
        z[znum] = int(zz)
        znum += 1
    anum = 0
    for xvalx in x:
        y = []
        for zval in range(0, len(z)):
            sto = 100 * (data[p1][xvalx][zval] / (data[p1][xvalx][zval] + data[p2][xvalx][zval]))
            y.append(sto)
        ax.plot([xvalx] * len(y), z, zs=y, marker='o', label=f'{states[xvalx]}={xvalx}')
        anum += 1
    plt.show()


def create_frame(y, x1, x2):
    for yearval in range(0, len(years)):
        years[yearval] = int(years[yearval])
    party1 = []
    party2 = []
    perc = []
    fig = plt.figure()
    for year in years:
        valx = find_title(year, years)
        party1.append(data[x1][y][valx])
        party2.append(data[x2][y][valx])
        perc.append((data[x1][y][valx] / (data[x1][y][valx] + data[x2][y][valx])) * 100)
    plt.ylim(0, 100)
    plt.fill_between(years, perc, [0] * len(years), color='b')
    plt.fill_between(years, perc, [100] * len(years), color='r')
    plt.ylabel('Percent Democrat vs republican')
    plt.xlabel('Presidential Election Year')
    plt.title(f'Percent Votes Democrat vs Republican in {states[y]}')
    plt.scatter(years, perc, c='k')
    '''
    ##data annotations, cut because of clutter
    for val in range(0, len(perc)):
        intinf = 5
        if val%2 == 1:
            intinf = -6
        plt.annotate(f'({years[val]}, {int(perc[val])}%D, {int(100 - perc[val])}%R)', xy=(years[val], perc[val]), xytext=(years[val], perc[val]+intinf))
    '''
    plt.plot(np.unique(years), np.poly1d(np.polyfit(years, perc, 1))(np.unique(years)),
             label=f'Best Fit Line \n {np.poly1d(np.polyfit(years, perc, 1))}', c='k')
    plt.show()
    plt.clf()
    plt.cla()
    plt.title(f'Number of Votes Democrat vs Republican in {states[y]}')
    plt.ylabel('Number of Votes')
    plt.xlabel('Presidential Election Year')
    plt.scatter(years, party1, c='b', label=f'{partys[x1]}')
    plt.plot(np.unique(years), np.poly1d(np.polyfit(years, party1, 1))(np.unique(years)),
             label=f'Best Fit Line: {partys[x1]} :\n {np.poly1d(np.polyfit(years, party1, 1))}', c='b')
    plt.scatter(years, party2, c='r', label=f'{partys[x2]}')
    plt.plot(np.unique(years), np.poly1d(np.polyfit(years, party2, 1))(np.unique(years)),
             label=f'Best Fit Line: {partys[x2]} :\n {np.poly1d(np.polyfit(years, party2, 1))}', c='r')
    plt.legend()
    plt.show()


def average(inf):
    return sum(inf) / len(inf)


def variance_analysis():
    for yearval in range(0, len(years)):
        years[yearval] = int(years[yearval])
    p1 = 0
    p2 = 1
    var2 = []
    var1 = []
    percinf = []
    for year in years:
        perc = []
        for y in range(0, len(states)):
            valx = find_title(year, years)
            perc.append((data[p1][y][valx] / (data[p1][y][valx] + data[p2][y][valx])) * 100)
        percinf.append(perc)
    ##yan stands for year analyis, san stadns for state analyisis
    avera = []
    for yan in percinf:
        ##print(yan)
        avera.append(average(yan))
    ##print(avera)
    averainf = []
    for year in years:
        avernum = 0
        ave = []
        for y in range(0, len(states)):
            valx = find_title(year, years)
            ave.append(abs(percinf[valx][y] - avera[valx]))
        ##print(ave)
        avernum = int((average(ave) / average(avera)) * 100)
        averainf.append(avernum)
    ##print(averainf)
    plt.scatter(years, averainf, label='Average State Percent deviation from average')
    plt.ylabel('Average difference in vote percent between states')
    plt.xlabel('Election Years')
    plt.plot(np.unique(years), np.poly1d(np.polyfit(years, averainf, 2))(np.unique(years)),
             label=f'Best Fit Line \n {np.poly1d(np.polyfit(years, averainf, 2))}', c='r')
    plt.legend()
    plt.show()


# def electoral_info():
#     text1 = list(open(fPathTwo, 'r'))
#     text2 = list(open(fPathThree, 'r'))
#     votese_num = []
#     votese_party = []
#     parties = ['dem', 'rep', 'ind']
#     for val in range(1, len(text1)):
#         votese_num.append(tokenizer('\t', str(text2[val])))
#         votese_party.append(tokenizer('\t', str(text1[val])))
#     ##print(votese_party)
#     for row in range(1, len(votese_party)):
#         for col in range(1, len(votese_party[0])):
#             ##print('dem, ', votese_party[row][col] == '#2437a3', 'rep', votese_party[col] == '#bf1520', votese_party[row][col])
#             if votese_party[row][col] == '#2437a3':
#                 votese_party[row][col] = 'dem'
#             elif votese_party[row][col] == '#bf1520':
#                 votese_party[row][col] = 'rep'
#             else:
#                 votese_party[row][col] = 'ind'
#         ##print(votese_party[row])
#         ##(votese_num[row])
#     stats = []
#     for val in range(0, len(votese_party)):
#         stats.append(votese_party[val][0])
#         del (votese_party[val][0])
#         del (votese_num[val][0])
#     ##print(stats)
#     stoele = np.zeros([len(states), len(parties), len(years)])
#     print(stoele)
#     for xvalxx in range(0, len(states)):
#         for zvalzz in range(0, len(years)):
#             if votese_party[xvalxx][zvalzz] == 'dem':
#                 stoele[xvalxx][0][zvalzz] = votese_num[xvalxx][zvalzz]
#                 stoele[xvalxx][1][zvalzz] = 0
#                 stoele[xvalxx][2][zvalzz] = 0
#             elif votese_party[xvalxx][zvalzz] == 'rep':
#                 stoele[xvalxx][0][zvalzz] = 0
#                 stoele[xvalxx][1][zvalzz] = votese_num[xvalxx][zvalzz]
#                 stoele[xvalxx][2][zvalzz] = 0
#             else:
#                 stoele[xvalxx][0][zvalzz] = 0
#                 stoele[xvalxx][1][zvalzz] = 0
#                 stoele[xvalxx][2][zvalzz] = votese_num[xvalxx][zvalzz]


data = collect_votes()
'''for state in range(0,len(states)):
    print(states[state])'''
y = find_title('\'MA\'', states)
create_frame(y, 0, 1)
threedim_plot(0, 1)
variance_analysis()
#electoral_info()
