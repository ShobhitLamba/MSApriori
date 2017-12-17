# Authors : Shobhit Lamba, Sakshi Panday
# Email Address : slamba4@ uic.edu, spanda7@uic.edu

import os
import itertools

phi = 0.0
MS = dict()
temp = dict()
MISSortDict = dict()
IList = list()
ICount = dict()
TList = list()
TCount = 0
L = list()
FList = list([] for _ in range(10))
CList = list([] for _ in range(10))
CDict = dict()
cannotBeTogether = list()
mustHave = list()
tailCount = {}

script_dir = os.path.dirname(__file__)

def main():
    readData()
    initPass()
    F1()
    Fi()
    cannotBeTogetherConstraint()
    if (mustHave != []):
        mustHaveConstraint()
    output()


def readData():
    '''To read the MIS values and phi (SDC) from parameterfile.txt'''
    global MS, TCount, IList, ICount, phi, TList, cannotBeTogether, mustHave
    
    rel_path_params = "parameters/para1-1.txt"
    abs_filepath_params = os.path.join(script_dir, rel_path_params)
    file1 = open(abs_filepath_params)


    for i in file1:
        if (i.find('SDC') != -1):
            phi = float(i.replace(' ','').rstrip().split('=')[1])

        if (i.find('MIS') != -1):
            temp = i.replace(' ','').replace('MIS','').replace('(','').replace(')','').rstrip().split('=')
            MS[int(temp[0])] = float(temp[1])

        if (i.find('must-have') != -1):
           mustHave = i.replace('must-have:','').replace(' ','').rstrip().split('or')
           mustHave = list(map(int, mustHave))

        if (i.find('cannot_be_together') != -1):
            global cannotBeTogether
            cannotBeTogether = i.replace(' ','').replace('cannot_be_together:','').replace('{','[').replace('}',']').replace("'", 'a').rstrip().split('a')    
            cannotBeTogether = cannotBeTogether[0].replace('],[',' ').replace('[','').replace(']','').split()
            for i in range(len(cannotBeTogether)):
                cannotBeTogether[i] = list(map(int, cannotBeTogether[i].split(',')))


    items = sorted(MS, key = MS.__getitem__)

    for item in items:
        IList.append(int(item))
        ICount[int(item)] = 0

    '''To read the Transactions from inputdata.txt'''
    rel_path_data = "data/data1.txt"
    abs_filepath_data = os.path.join(script_dir, rel_path_data)
    file2 = open(abs_filepath_data)


    for i in file2:
        TList.append(list())
        transaction = i.replace(' ', '').replace('{','').replace('}','').replace('<','').replace('>','').split(',')
        for t in transaction:
            TList[len(TList) - 1].append(int(t))
            if(ICount.get(int(t)) != None):
                ICount[int(t)] = ICount.get(int(t)) + 1

    TCount = len(TList)

def initPass():
    global L
    for i in range(len(IList)):
        if(i == 0):
            L.append(IList[0])
        else:
            if((ICount.get(IList[i]) / TCount) >= MS.get(IList[0])):
                L.append(IList[i])

    for i in range(len(L)):
        MISSortDict[L[i]] = i


def level2CandidateGeneration():
    global CList, L
    for l in range (0, len(L)):
        if (ICount[L[l]] / TCount) >= MS[L[l]]:
            for h in range( l + 1, len(L)):
                if (ICount[L[h]] / TCount) >= MS[L[l]] and abs((ICount[L[h]] / TCount) - (ICount[L[l]] / TCount)) <= phi:
                    CList[2].append(list())
                    CList[2][len(CList[2])-1].append(L[l])
                    CList[2][len(CList[2])-1].append(L[h])
    CList[2].sort(key = lambda row: row[1])


def findSubsets(S,m):
    return list(set(itertools.combinations(S, m)))

def MSCandidateGeneration(n):
    m = n - 1
    k = 0
    for i in range(0, len(FList[m])):
        for j in range(0, len(FList[m])):
            while ((k < m-1) and (FList[m][i][k] == FList[m][j][k])):
                k += 1
                
            if (k == m - 1):
                if ((MISSortDict[FList[m][i][k]] < MISSortDict[FList[m][j][k]]) and (abs((ICount[FList[m][i][k]] / TCount) - (ICount[FList[m][j][k]] / TCount)) <= phi)):
                    CList[m+1].append(list(FList[m][i]))
                    CList[m+1][len(CList[m+1])-1].append(FList[m][j][k])
                    subset = findSubsets(CList[m+1][len(CList[m+1])-1],m)
                    for sub in range(0,len(subset)):
                        if(not CList[m+1]):
                            if ((bool(CList[m+1][len(CList[m+1])-1][0]) in subset[sub]) or (MS[CList[m+1][len(CList[m+1])-1][1]] == MS[CList[m+1][len(CList[m+1])-1][0]])):
                                if (bool(subset[sub]) not in FList[m]):
                                    CList[m+1][len(CList[m+1])-1].remove()
            
            k=0

def F1():
    global FList
    if(not FList[1]):
        for i in range(len(L)):
            if((ICount.get(L[i])/TCount)>=MS.get(L[i])):
                FList[1].append([L[i]])


def Fi():
    global FList, CDict, tailCount
    k = 2
    while (True):
        if (not FList[k - 1]):
            break

        if (k == 2):
            level2CandidateGeneration()
        else:
            MSCandidateGeneration(k)

        for t in TList:
            for c in CList[k]:
                if (set(c).issubset(set(t))):
                    if (CDict.get(tuple(c)) == None):
                        CDict[tuple(c)] = 1
                    else:
                        CDict[tuple(c)] = CDict.get(tuple(c)) + 1

                if (set(c[1:]).issubset(set(t))):
                    if (tailCount.get(tuple(c)) == None):
                        tailCount[tuple(c)] = 1
                    else:
                        tailCount[tuple(c)] = tailCount.get(tuple(c)) + 1

        for c in CList[k]:
            if (CDict.get(tuple(c)) != None):
                if (CDict.get(tuple(c)) / TCount >= MS[c[0]]):
                    FList[k].append(c[:])
        k += 1


def cannotBeTogetherConstraint():
    global cannotBeTogether, FList
    for fListIndex in range(len(FList)):
        listIndex = len(FList[fListIndex])-1
        while listIndex > -1:
            subset = FList[fListIndex][listIndex]
            for i in range(len(cannotBeTogether)):
                    if(set(cannotBeTogether[i]) <= set(subset)):
                        FList[fListIndex].pop(FList[fListIndex].index(subset))
                        break
            listIndex = listIndex - 1

def mustHaveConstraint():
    global mustHave, FList
    for fListIndex in range(len(FList)):
        listIndex = len(FList[fListIndex])-1
        while listIndex > -1:
            subset = FList[fListIndex][listIndex]
            if(set(mustHave).isdisjoint(subset)):
                FList[fListIndex].pop(FList[fListIndex].index(subset))
            listIndex = listIndex - 1

def output():
    global FList, tailCount, ICount, CDict
    FList = [x for x in FList if x != []]
    
    rel_path_results = "results/result1-1.txt"
    abs_filepath_results = os.path.join(script_dir, rel_path_results)
    file3 = open(abs_filepath_results, "w")
    
    count = 0
    print ("Frequent 1-itemsets")
    file3.write("\nFrequent 1-itemsets\n")
    if (FList != []):
        for t in FList[0]:
            count += 1
            print ('\t' + str(ICount[t[0]]) + ' : { ' + str(t[0]) + ' }')
            file3.write('\t' + str(ICount[t[0]]) + ' : { ' + str(t[0]) + ' }\n')
    print ("\tTotal number of frequent 1-itemsets = " + str(count))
    file3.write("\tTotal number of frequent 1-itemsets = " + str(count) + "\n")


    for i in range(1,len(FList)):
         print ('\n\nFrequent',str(i+1) + '-itemsets')
         file3.write('\n\nFrequent' + str(i+1) + '-itemsets\n')
         count = 0
         for t in FList[i]:
              tCount = 0
              for j in range(len(TList)):
#                    print(TList[i],'  t:',t)
                    if(set(TList[j]) >= set(t)):
                        tCount += 1
              count += 1
              print ('\t',tCount , ' : {',str(t).replace("[", "").replace("]", ""),'}')
              file3.write('\t' + str(tCount) + ' : {' + str(t).replace("[", "").replace("]", "") + '}\n')
              print('Tail Count =', tailCount[tuple(t)])
              file3.write('Tail Count = ' + str(tailCount[tuple(t)]) + "\n")
         print ('\n\tTotal number of frequent', str(i+1) + '-itemsets = ' ,count)
         file3.write('\n\tTotal number of frequent ' + str(i+1) + '-itemsets = '  + str(count) + "\n")


if __name__ == "__main__": main()