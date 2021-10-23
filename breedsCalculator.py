import hashlib
import pprint


class dragon:

    def __init__(self,fuerza,inteligencia,defensa,parents=[None,None]):

        self.fuerza         = fuerza
        self.inteligencia   = inteligencia
        self.defensa        = defensa
        self.child          = 0
        self.parents        = parents
        self.id = id(self)

    def returnData(self):

        return { "fuerza"       :self.fuerza,
                 "inteligencia" :self.inteligencia,
                 "defensa"      :self.defensa,
                 "child"        :self.child,
                 "parents"      :self.parents}

    def getHash(self):

        data = [self.fuerza,self.inteligencia,self.defensa]
        hash_object = hashlib.sha256(str(data).encode())
        hex_dig     = hash_object.hexdigest()
        return hex_dig



def breedChild(a,b, round_factor = 0):

    result_fuerza = int(round(((a.fuerza+b.fuerza)/2)*1.2,round_factor))
    result_inteligencia = int(round(((a.inteligencia+b.inteligencia)/2)*1.2,round_factor))
    result_defensa = int(round(((a.defensa+b.defensa)/2)*1.2,round_factor))

    # a.child += 1
    # b.child += 1
    new_dragon = dragon(result_fuerza,result_inteligencia,result_defensa,[a,b])

    return new_dragon

def generateNewGeneration(a,b):

    hijo_AB1 = breedChild(a,b)
    hijo_AB2 = breedChild(a,b)

    return hijo_AB1,hijo_AB2

def calculatePowerDragon(dragon):

    return dragon.fuerza + dragon.inteligencia + dragon.defensa

def getCostBreed(a,b):

    prices_comun = { 0:5,
                     1:10,
                     2:20,
                     3:30,
                     4:40,
                     5:50}

    prices_pococomun = { 0:100,
                         1:150,
                         2:200,
                         3:300,
                         4:500,
                         5:800}

    c = breedChild(a,b)
    power_a = calculatePowerDragon(a)
    power_b = calculatePowerDragon(b)
    power_c = calculatePowerDragon(c)


    if power_a <= 49 and power_b <= 49 and power_c <= 49:
        drag_type = 0
        multiplicator = 1
    elif power_a >= 49 and power_b >= 49 and power_c < 49:
        drag_type = 0
        multiplicator = 1.5
    elif power_a > 49 and power_b <= 49 and power_c > 49:
        drag_type = 1
        multiplicator = 1.5
    elif power_a <= 49 and power_b > 49 and power_c > 49:
        drag_type = 1
        multiplicator = 1.5

    elif power_a > 49 and power_b > 49:
        drag_type = 1
        multiplicator = 1
    elif power_a <= 49 and power_b <= 49 and power_c <= 49:
        drag_type = 0
        multiplicator = 1

    elif power_a <= 49 and power_b <= 49 and power_c > 49:
        drag_type = 0
        multiplicator = 1

    childs = a.child if a.child >= b.child else b.child

    if drag_type == 0:
        cost = prices_comun[childs] * multiplicator
        spark_cantidad = 5
        spark_price = 0
    else:
        cost = prices_pococomun[childs] * multiplicator
        spark_cantidad = 25
        spark_price = 50

    # print(a.child,b.child,"=",cost)

    a.child += 1
    b.child += 1

    return cost + spark_price, spark_cantidad

def printData(data):

        total_cost = 0
        total_sparks = 0
        total_days = 0
        for breed_num in data.keys():
            total_cost += data[breed_num]["price"]
            total_days += data[breed_num]["time"]
            total_sparks += data[breed_num]["time"]*sparks_win_per_day
            print("BREED {breed_num}: {dragon_a}|{dragon_a_power} + {dragon_b}|{dragon_b_power} = {child} | {price} cyt | {time} days".format(
                        breed_num      = breed_num,
                        dragon_a       = "[{},{},{}]".format(data[breed_num]["dragon_a"].fuerza,data[breed_num]["dragon_a"].inteligencia,data[breed_num]["dragon_a"].defensa),
                        dragon_a_power = data[breed_num]["dragon_a_power"],
                        dragon_b       = "[{},{},{}]".format(data[breed_num]["dragon_b"].fuerza,data[breed_num]["dragon_b"].inteligencia,data[breed_num]["dragon_b"].defensa),
                        dragon_b_power = data[breed_num]["dragon_b_power"],
                        child          = "[{},{},{}] | {}".format(data[breed_num]["child"].fuerza,data[breed_num]["child"].inteligencia,data[breed_num]["child"].defensa,calculatePowerDragon(data[breed_num]["child"])),
                        price          = data[breed_num]["price"],
                        time           = data[breed_num]["time"]))

        print("\n****************************")
        print("TOTAL COST: {}".format(total_cost))
        print("TOTAL SPARK: {}".format(total_sparks))
        print("TOTAL DAYS: {}".format(total_days))

class Family:

    def __init__(self):

        self.list_dragons = []
        self.list_parents = []

    def sortOrderParents1(self):
        pass
        # import collections
        # new_parents = {}
        # for breed in self.list_parents:

        #     pos = max(calculatePowerDragon(breed[0]),calculatePowerDragon(breed[1]))
        #     if not str(pos) in new_parents.keys():
        #         new_parents[str(pos)] = [breed[0],breed[1]]
        #     else:
        #         new_parents[str(pos-1)] = [breed[0],breed[1]]

        # new_parents = collections.OrderedDict(new_parents)

        # self.list_parents = list(new_parents.values())

    def sortOrderParents(self):
        pass
        # list_added_dragons = [self.list_parents[0][0],self.list_parents[0][1]]
        # new_list_parents = [self.list_parents[0]] 
        # pending_dragons = [x for x in self.list_parents]

        
        # for breed in self.list_parents:

        #     if breed[0].parents[0] in list_added_dragons and breed[0].parents[1] in list_added_dragons\
        #         and breed[1].parents[0] in list_added_dragons and breed[1].parents[1] in list_added_dragons:


        #         new_list_parents.append(breed)
        #         list_added_dragons += breed
        #         # self.list_parents.remove(breed)

        #     else:
        #         print("MISSING PARENT:",breed)


        # self.list_parents = new_list_parents

    def returnGeneration(self):

        global sparks_win_per_day
        data = dict()
        breed_num = 1
        
        for dragon in self.list_dragons:
            dragon.child = 0

        for breed in self.list_parents:
            price, sparks = getCostBreed(breed[0],breed[1])

            data[breed_num]                    = dict()
            data[breed_num]["dragon_a"]        = breed[0]
            data[breed_num]["dragon_a_power"]  = calculatePowerDragon(breed[0])
            data[breed_num]["dragon_b"]        = breed[1]
            data[breed_num]["dragon_b_power"]  = calculatePowerDragon(breed[1])
            data[breed_num]["child"]           = breedChild(breed[0],breed[1])
            data[breed_num]["price"]           = price
            data[breed_num]["time"]            = sparks/sparks_win_per_day

            breed_num += 1

        return data

class Generation:

    def __init__(self,total_breed = 89):

        self.total_breed = total_breed
        self.num_family = -1
        self.list_families = {}
        self.new_parents = []

    def generateFamilies(self,padre_A,padre_B):

        self.addFamily(padre_A,padre_B)
        self.generateHierarchyBrothers(padre_A,padre_B)
        if not self.total_breed in [calculatePowerDragon(d) for d in self.list_families[self.num_family].list_dragons]:
            self.checkWithParents()

        self.list_families[self.num_family].sortOrderParents()

        # self.addFamily(padre_A,padre_B)
        # self.generateHierarchyParents(padre_A,padre_B)
        # self.list_families[self.num_family].sortOrderParents()

        return self.list_families


    def generateHierarchyParents(self,a,b):

        good_89 = False
        list_dragons = [a,b]
        for p1 in list_dragons:

            new_dragons = []
            for p2 in list_dragons:

                if p1 != p2:

                    result = breedChild(p1,p2)

                    if calculatePowerDragon(result) == self.total_breed:
                        good_89 = result
                        break

                    else:
                        if not result in new_dragons and not result in list_dragons:
                            new_dragons.append(result)

            list_dragons += new_dragons

            if good_89:
                self.addNewGenerations(good_89.parents,True)
                
                break

    def generateHierarchyBrothers(self,a,b):

        ha,hb = generateNewGeneration(a,b)

        if calculatePowerDragon(ha) < 89 and calculatePowerDragon(hb) < 89:
            self.list_families[self.num_family].list_parents.append(ha.parents)
            self.list_families[self.num_family].list_parents.append(hb.parents)
            self.list_families[self.num_family].list_dragons += [a,b]
            print(self.list_families[self.num_family].list_parents)
            self.generateHierarchyBrothers(ha,hb)
            self.list_families[self.num_family].list_dragons += [ha,hb]

    def checkWithParents(self):

        good_89 = []
        list_dragons = [x for x in self.list_families[self.num_family].list_dragons]
        for p1 in list_dragons:

            new_dragons = []
            for p2 in list_dragons:

                if p1 != p2:

                    result = breedChild(p1,p2)
                    print(calculatePowerDragon(result))
                    if calculatePowerDragon(result) == self.total_breed:
                        good_89 = result
                        break

                    else:
                        if not result in new_dragons and not result in list_dragons:
                            if calculatePowerDragon(result) < 89:
                                new_dragons.append(result)
            list_dragons += new_dragons
            # self.list_families[self.num_family].list_dragons += new_dragons

            if good_89:
                self.addNewGenerations(good_89,True)

                break

    def addNewGenerations(self,dragon,breed_89 = False):

        if not dragon in self.list_families[self.num_family].list_dragons:
            self.list_families[self.num_family].list_dragons.append(dragon)

        parents = dragon.parents
        parent_a = dragon.parents[0]
        parent_b = dragon.parents[1]

        if not parents in self.list_families[self.num_family].list_parents:
            self.list_families[self.num_family].list_parents.append(parents)
            if breed_89:
                self.list_families[self.num_family].list_parents.append(parents)

        if not parent_a in self.list_families[self.num_family].list_dragons or not parent_b in self.list_families[self.num_family].list_dragons:

            if not parent_a in self.list_families[self.num_family].list_dragons:
                self.list_families[self.num_family].list_dragons.append(parent_a)
                self.addNewGenerations(parent_a)

            if not parent_b in self.list_families[self.num_family].list_dragons:
                self.list_families[self.num_family].list_dragons.append(parent_b)
                self.addNewGenerations(parent_b)

    def addFamily(self,padre_A=None,padre_B=None):

        self.num_family += 1
        self.list_families[self.num_family] = Family()
        self.list_families[self.num_family].list_parents = []
        self.list_families[self.num_family].list_dragons = []

        return self.list_families[self.num_family]

def run(a,b):
    generation = Generation(89)
    data     = generation.generateFamilies(a,b)
    total = 1000000000000
    num = 0
    for n,f in data.items():
        _data = f.returnGeneration()
        total_cost = 0
        total_days = 0
        for breed_num in _data.keys():
            total_cost += _data[breed_num]["price"]
            total_days += _data[breed_num]["time"]
            if total_cost < total:
                num = n

            if calculatePowerDragon( _data[breed_num]['child']) == 89:
                ch = breedChild( _data[breed_num]['child'],_data[breed_num]['child'])
                print("[{},{},{}] | {}".format(ch.fuerza,ch.inteligencia,ch.defensa,calculatePowerDragon(ch)))

    printData(data[num].returnGeneration())

if __name__ == '__main__':
    
    sparks_win_per_day = 14

    # padre_A = dragon(16,13,14)
    # padre_A = dragon(17,13,14)
    # padre_B = dragon(17,13,14)
    # padre_A = dragon(16,13,14)
    # padre_B = dragon(14,13,13)
    # run(padre_A,padre_B)

    padre_A = dragon(16,13,14)
    padre_B = dragon(12,8,10)
    # padre_B = dragon(14,13,13)
    ch1 = breedChild(padre_A,padre_B)
    print(ch1.fuerza,ch1.inteligencia,ch1.defensa)

    ch2 = breedChild(ch1,padre_A)
    print(ch2.fuerza,ch2.inteligencia,ch2.defensa)

    ch3 = breedChild(ch2,padre_B)
    print(ch3.fuerza,ch3.inteligencia,ch3.defensa)

    ch4 = breedChild(ch3,ch1)
    print(ch4.fuerza,ch4.inteligencia,ch4.defensa)

    ch5 = breedChild(ch4,ch4)
    print(ch5.fuerza,ch5.inteligencia,ch5.defensa)

    ch6 = breedChild(ch4,padre_B)
    print(ch6.fuerza,ch6.inteligencia,ch6.defensa)

    ch2 = breedChild(ch6,padre_B)
    print(ch2.fuerza,ch2.inteligencia,ch2.defensa)

    ch3 = breedChild(ch2,ch2)
    print(ch3.fuerza,ch3.inteligencia,ch3.defensa)

    ch4 = breedChild(ch3,ch3)
    print(ch4.fuerza,ch4.inteligencia,ch4.defensa)

    ch5 = breedChild(ch4,ch4)
    print(ch5.fuerza,ch5.inteligencia,ch5.defensa)

    ch6 = breedChild(ch5,padre_B)
    print(ch6.fuerza,ch6.inteligencia,ch6.defensa)

    ch7 = breedChild(ch6,padre_B)
    print(ch7.fuerza,ch7.inteligencia,ch7.defensa)

    ch8 = breedChild(ch7,ch7)
    print(ch8.fuerza,ch8.inteligencia,ch8.defensa)

    ch9 = breedChild(ch8,ch8)
    print(ch9.fuerza,ch9.inteligencia,ch9.defensa)

    ch1 = breedChild(ch9,padre_B)
    print(ch1.fuerza,ch1.inteligencia,ch1.defensa)

    ch2 = breedChild(ch1,padre_B)
    print(ch2.fuerza,ch2.inteligencia,ch2.defensa)

    ch3 = breedChild(ch2,padre_B)
    print(ch3.fuerza,ch3.inteligencia,ch3.defensa)

    ch4 = breedChild(ch3,padre_B)
    print(ch4.fuerza,ch4.inteligencia,ch4.defensa)

    ch1 = breedChild(ch4,ch4)
    print(ch1.fuerza,ch1.inteligencia,ch1.defensa)

    ch2 = breedChild(ch1,ch1)
    print(ch2.fuerza,ch2.inteligencia,ch2.defensa)

    ch3 = breedChild(ch2,ch2)
    print(ch3.fuerza,ch3.inteligencia,ch3.defensa)

    ch4 = breedChild(ch3,ch3)
    print(ch4.fuerza,ch4.inteligencia,ch4.defensa)

    ch5 = breedChild(ch4,ch4)
    print(ch5.fuerza,ch5.inteligencia,ch5.defensa)






    # padre_B = dragon(16,13,14)
    # run(padre_A,padre_B)

    # padre_A = dragon(14,13,13)
    # padre_B = dragon(16,13,14)
    # run(padre_A,padre_B)

    # padre_A = dragon(12,8,10)
    # padre_B = dragon(14,13,13)
    # run(padre_A,padre_B)



    
    

    
