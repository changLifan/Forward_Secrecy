def set_link(i, j, value):
    DV[i][j] = value
    DV[j][i] = value

DV = []
if __name__ == '__main__':
    DV =[[float('inf') for i in range(9)] for i in range(9)]
    for i in range(9):
        DV[i][i] = 0
    
    set_link(0,1,4)
    set_link(0,7,8)
    set_link(1,2,8)
    set_link(1,7,11)
    set_link(2,3,7)
    set_link(2,5,4)
    set_link(2,8,2)
    set_link(3,4,9)
    set_link(3,5,14)
    set_link(4,5,10)
    set_link(5,6,2)
    set_link(6,7,1)
    set_link(6,8,6)
    set_link(7,8,7)

    print('Initialize table:')
    for i in range(len(DV)):
        print('D%d(0,1,2,...,9)=%s'%(i,DV[i]))
    print('')
    
    nd_link = []
    nd_link.append([1,7])
    nd_link.append([0,2,7])
    nd_link.append([1,3,5,8])
    nd_link.append([2,4,5])
    nd_link.append([3,5])
    nd_link.append([2,3,4,6])
    nd_link.append([5,7,8])
    nd_link.append([0,1,6,8])
    nd_link.append([2,6,7])

    print(nd_link)

    for i in range(10):
        for j in range(9):
            for k in range(9):
                for adj_node in nd_link[j]:
                    if DV[j][adj_node]+DV[adj_node][k] < DV[j][k]:
                        DV[j][k] = DV[j][adj_node]+DV[adj_node][k]
                print('Table after DV algorithm:')
                for m in range(k):
                    print('D%d(0,1,2,...,9)=%s'%(m,DV[m]))
        print(f'第{i+1}轮更新', DV)
        
