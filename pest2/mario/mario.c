#include <stdio.h>
#include <cs50.h>

int get_heigth(void);

int main(void)
{
    int heigth = get_heigth();
    
   for (int i = 0; i < heigth; i++) 
   {
       int blocks = i + 1;
       int spaces = heigth - blocks;
       
       for ( int j = 0; j < spaces; j++)
       {
           printf(" ");
       }
      
      for (int j = 0; j < blocks; j++)
      {
          printf("#");
      }
      
      printf("\n");
   }
}

int get_heigth(void)
{
    int heigth;
    
    do
    {
        heigth = get_int("Heigth: ");
    }
    while(heigth < 1 || heigth > 8); 

    return heigth;
}

 
