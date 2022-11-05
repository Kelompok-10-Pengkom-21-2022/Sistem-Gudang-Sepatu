# ======================================  FUNCTION ======================================
import os
import time
import itertools
import threading
import sys

start = "\033[1m"
end = "\033[0;0m"

column = ["No.", "Series Name", "Collection", "Code", "39", "40", "41"]
columnWidth = [3, 11, 10, 4, 2, 2, 2]

def _inputInt(prompt, inputType, allowed):
    true = False
    while not true:
        __input = input(f"                          >> {(start + prompt + end)}: ")
        if __input.isdigit() == True:
            _input = int(__input)
            if inputType == "choice":
                if _input > -1 and _input < allowed:
                    true = True
                else:
                    print("                             Choice not avaliable. 😞")
            elif inputType == "size":
                if _input > 38 and _input < 42:
                    true = True
                else:
                    print("                             Size not available. 😞")
            elif inputType == "buyQ":
                if _input <= allowed:
                    true = True
                else:
                    print(f"                             Sorry, stock are just {allowed}. 😞")
            else:
                true = True
        else:
            print("                             Input not valid. 😞")
    return _input

def _inputStr(prompt, inputType):
    global shoesCount
    true = False
    while not true:
        __input = input(f"                          >> {(start + prompt + end)}: ")
        if inputType == "search":
            # __input = __input.capitalize()
            true = True
        elif inputType == "buyCode" or inputType == "addStockCode":
            # stock update
            i = 0
            while true == False and i < shoesCount:
                if (__input == shoes[2][i]):
                    true = True
                    __input = str(i)
                i += 1 
            if true == False:
                print("                             Code not found. 😞")
        elif inputType == "addCode":
            found = False
            i = 0
            while found == False and i < shoesCount:
                if (__input == shoes[2][i]):
                    found = True
                i += 1 
            if found == True:
                print("                             Code already exist. 😞")
                true = False
            else:
                true = True
        elif inputType == "addCo":
            __input = __input.upper()
            true = True
            if __input == 'U':
                __input = "Men-Women"
            elif __input == 'M':
                __input = "Men"
            elif __input == 'W':
                __input = "Women"
            else:
                print(f"                             Type {__input} not available. 😞")
                true = False
        elif inputType == "addSeries":
            true = True
    return __input

def readFile():
    global shoes
    global shoesCount
    file = open("data.txt", 'r')
    # read the first line of the file
    shoesCount = int(file.readline())

    # array template
    shoes = [[[0 for i in range(3)] for j in range(shoesCount)], ["" for j in range(
        shoesCount)], ["" for j in range(shoesCount)], ["" for j in range(shoesCount)]]
    # shoes = [[array0], [array1], [array2]]
    # array0: 3 sets of sizes for each series
    # array1: collection category of each series
    # array2: code of each series
    # array3: name of each series
    # insert data to array template
    idx = 0
    for line in file:
        shoes[0][idx][0] = int(line.split()[0])
        shoes[0][idx][1] = int(line.split()[1])
        shoes[0][idx][2] = int(line.split()[2])
        # size
        # [array0] of [shoes] is an array in an array in an array
        # shoes [array0] [set of series] [set of sizes]
        shoes[1][idx] = line.split()[3]
        # collection
        # [array1] of [shoes] is an array in an array
        # shoes [array1] [set of series]
        '''New Update'''
        shoes[2][idx] = line.split()[4]
        # code
        # [array2] of [shoes] is an array in an array
        # shoes [array2] [set of series]
        shoes[3][idx] = ' '.join(line.split()[5:])
        # series
        # [array3] of [shoes] is an array in an array
        # shoes [array3] [set of series]
        # source.slice()[]: slices items in source in range [],
        # resulting in each word in range [] becoming an item of a new array
        # ''.join(): joining items of the new array into a string, existing items are separated by ''
        idx += 1
    file.close()

def writeFile():
    global shoes
    global shoesCount 
    file = open("data.txt", 'w')
    strShoes = str(shoesCount) + '\n' + '\n'.join((str(shoes[0][idx][0]) + ' ' + str(shoes[0][idx][1]) + ' ' + str(shoes[0][idx][2]) + ' ' + str(shoes[1][idx]) + ' ' + str(shoes[2][idx]) + ' ' + str(shoes[3][idx])) for idx in range (shoesCount))
    file.write(strShoes)
    file.close()

def menuDisplay(choices):
    os.system("cls")
    print("=====================================================================")
    print(start + "                             ♥ ShoeShoe ♥" + end)
    print("=====================================================================")
    print()
    print(f"                         「 {choices[0].upper()} 」")
    print()
    for i in range(1, len(choices) - 1):
        print(f"                          ↳ {i}. {choices[i]}")
    print(f"                          ↳ 0. {choices[len(choices) - 1]}")
    print()
    return _inputInt("I want to do", "choice", len(choices)-1)

def showShoes(req):
    global shoes
    global shoesCount
    
    print()

    if req == "all" :
        loading()
        tableHeader()
        for i in range (shoesCount):
            showOneShoe(i, i+1)
    else:
        key = _inputStr(f"I want to search this {req}", "search")
        if req == "series" :
            idxCheck = 3
        elif req == "collection" :
            idxCheck = 1
        count = 0
        loading()
        tableHeader()
        for i in range (shoesCount):
            found = shoes[idxCheck][i].find(key)
            # source.find(): find members that contain () in source
            # if not found, index will be -1
            if (found != -1):
                count += 1
                showOneShoe(i, count)
    print()

def charLoop(char, loop):
    for i in range(loop):
        print(char, end='')


def tableHeader():
    print()

    columnWidth[0] = len(str(shoesCount)) + 1
    columnWidth[1] = max([max([len(shoes[3][i]) for i in range(shoesCount)]), columnWidth[1]])
    columnWidth[2] = max([max([len(shoes[1][i]) for i in range(shoesCount)]), columnWidth[2]])
    columnWidth[3] = max([max([len(shoes[2][i]) for i in range(shoesCount)]), columnWidth[3]])
    columnWidth[4] = max([max([len(str(shoes[0][i][0])) for i in range(shoesCount)]), columnWidth[4]])
    columnWidth[5] = max([max([len(str(shoes[0][i][1])) for i in range(shoesCount)]), columnWidth[5]])
    columnWidth[6] = max([max([len(str(shoes[0][i][2])) for i in range(shoesCount)]), columnWidth[6]])

    print()
    for i in range(7):
        print('+', end='')
        charLoop('-', columnWidth[i] + 2)
    print('+')  
    print('|', end='')
    for i in range(7):
        print('', start + column[i] + end, end='')
        charLoop(' ', columnWidth[i] - len(column[i]) + 1)
        print('|', end='')
    print()
    for i in range(7):
        print('+', end='')
        charLoop('-', columnWidth[i] + 2)
    print('+')        

def oneCell(string, i):
    print(f" {string}", end="")
    charLoop(' ', columnWidth[i] - len(string) + 1)
    print('|', end='')

def showOneShoe(idx, count):
    print('|', end='')
    oneCell(str(count) + '.', 0)
    oneCell(shoes[3][idx], 1)
    oneCell(shoes[1][idx], 2)
    oneCell(shoes[2][idx], 3)
    oneCell(str(shoes[0][idx][0]), 4)
    oneCell(str(shoes[0][idx][1]), 5)
    oneCell(str(shoes[0][idx][2]), 6)
    print()
    for i in range(7):
        print('+', end='')
        charLoop('-', columnWidth[i] + 2)
    print('+')   


def _(menu):
    if menu == "main":
        return ["Menu", "Show All Shoes", "Search Shoes", "Buy Shoes", "Add Shoes", "Close App"]
    elif menu == "search":
        return ["Search shoes by", "Series", "Collection", "Back"]
    elif menu == "buy":
        return ["Menu", "Buy Shoes", "Main Menu"]
    elif menu == "add":
        return ["Menu", "Add New Shoes", "Add Stock to an Existing Shoe", "Back"]


def buy():
    global shoes
    global shoesCount
    # one series, one size, several pairs every buy
    os.system("cls")
    print("=====================================================================")
    print(start + "                             ♥ ShoeShoe ♥" + end)
    print("=====================================================================")
    print()
    print(f"                         「 BUY SHOES 」")
    print()
    idx = int(_inputStr("Code", "buyCode"))
    size = _inputInt("Size", "size", 0)
    pair = _inputInt("Quantity", "buyQ", shoes[0][idx][size-39])
    # update
    shoes[0][idx][size-39] -= pair
    print()
    loading()
    writeFile()
    print()
    print()
    print("[SUCCESS]")
    print("Here is updated stock:", end='')
    tableHeader()
    showOneShoe(idx, 1)
    print()

def add(ty):
    global shoes
    global shoesCount
    idx = 0
    os.system("cls")
    print("=====================================================================")
    print(start + "                             ♥ ShoeShoe ♥" + end)
    print("=====================================================================")
    print()
    if ty == "new":
        print(f"                         「 ADD NEW SHOES 」")
        print()
        shoes[2].append(_inputStr("Code", "addCode"))
        shoes[3].append(_inputStr("Series", "addSeries"))
        shoes[1].append(_inputStr("Collection [U/M/W]", "addCo"))
        shoes[0].append([_inputInt("Stock (size 39)", "", 0), _inputInt("Stock (size 40)", "", 0), _inputInt("Stock (size 41)", "", 0)])
        shoesCount += 1
        idx = shoesCount - 1
    else:
        print(f"                         「 ADD STOCK 」")
        print()
        idx = int(_inputStr("Code", "addStockCode"))
        size = _inputInt("Size", "size", 0)
        addStock = _inputInt("Quantity", '', 0)
        # update
        shoes[0][idx][size - 39] += addStock
    loading()
    writeFile()
    print()
    print()
    print("[SUCCESS]")
    print("Here is updated stock:", end='')
    tableHeader()
    showOneShoe(idx, 1)
    print()

def loading():
    done = False
    def animate():
        for c in itertools.cycle(['.', '..', '...', '....']):
            if done:
                break
            sys.stdout.write('\rloading ' + c)
            sys.stdout.flush()
            time.sleep(0.2)
    threading.Thread(target=animate).start()
    time.sleep(1.6)
    done = True
