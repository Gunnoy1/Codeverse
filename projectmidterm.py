# ===================== CONFIGURATION ===================== #
PASSWORD = "1234"
GOODS_FILES = "Goods.txt"
WALLET_FILES = "Wallet.txt"


# ===================== LOAD & SAVE ===================== #
def load_goods(goods_file):
    goods = {}
    try:
        with open(goods_file, 'r', encoding='utf-8') as stocks:
            for line in stocks:
                num, name, price, stock = line.strip().split(',')
                goods[int(num)] = {
                    'name': name,
                    'price': int(price),
                    'stock': int(stock)
                }
    except FileNotFoundError:
        print(f"⚠️ ไม่พบไฟล์ {goods_file}")
    return goods


def load_wallet(wallet_file):
    wallet = {}
    try:
        with open(wallet_file, 'r', encoding='utf-8') as fund:
            for line in fund:
                money, num = line.strip().split(',')
                wallet[int(money)] = int(num)
    except FileNotFoundError:
        print(f"⚠️ ไม่พบไฟล์ {wallet_file}")
    return wallet


def save_goods(goods, goods_file):
    with open(goods_file, 'w', encoding='utf-8') as stocks:
        for num, item in goods.items():
            stocks.write(f"{num},{item['name']},{item['price']},{item['stock']}\n")


def save_wallet(wallet, wallet_file):
    with open(wallet_file, 'w', encoding='utf-8') as fund:
        for coin, amount in wallet.items():
            fund.write(f"{coin},{amount}\n")


# ===================== PAYMENT ===================== #
def money_received(price):
    valid_money = [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]
    total = 0
    inserted_money = {}

    while total < price:
        entry = input(
            f"\n💰 โปรดใส่เงิน (ยอดคงเหลือ: {price - total} บาท)\n"
            f"   หรือกด 'c' เพื่อยกเลิก: "
        )
        if entry.lower() == 'c':
            print("❌ การชำระเงินถูกยกเลิก")
            return None, None

        try:
            amount = int(entry)
            if amount in valid_money:
                inserted_money[amount] = inserted_money.get(amount, 0) + 1
                total += amount
                print(f"➕ ใส่เงินเพิ่ม: {amount} บาท (รวม {total} บาท)")
            else:
                print(f"⚠️ กรุณาใส่เหรียญ/ธนบัตรที่ถูกต้อง: {valid_money}")
        except ValueError:
            print("⚠️ กรุณาใส่ตัวเลขเท่านั้น")

    return total, inserted_money


# ===================== CHANGE ===================== #
def calculate_change(change, wallet):
    change_back = {}
    for coin in sorted(wallet.keys(), reverse=True):
        count = min(change // coin, wallet.get(coin, 0))
        if count > 0:
            change_back[coin] = count
            change -= coin * count
            wallet[coin] -= count
    return change_back if change == 0 else None


def display_change(change_back):
    coins = [1, 2, 5, 10]  
    notes = [20, 50, 100, 200, 500, 1000] 
    
    coin_change = {k: v for k, v in change_back.items() if k in coins}
    note_change = {k: v for k, v in change_back.items() if k in notes}
    
    if coin_change:
        print("  🪙 เหรียญ:")
        for coin in sorted(coin_change.keys()):
            print(f"    {coin} บาท x {coin_change[coin]} เหรียญ")
    
    if note_change:
        print("  💵 ธนบัตร:")
        for note in sorted(note_change.keys()):
            print(f"    {note} บาท x {note_change[note]} ใบ")


# ===================== BUY GOODS ===================== #
def buy_goods(goods, wallet):
    while True:
        print("\n" + "=" * 50)
        print("🛒 รายการสินค้าในตู้จำหน่ายสินค้า")
        print("=" * 50)
        for num, item in goods.items():
            print(f"{num:2d}. {item['name']:<20} | ราคา: {item['price']:>5} บาท | คงเหลือ: {item['stock']:>3} ชิ้น")
        print("=" * 50)

        choice = input("กรุณาเลือกสินค้าหมายเลข (หรือ 'q' เพื่อออก): ").strip()

        if choice.lower() == 'q':
            print("กลับสู่เมนูหลัก...\n")
            break

        try:
            choice = int(choice)
            if choice not in goods:
                print("⚠️ หมายเลขสินค้าที่เลือกไม่ถูกต้อง กรุณาลองใหม่")
                continue

            item = goods[choice]
            if item['stock'] <= 0:
                print("❌ สินค้าหมด กรุณาเลือกสินค้าอื่น")
                continue

            print(f"\n🛍 คุณเลือก: {item['name']} ราคา {item['price']} บาท")

            total, inserted_money = money_received(item['price'])
            if total is None:
                continue

            change = total - item['price']
            wallet_backup = wallet.copy()

            # เพิ่มเงินที่ลูกค้าใส่เข้าตู้
            for coin, count in inserted_money.items():
                wallet[coin] = wallet.get(coin, 0) + count

            change_back = calculate_change(change, wallet)

            if change_back is None:
                print("\n❌ ไม่สามารถทอนเงินได้ กรุณารับเงินคืน:")
                for coin, count in inserted_money.items():
                    print(f"  {coin} บาท x {count} ใบ")
                    wallet[coin] -= count
                wallet = wallet_backup
                continue

           
            item['stock'] -= 1

         
            save_goods(goods, GOODS_FILES)
            save_wallet(wallet, WALLET_FILES)
            print("💾 อัปเดตข้อมูลในไฟล์เรียลไทม์...")

            print("\n✅ ซื้อสำเร็จ!")
            if change > 0:
                print(f"💰 เงินทอน: {change} บาท")
                display_change(change_back)
                input("\n🎉 กดปุ่มใดๆ เพื่อดำเนินการต่อ...")
            else:
                print("💰 ชำระเงินพอดี ไม่ต้องทอนเงิน")
                input("\n🎉 กดปุ่มใดๆ เพื่อดำเนินการต่อ...")

        except ValueError:
            print("⚠️ กรุณาใส่หมายเลขสินค้าให้ถูกต้อง")
            


# ===================== MANAGE MENU ===================== #
def manage_menu(goods, wallet):
    pwd = input("\n🔒 ใส่รหัสผ่านสำหรับเข้าสู่เมนูจัดการ: ")
    if pwd != PASSWORD:
        print("❌ รหัสผ่านไม่ถูกต้อง")
        return goods, wallet

    while True:
        print("\n" + "=" * 40)
        print("🔧 เมนูจัดการสินค้าและเงินในตู้")
        print("=" * 40)
        print("g) จัดสินค้าใส่ตู้")
        print("w) จัดเงินใส่ตู้")
        print("c) กลับสู่เมนูหลัก")
        print("=" * 40)

        choice = input("เลือก (g/w/c): ").lower()

        if choice == "g":
            print("\n📦 กรอกข้อมูลสินค้า (สูงสุด 9 รายการ)")
            for i in range(1, 10):
                name = input(f"ลำดับที่ {i} ชื่อสินค้า (กด Enter เพื่อหยุด): ").strip()
                if not name:
                    break
                try:
                    price = int(input("ราคา (บาท): "))
                    stock = int(input("จำนวน (ชิ้น): "))
                    goods[i] = {'name': name, 'price': price, 'stock': stock}
                except ValueError:
                    print("⚠️ กรุณาใส่ตัวเลขที่ถูกต้อง")
            save_goods(goods, GOODS_FILES)
            print("✅ บันทึกสินค้าเรียบร้อย")

        elif choice == "w":
            print("\n💵 กรอกจำนวนเหรียญ/ธนบัตรในตู้")
            for n in [1, 2, 5, 10, 20, 50, 100, 200, 500, 1000]:
                try:
                    stock = int(input(f"{n} บาท: "))
                    wallet[n] = stock
                except ValueError:
                    print("⚠️ กรุณาใส่ตัวเลขที่ถูกต้อง")
            save_wallet(wallet, WALLET_FILES)
            print("✅ บันทึกเงินเรียบร้อย")

        elif choice == "c":
            print("กลับสู่เมนูหลัก...\n")
            break

        else:
            print("⚠️ เลือกไม่ถูกต้อง")

    return goods, wallet


# ===================== SHUTDOWN ===================== #
def shutdown():
    pwd = input("\n🔒 ใส่รหัสปิดระบบ: ")
    if pwd == PASSWORD:
        confirm = input("คุณแน่ใจหรือไม่ที่จะปิดระบบ? (y/n): ")
        if confirm.lower() == 'y':
            print("🛑 ปิดระบบเรียบร้อย")
            exit(0)
        else:
            print("❎ ยกเลิกการปิดระบบ")
    else:
        print("❌ รหัสผิด")


# ===================== MAIN MENU ===================== #
def main_menu():
    goods = load_goods(GOODS_FILES)
    wallet = load_wallet(WALLET_FILES)

    while True:
        print("\n" + "=" * 50)
        print("📍 ตู้ขายสินค้าอัตโนมัติ".center(50))
        print("=" * 50)
        print("b) ซื้อสินค้า")
        print("m) จัดการสินค้า / เงิน")
        print("s) ปิดระบบ")
        print("=" * 50)

        choice = input("กรุณาเลือก (b/m/s): ").lower()

        if choice == "b":
            buy_goods(goods, wallet)
            

        elif choice == "m":
            goods, wallet = manage_menu(goods, wallet)

        elif choice == "s":
            shutdown()

        else:
            print("⚠️ พิมพ์ไม่ถูกต้อง")


# ===================== RUN ===================== #
if __name__ == "__main__":
    main_menu()
