class ActiveTurbines(object):
    def writeActiveList(self, aList):
        bList = []
        for i in aList:
            bList.append(str(i))
        # if len(aList) == 1:
        #     aline = str(aList[0])
        # else:
        aline = ','.join(bList)
        with open('activeList.txt', 'w') as f:
            f.write(aline)

    def readActiveList(self):
        with open('activeList.txt', 'r') as f:
            for line in f.readlines():
                return line.strip().split(",")
                print(line.strip())
