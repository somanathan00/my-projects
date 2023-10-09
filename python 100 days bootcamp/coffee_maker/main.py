MENU = {
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
        },
        "cost": 1.5,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
        },
        "cost": 2.5,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
        },
        "cost": 3.0,
    }
}
money=0
resources = {
    "water": 300,
    "milk": 200,
    "coffee": 100,
}
def check_resources(order_ingredients):
    for item in order_ingredients:
        if order_ingredients[item] >= resources[item]:
            print(f"Sorry there is not enough {item}.")
            return False
    return True

def process_coins():
    print("Please insert coins.")
    total = int(input("how many quarters?: ")) * 0.25
    total += int(input("how many dimes?: ")) * 0.1
    total += int(input("how many nickles?: ")) * 0.05
    total += int(input("how many pennies?: ")) * 0.01
    return total

def transaction_is_successful(payment,actual_cost):
    if payment >= actual_cost:
        change=round(payment-actual_cost,2)
        print(f"Here is your change: {change}")
        global money
        money += actual_cost
        return True
    else:
        print(f"sorry that is not enough.money refunded")
        return False

def make_coffee(order_ingredients, choice):
    for item in order_ingredients:
        resources[item] -= order_ingredients[item]
    print(f"Here is your {choice} ☕️. Enjoy!")


is_on=True
while is_on:
    choice=input("What would you like? (espresso/latte/cappuccino):")
    if choice == "off":
        is_on=False
    elif choice == "report":
        print(f"water: {resources['water']}")
        print(f"milk: {resources['milk']}")
        print(f"coffee: {resources['coffee']}")
        print(f"money: {money}")
    else:
        drink=MENU[choice]
        if check_resources(drink["ingredients"]):
            payment= process_coins()
            if transaction_is_successful(payment,drink["cost"]):
                make_coffee(drink["ingredients"],choice)

