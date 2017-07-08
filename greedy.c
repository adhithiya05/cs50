#include <stdio.h>
#include <cs50.h>
# include <math.h>
int main(void)
{
    int quarter;
    int dimes;
    int nickels;
    int coins;
    int balance;
    float c;
    
    do
    {
    printf("hii,how much change is owed ?\n");
    c = GetFloat ();
    }
    while (c<=0);
    int a =(int)round(c*100);
    
    quarter =(a/25);
    balance =(a%25);
     
    dimes =(balance/10);
    balance =(balance%10);
     
    nickels =(balance/5);
    balance =(balance%5);
     
    coins=(quarter + dimes + nickels + balance);
    printf("%d\n",coins);
}
