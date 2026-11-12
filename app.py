from rich import print

class User:
    all_users = []
    next_id = 1
    current_user = None

    def __init__(self, name, password):
            self.name = name
            self.password = password
            self.id = User.next_id
            User.next_id += 1
            User.all_users.append(self)
            self.cart = Cart()
            self.rewards_points = 0
            User.current_user = self
            print("\n[green]Account created![/green]\n")

    def signout(self):
        if User.current_user:
            User.current_user = None
        else:
            print("No user logged in.")

class Cart:
    def __init__(self):
        self.items = []
        self.rewards_points = 0

    def add_item(self, item):
        self.items.append(item)
        print(f"\n[green]{item.name} added to cart![/green]\n")

    def show_cart(self):
        if len(self.items) == 0:
            print("\n[yellow]Your cart is empty.[/yellow]\n")
        else:
            print("\n--- Your Cart ---")
            for item in self.items:
                print(f"{item.name} - ${item.price:.2f} ({item.calories} calories)")
            total_price = sum(item.price for item in self.items)
            print(f"\nTotal Price: ${total_price:.2f}\n")
            while True:
                user_input = input("\nPress 1 to checkout or 2 to return to the main menu: \n")

                if user_input == '1':
                    User.current_user.cart.checkout()
                    break
                elif user_input == '2':
                    break
                else:
                    print("\n[red]Invalid input. Try again.[/red]\n")
                    continue
    
    def checkout(self):
        if len(self.items) == 0:
            print("\n[yellow]Your cart is empty. Cannot proceed to checkout.[/yellow]\n")
        else:
            while True:

                user_input = input(f"You have {self.rewards_points} rewards points. You can save ${self.rewards_points / 100:.2f} on your order. Press 1 to use your rewards points or 2 to continue without using them.\n")
                if user_input == '1':
                    total_price = sum(item.price for item in self.items)
                    if self.rewards_points >= (total_price * 100):
                        self.rewards_points -= (total_price * 100)
                        total_price = 0
                    else:
                        total_price -= self.rewards_points / 100
                        self.rewards_points = 0
                        
                    
                elif user_input == '2':
                    total_price = sum(item.price for item in self.items)
                else:
                    print("\n[red]Invalid input. Try again.[/red]\n")
                    continue
        
                self.rewards_points += int(total_price * 10)
                print(f"\n[green]Checkout successful! Total Price: ${total_price:.2f}\nRewards Points Earned: {int(total_price * 10)} [/green]\n")
                self.items.clear()
                break


class Item:
    all_items = []
    next_id = 1

    def __init__(self, name, calories, price):
        self.name = name
        self.calories = calories
        self.price = price
        self.id = Item.next_id
        Item.next_id += 1
        Item.all_items.append(self)

class Dessert(Item):
    def __init__(self, name, calories, price, sugar_content):
        super().__init__(name, calories, price)
        self.sugar_content = sugar_content

class Drink(Item):
    def __init__(self, name, calories, price, fl_oz):
        super().__init__(name, calories, price)
        self.fl_oz = fl_oz

class Food(Item):
    def __init__(self, name, calories, price):
        super().__init__(name, calories, price)


Food("Classic Smash Burger", 650, 8.99)
Food("Chicken Sandwich", 550, 7.99)
Food("Veggie Burger", 480, 7.49)
Food("French Fries", 320, 3.49)
Food("Chicken Tenders", 600, 6.99)
Dessert("Chocolate Brownie", 350, 3.49, 28)
Dessert("Cheesecake", 420, 4.49, 32)
Dessert("Apple Pie", 310, 3.99, 22)
Drink("Cola", 150, 2.49, 16)
Drink("Lemonade", 180, 2.99, 16)
Drink("Iced Tea", 90, 2.49, 16)


def show_menu():
    print("[blue]Click the number of the item you want to add to your cart or type '0' to return to the main menu.[/blue]")

    print("\n--- Main Menu ---")
    n = 1
    food = "\n--- Food ---\n"
    dessert = "\n--- Desserts ---\n"
    drink = "\n--- Drinks ---\n"

    for item in Item.all_items:

        if type(item) == Food:
            food += (f"{n}. {item.name} - ${item.price} ({item.calories} calories)\n")
            n += 1

        elif type(item) == Dessert:
            dessert += (f"{n}. {item.name} - ${item.price} ({item.calories} calories, {item.sugar_content}g sugar)\n")
            n += 1
            
        elif type(item) == Drink:
            drink += (f"{n}. {item.name} - ${item.price} ({item.calories} calories, {item.fl_oz} fl oz)\n")
            n += 1

    print(food + dessert + drink)

    if User.current_user:
        while True:
            try:
                user_input = int(input("\nEnter the number of the item to add to your cart or type '0' to return: \n"))

            except ValueError:
                print("\n[red]Invalid input. Please enter a number or '0' to return.[/red]\n")
                continue

            if user_input == 0:
                return

            elif 1 <= user_input <= len(Item.all_items):
                User.current_user.cart.add_item(Item.all_items[user_input - 1])

            else:
                print("\n[red]Invalid input. Please enter a number or '0'.[/red]\n")
    else: 
        print("\n[yellow]You need to create an account to add items to your cart.[/yellow]\n")


while True:

    if User.current_user:

        print(f"""========================================================================
[ 1. Menu ]                   BURGER HAVEN              [ 2. Cart ({len(User.current_user.cart.items)}) ]
========================================================================

WELCOME TO BURGER HAVEN!
Freshly smashed beef, crisp local greens, and house-made sauces. Press 1
for our menu or press 2 to see your cart, press 3 to sign out, 
press "q" to quit.""")
        choice = input()

        if choice == '1':
            show_menu()

        elif choice == '2':
            User.current_user.cart.show_cart()
        elif choice == '3':
            User.current_user.signout()

        elif choice.lower() == 'q':
            print("\n[green]Thank you for visiting Burger Haven![/green]\n")
            break

    else:
        print(f"""========================================================================
[ 1. Menu ]                   BURGER HAVEN             [ 2. Create Acc ]
========================================================================

WELCOME TO BURGER HAVEN!
Freshly smashed beef, crisp local greens, and house-made sauces. Press 1
for our menu, press 2 to create an account to add items to your cart, 
press "q" to quit.""")
        choice = input()

        if choice == "1":
            show_menu()
        
        elif choice == '2':
            name = input("\nEnter your name: ")
            password = input("\nEnter your password: ")
            User(name, password)

        elif choice.lower() == 'q':
            print("\n[green]Thank you for visiting Burger Haven![/green]\n")
            break