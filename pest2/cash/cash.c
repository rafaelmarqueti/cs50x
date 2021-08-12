#include <stdio.h>
#include <cs50.h>
#include <math.h>

float get_positive(void);
int cauculate_minimum_coins(int cents);

int main(void)
{
    float dollars = get_positive();
    int cents = round(dollars * 100);
    int coins = cauculate_minimum_coins(cents);
    printf("%d\n", coins);
}

float get_positive(void)
{
    float positive;
    
    do
    {
        positive = get_float("change owed: ");
    }
    while (positive < - 0);
    
    return positive;
}

int cauculate_minimum_coins(int cents)
{
    int coins = 0;

    if (cents >= 25)
    {
        coins += cents / 25;
        cents = cents % 25;
    }
    
    if (cents >= 10)
    {
        coins += cents / 10;
        cents = cents % 10;
    }
    
    if (cents >= 5)
    {
        coins += cents / 5;
        cents = cents % 5;
    }
    
    coins += cents;
    
    return coins;
}

