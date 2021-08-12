QUARTER = 25
DIME = 10
NICKEL = 5


def main():
    dollars = get_positive()
    cents = calculate_cents(dollars)
    coins = calculate_minimum_coins(cents)
    print(coins)
    
    
def get_positive():
    while True:
        try:
            value = float(input("change owed: "))
            if value > 0:
                return value
        except ValueError:
            continue
        
        
def calculate_cents(dollars):
    return round(dollars * 100)
    
    
def calculate_minimum_coins(cents):
    coins = 0
    
    coins, cents = calculate_coins_value(coins, cents, QUARTER)
    coins, cents = calculate_coins_value(coins, cents, DIME)
    coins, cents = calculate_coins_value(coins, cents, NICKEL)
    coins += cents
    
    return coins
    
    
def calculate_coins_value(coins, cents, value):
    if (cents >= value):
        coins += cents // value
        cents = cents % value
        
    return coins, cents
    
    
main()
