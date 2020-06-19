import dndTools
import numpy as np

class business: #this is not very elegant please ignore the countless circular dependencies!
    def __init__(self, products={}, producers={}, locations={}, day=0, total_gp=0):
        self.products = products #dict of product objects with product names as keys
        self.producers = producers #dict of producer objects with producer names as keys
        self.locations = locations #dict of location objects with location names as keys
        self.day = day
        self.total_gp = total_gp

    def __call__(self, days=1):
        """
        days is the number of days to run the business for. The value should be an int
        """
        period_gp = 0
        for day in range(days):
            daily_gp = 0
            print("day {0}".format(self.day))
            
            for location in self.locations:
                for product in self.products:
                    supply = 0
                    cost = 0
                    for producer in self.locations[location].producers:
                        producer_supply,producer_cost =  self.producers[producer](product) #TODO expose producers to logs
                        supply += producer_supply
                        cost += producer_cost
                    product_gp,product_message = self.products[product](self.locations[location],supply,cost)
                    daily_gp += product_gp
                    print(product_message)
                print("for day {0} in {1} the total profit was {2}".format(self.day,location,daily_gp))
            self.day += 1 #increment day
            period_gp += daily_gp
        self.total_gp += period_gp
        print("in the last {0} days, {1} gp was earned. The total balance is {2}".format(days,period_gp, self.total_gp))

    def add_product(self,product):
        self.products[product.name] = product

    def add_producers(self,producer):
        self.producers.append(producer)

    def add_location(self,location):
        self.locations[location.name] = location

    def save(self): #TODO save as json
        pass

    def load(self): #TODO load from json
        pass

class product:
    def __init__(self, name, oneoff, price, locations, interest, saturated_demand):
        """
        name is the products name. oneoff is a bool if true people only need to buy it once, saturated demand will increase when products are bought.
        """
        self.name = name #string
        self.oneoff = oneoff #bool
        self.price = price #float
        self.locations = locations #list of string
        self.interest = interest #dict of floats with locations as keys
        self.saturated_demand = saturated_demand #dict of int with locations as keys

        #initialise revenue, profit, and cost
        self.revenue = {}
        self.profit = {}
        self.cost = {}
        for location in self.locations:
            self.revenue[location] = []
            self.profit[location] = []
            self.cost[location] = []
            
    def __call__(self, location, supply, cost):
        """
        returns product_gp (gold earned per day) and product_message (string providing more detailed updates on parameters)
        """
        demand = location.population * location.presence * self.interest[location.name] * location.purchase_power(self.price) - self.saturated_demand[location.name]
        revenue = min(demand,supply) * (dndTools.roll(5,20)/100) * self.price #diceroll used for randomness
        profit = revenue - cost

        #product message
        product_message = "For {0} in {1}. There was {3}gp revenue, and {4}gp costs. For {2}gp profit.".format(self.name,location.name,profit,revenue,cost)
        
        #log results
        self.revenue[location.name].append(revenue)
        self.profit[location.name].append(profit)
        self.cost[location.name].append(cost)

        return(profit,product_message)

    def add_location(self,location_name,interest,producers=[],saturated_demand=0):
        #add location name to locations list
        self.locations.append(location_name )
        #add interest to interest dict with location name as key
        self.interest[location_name] = interest
        #add saturated_demand to saturated_demand dict with location name as key
        self.saturated_demand[location_name] = saturated_demand
        #add logging lists to dicts with location names as key
        self.revenue[location_name] = []
        self.profit[location_name] = []
        self.cost[location_name] = []


class producer:
    def __init__(self,name,products,capacity,badactor=False):
        self.name = name #string
        self.products = products #dict of tuples 'product':(supply,cost) where supply is an int and cost is float NOTE: cost is cost to produce the number given by supply not per unit
        self.capacity = capacity #int total supply across all products, if supply exceeds capacity an error is thrown #TODO add error 
        self.badactor = badactor #bool if true producer may steal/not work on some days

    def __call__(self,product):
        #check for product in product list
        if (not product in self.products):
            return (0,0)

        #return supplies and costs
        return self.products[product]


class location:
    def __init__(self,name,population,purchase_power,presence,producers):
        self.name = name #string
        self.population = population #int
        self.purchase_power = purchase_power #callable takes price returns percentage that can afford
        self.presence = presence #percentage
        self.producers = producers #producers

    def add_producer(self,producer):
        self.producers.append(producer)

class purchase_power:
    def __init__(self, percentage_at_price_point):
        """
        percentage_at_at_price_point should be a list where values are the percentage (as a value between 0 and 1)
        of people who can afford a price equal to 10 to the power of the index value.
        
        e.g a list [0.9,0.5,0.3,0.1] corresponds to 90% of people affording 1gp, 50% affording 10gp, 30% 100gp,
        10% 1000gp
        """
        percentage_afford = []
        price = [] 
        for i,percentage in enumerate(percentage_at_price_point):
            #I've hacked this to do it quickly
            if (i==0):
                price += np.linspace(0,10**i,2).tolist()
                percentage_afford += np.linspace(1,percentage,2).tolist() 
            else:
                price += np.linspace(10**(i-1),10**i,2).tolist()
                percentage_afford += np.linspace(percentage_at_price_point[i-1],percentage,2).tolist()
            
        self.model = np.poly1d(np.polyfit(price,percentage_afford,1)) 
    
    def __call__(self,price):
        percentage_afford = self.model(price)
        
        if (percentage_afford > 1): percentage_afford = 1
        if (percentage_afford < 0): percentage_afford = 0
    
        return percentage_afford 

#config for testing
bs_products = {'huntingtrap':product('huntingtrap',False,5,['hethport'],{'hethport':0.01},{'hethport':0})}
bs_producers = {'bug':producer('bug',{'huntingtrap':(4,8)},4)}
hethport_purchase_power = purchase_power([0.9,0.6,0.1,0.1,0.05])
bs_locations = {'hethport':location('hethport',120000,hethport_purchase_power,0.05,['bug'])}
bs = business(bs_products,bs_producers,bs_locations)
