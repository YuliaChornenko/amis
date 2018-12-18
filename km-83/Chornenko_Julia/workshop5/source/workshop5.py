import plotly
import plotly.graph_objs as go

input_file = '../task/dz.csv'

#dataset
file=open(input_file)
info=file.read()
lines=info.splitlines()
dataset = dict()

statistics=[]
for statistic in lines[1:]:
    statistics.append(statistic.split(';'))


for statistic in statistics:
    client=statistic[0]
    date=statistic[1]
    product=statistic[2]
    quantity=statistic[3]
    price=statistic[4]
    if client in dataset:
        if date in dataset[client]:
            if product in dataset[client][date]:
                dataset[client][date][product]['quantity'] += quantity
                dataset[client][date][product]['price'] += price
            else:
                dataset[client][date][product] = {'quantity': quantity, 'price': price}
        else:
            dataset[client][date] = {product: {'quantity': quantity, 'price': price}}
    else:
        dataset[client] = {date: {product: {'quantity': quantity, 'price': price}}}
print(dataset)

# Які продукти купляли усі покупці?

client_products=dict()
for client in dataset:
    client_products[client] = set()

    for date in dataset[client]:
        client_products[client].update(set(dataset[client][date].keys()) )

orders = list(client_products.values())
products_set = orders[0]

for order in orders:
    products_set = products_set.intersection(order)

print('Усі купували',products_set)

# Як змінювалась ціна на яблука? (графік)


dates = []
prices = []

for client in dataset:
    for date in dataset[client]:
        if 'apple' in dataset[client][date]:
            dates.append(date)
            quantity, price = dataset[client][date]['apple'].values()
            prices.append(float(price)/float(quantity))

n = 1
while n < len(dates):
    for i in range(len(dates)-1):
        if dates[i] > dates[i+1]:
            dates[i], dates[i+1] = dates[i+1], dates[i]
            prices[i], prices[i+1] = prices[i+1], prices[i]
    n += 1


diagram = [go.Bar(x=dates,
                      y=prices)]
plotly.offline.plot(diagram, filename='change_price.html')

# Скільки грошей витрачає кожний покупець на покупки? (графік)

dictionary={}
for client in dataset:
    for date in dataset[client]:
        for product in dataset[client][date]:
            if client in dictionary:
                dictionary[client]+=float(dataset[client][date][product]["price"])
            else:
                dictionary[client]=float(dataset[client][date][product]["price"])



diagram = [go.Bar(x=list(dictionary.keys()),
                  y=list(dictionary.values()))]
plotly.offline.plot(diagram,filename="prices.html")

# Який найпопулярніший товар?
# Якого товару було куплено найменше?

popular=dict()
for client in dataset:
    for data in dataset[client]:
        for product in dataset[client][data]:
            if product in popular:
                popular[product] += dataset[client][data][product]['quantity']
            else:
                popular[product] = dataset[client][data][product]['quantity']

maximum = sorted(list(popular.values()))[-1]
minimum = sorted(list(popular.values()))[0]
for items in popular:
    if popular[items] == maximum:
        print('Найпопулярніший: ', items)
    if popular[items] == minimum:
        print('Не популярний: ', items)

# Який найдорожчий товар?

max_price=dict()

for client in dataset:
    for data in dataset[client]:
        for product in dataset[client][data]:
            if product in max_price:
                if max_price[product] < dataset[client][data][product]['price']:
                    max_price[product] = dataset[client][data][product]['price']
            else:
                max_price[product] = dataset[client][data][product]['price']

most_price = sorted(list(max_price.values()))[-1]

print(most_price)

# Якого товару, скільки покупців купляє? (графік)

products=set()
for name in dataset:
    for date in dataset[name]:
        for product in dataset[name][date]:
            products.add(product)
product_list=[]
quantity_list=[]
for product in products:
    count=0
    for name in dataset:
        for date in dataset[name]:
            if product in dataset[name][date]:
                count+=1
                break

    product_list.append(product)
    quantity_list.append(count)

graph=[go.Bar(x=product_list,y=quantity_list)]
plotly.offline.plot(graph,filename="quantity.html")

# Написати функціонал для додавання нових даних

def add_client_product(client_item=input('Client:'),data_item=input('Data:'),product_item=input('Product:'),q_item=input('Quantity:'),price_item=input('Price:')):

    if client_item in dataset:
        if data_item in dataset[client]:
            if product_item in dataset[client][data]:
                if q_item in dataset[client][data][product]:
                    if price_item in dataset[client][data][product][quantity]:
                        price_list=dataset[client][data][product][price]
                        price_list.append(price_item)
                    else:
                        dataset[client][data][product][quantity]=[price_item]
                else:
                    dataset[client][data][product]=[q_item]
            else:
                dataset[client][data] = [product_item]
        else:
            dataset[client]=[data_item]
    else:
        dataset=dict()
        dataset[client_item]={
            {data_item: {product_item: {'quantity': q_item, 'price': price_item}}}
                           }

add_client_product()
print(dataset)

file.close()