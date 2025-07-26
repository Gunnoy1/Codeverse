import random

print("🎯 ══════ NUMBER GUESSING QUEST ══════ 🎯")
print("🎮 (1) WARRIOR MODE 🗡️  -- 🌟 (2) ROOKIE MODE 🛡️")
mode = int(input("⚔️ Choose your difficulty: "))
print()

def game(target, num):
    for i in range(num, -1, -1):
        try:
            user_input = int(input("🔮 Cast your guess: "))
        except ValueError:
            print("⚠️ Magic failed! Enter numbers only!")
            continue
            
        print()
        if user_input == target:
            print(f"🏆 ✨ VICTORY ACHIEVED! ✨ 🏆")
            print(f"🎊 You have conquered the number! 🎊")
            return
        elif user_input > target:
            if i > 0:
                print(f"🔥 Too powerful! Aim lower! 📉")
                print(f"⚡ {i} magic attempts remaining! ⚡")
            else:
                print(f"🔥 Too powerful! Aim lower! 📉")
        elif user_input < target:
            if i > 0:
                print(f"❄️ Too weak! Channel more energy! 📈") 
                print(f"⚡ {i} magic attempts remaining! ⚡")
            else:
                print(f"❄️ Too weak! Channel more energy! 📈")
                
    print("💀 ═══ QUEST FAILED! ═══ 💀")
    print(f"🔍 The sacred number was: {target}")
          
if mode == 1:
    target = random.randint(1, 40)
    print("⚔️ WARRIOR CHALLENGE: Guess between 1-40 ⚔️")
    print("🗡️ You have 5 battle attempts!")
    game(target, 4)
     
elif mode == 2:
    target = random.randint(1, 20)
    print("🛡️ ROOKIE TRAINING: Guess between 1-20 🛡️")
    print("🌟 You have 3 practice attempts!")
    game(target, 2)