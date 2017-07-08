#include <stdio.h>
#include <cs50.h>
int main(void)
{
    int h;
    do
    {
    printf("Height: ");
    h = GetInt();
    }
    while (h < 0 || h > 23);
     
    for (int n = 0; n < h; n ++)
    {
        for (int space = 0; space < h-n-1; space ++)
        {
        printf(" ");
        }
            for (int hash = 0; hash < n+2; hash ++)
            {
            printf("#");
            }
            printf("\n");
    }
}
