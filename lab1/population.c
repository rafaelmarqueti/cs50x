#include <cs50.h>
#include <stdio.h>
#include <math.h>

int main(void)
{
    int start_size;
    do
    {
        start_size = get_int("Start size:: ");
    }
    while (start_size < 9);

    
int end_size;
    do
    {
        end_size = get_int("End size:: ");
    }
    while (end_size < start_size);
    int year = 0;
    int n = start_size;
    int calculator = 0;

    
    if (start_size == end_size)
    {
        printf("Years: 0");
    }

   
    do
    {
        n = round(n + (n / 3) - (n / 4));
        year += 1;

    }
    while (n < end_size);
    printf("Years: %i",  year);

}