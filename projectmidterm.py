# ======== Configuration File ======== #
Password = "1234"
Goods_Files = "Goods.txt"
Wallet_Files = "Wallet.txt"

# ============Save / Load============== #
def load_goods(Goods_Files):
    goods = {}
    with open(Goods_Files, 'r') as stocks:
        for line in stocks:
            num, name, price, stock = line.strip().split(',')
            goods[int(num)] = {
                'name': name,
                'price': int(price),
                'stock': int(stock)
            }   
    return goods
            
def load_Wallet(Wallet_Files):
    wallet = {}
    with open(Wallet_Files, 'r') as Money:
        for line in Money:
            Coin, num = line.strip().split(',')
            wallet[int(Coin)] = [int(num)]
    return wallet
def save_goods(goods, Goods_Files):
    with open(Goods_Files, 'w') as stocks:
        for num, item in goods.items():
            stocks.write(f"{num},{item['name']},{item['price']},{item['stock']}\n")
def save_wallet(wallet, Wallet_Files):
    with open(Wallet_Files, 'w') as Money:
        for coin, amount in wallet.items():
            Money.write(f"{coin},{amount[0]}\n")
            
# =========== Payment ============ #
def 
            
            

            
         
        
        
