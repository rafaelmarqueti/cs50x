#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // nome
    string name = get_string("what is your name?\n");
    
    // nome imprimido
    printf("hello, %s\n" , name);
}

