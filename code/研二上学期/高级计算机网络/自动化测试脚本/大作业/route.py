KEYDATA_ZERO = 0
KEYDATA_FIRST = 1
KEYDATA_SECOND = 2
KEYDATA_THIRD = 3
KEYDATA_FOURTH = 4
KEYDATA_FIFTH = 5
KEYDATA_SIXTH = 6
KEYDATA_EVENTH = 7
KEYDATA_EIGHTH = 8
KEYDATA_NINTH = 9
KEYDATA_TENTH = 10
KEYDATA_ELEVENTH = 11
KEYDATA_FOURTEENTH = 14


def set_link(i, j, value):
    NODE_V[i][j] = value
    NODE_V[j][i] = value

def select_data(cans):
    data = ""
    if (cans == 'inf'):
        data = "no road access"
    else:
        data = cans
    return data

   
def node_update(i, j, NODE_V, nd_link, NODE_HOP):
    list = []
    flag = -1
    length_for_list = 0
    list_hop_router = []
    for k in range(KEYDATA_NINTH):
        for adj_node in nd_link[j]:
            if NODE_V[j][adj_node]+NODE_V[adj_node][k] < NODE_V[j][k]:
                NODE_V[j][k] = NODE_V[j][adj_node]+NODE_V[adj_node][k]
                NODE_HOP[j][k] = adj_node
                if (flag != j):
                    list = []
                    length_for_list = len(list)- 1
                list.append(k-1)
                list_hop_router.append(adj_node)
                '''print("adj_node is : ",adj_node)
                print("k is : ",k)
                print("j: ", j)
                print("append data is : ",NODE_V[adj_node][k])'''
            else:
                list_hop_router.append(-1)
        if (len(list) > length_for_list):
            #print("i: ", j, ", j: ", k)
            if (flag != j):
                list.insert(0,j)
                list.insert(len(list),k)
                flag = j
            else:
                list.insert(len(list),k)
            #print(list)
            #print()
            length_for_list = len(list)
        #print('Table after NODE_V algorithm:')
    for m in range(k):
        #print("i: ", j, ", j: ", k)
        print("                  ", "every line to update route: ")
        print("                  ", "Purpose of the network  ", "distance  ", "Next hop router")
        for j in range(len(NODE_V[m])):
            if m != j:
                print("                   ", 'N%d'%(j), "                     ", NODE_V[m][j],"           ", "N",NODE_HOP[m][j])
    print()               


def fun_update(NODE_V, nd_link, NODE_HOP):
    print()
    for i in range(10):
        for j in range(len(nd_link)):
            node_update(i, j, NODE_V, nd_link , NODE_HOP)
        
        # print(f'the {i+1} time update', NODE_V)
    print('Table after NODE_V algorithm:')
    for i in range(len(NODE_V)):
        print("Router ", i, " updated routing table is :")
        print("Purpose of the network  ", "distance  ", "Next hop router")
        for j in range(len(NODE_V[i])):
            if i != j:
                print('N%d'%(j), "                       ", NODE_V[i][j],"          ", "N",NODE_HOP[i][j])
        #print('N%d(0,1,2,...,9)=%s'%(i,NODE_V[i]))
        print()


def data_print(NODE_V, nd_link, NODE_HOP):
    print("Add nodes for the first time, we don't add any note : ")
    fun_update(NODE_V, nd_link, NODE_HOP);
    nd_link.append([0,8,2])
    fun_update(NODE_V, nd_link, NODE_HOP);
    nd_link.append([KEYDATA_FIRST,KEYDATA_EVENTH])
    print("Add nodes for the second time: ")
    fun_update(NODE_V, nd_link, NODE_HOP);
    nd_link.append([KEYDATA_ZERO,KEYDATA_SECOND,KEYDATA_EVENTH])
    print("Add nodes for the third time: ")
    fun_update(NODE_V, nd_link, NODE_HOP);
    nd_link.append([KEYDATA_FIRST,KEYDATA_THIRD,KEYDATA_FIFTH,KEYDATA_EIGHTH])
    print("Add nodes for the fourth time: ")
    fun_update(NODE_V, nd_link, NODE_HOP);
    nd_link.append([KEYDATA_SECOND,KEYDATA_FOURTH,KEYDATA_FIFTH])
    print("Add nodes for the fifth time: ")
    fun_update(NODE_V, nd_link, NODE_HOP);
    nd_link.append([KEYDATA_THIRD,KEYDATA_FIFTH])
    print("Add nodes for the sixth time: ")
    fun_update(NODE_V, nd_link, NODE_HOP);
    nd_link.append([KEYDATA_SECOND,KEYDATA_THIRD,KEYDATA_FOURTH,KEYDATA_SIXTH])
    print("Add nodes for the seventh time: ")
    fun_update(NODE_V, nd_link, NODE_HOP);
    nd_link.append([KEYDATA_FIFTH,KEYDATA_EVENTH,KEYDATA_EIGHTH])
    print("Add nodes for the eighth time: ")
    fun_update(NODE_V, nd_link, NODE_HOP);
    nd_link.append([KEYDATA_ZERO,KEYDATA_FIRST,KEYDATA_SIXTH,KEYDATA_EIGHTH])
    print("Add nodes for the ninth time: ")
    fun_update(NODE_V, nd_link, NODE_HOP);
    
    
    
    
def linkdata_pad():
    set_link(KEYDATA_ZERO,KEYDATA_FIRST,KEYDATA_THIRD)
    set_link(KEYDATA_ZERO,KEYDATA_EVENTH,KEYDATA_EIGHTH)
    set_link(KEYDATA_FIRST,KEYDATA_SECOND,KEYDATA_EIGHTH)
    set_link(KEYDATA_FIRST,KEYDATA_EVENTH,KEYDATA_ELEVENTH)
    set_link(KEYDATA_SECOND,KEYDATA_THIRD,KEYDATA_EVENTH)
    set_link(KEYDATA_SECOND,KEYDATA_FIFTH,KEYDATA_THIRD)
    set_link(KEYDATA_SECOND,KEYDATA_EIGHTH,KEYDATA_SECOND)
    set_link(KEYDATA_THIRD,KEYDATA_FOURTH,KEYDATA_NINTH)
    set_link(KEYDATA_THIRD,KEYDATA_FIFTH,KEYDATA_FOURTEENTH)
    set_link(KEYDATA_FOURTH,KEYDATA_FIFTH,KEYDATA_TENTH)
    set_link(KEYDATA_FIFTH,KEYDATA_SIXTH,KEYDATA_SECOND)
    set_link(KEYDATA_SIXTH,KEYDATA_EVENTH,KEYDATA_FIRST)
    set_link(KEYDATA_SIXTH,KEYDATA_EIGHTH,KEYDATA_SIXTH)
    set_link(KEYDATA_EVENTH,KEYDATA_EIGHTH,KEYDATA_EVENTH)
    set_link(KEYDATA_ZERO,KEYDATA_EIGHTH,KEYDATA_EVENTH)



def DVdata_init_data(NODE_V, NODE_HOP):
    print('Initialize table:')
    for i in range(len(NODE_V)):
        print("Router ", i, " updated routing table is :")
        print("Purpose of the network  ", "distance  ", "Next hop router")
        for j in range(len(NODE_V[i])):
            if i != j:
                print('N%d'%(j), "                       ", NODE_V[i][j], "          ", "N",NODE_HOP[i][j])
    print('')




NODE_V = []
NODE_HOP = []
if __name__ == '__main__':
    NODE_V =[[float('inf') for i in range(KEYDATA_NINTH)] for i in range(KEYDATA_NINTH)]
    for i in range(KEYDATA_NINTH):
        NODE_V[i][i] = 0
    
    NODE_HOP =[[float('inf') for i in range(KEYDATA_NINTH)] for i in range(KEYDATA_NINTH)]
    for i in range(KEYDATA_NINTH):
        NODE_HOP[i][i] = -1
        
    linkdata_pad()
    DVdata_init_data(NODE_V, NODE_HOP)
    
    nd_link = []
    data_print(NODE_V, nd_link, NODE_HOP)
         
