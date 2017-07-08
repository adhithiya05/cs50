/*
* Program name : caesar cipher
* Author : Adhithiya.R
 
* This program takes a non negative integer and 
  given input from the user.It rotates all the alphabets 
  of the input to n = (the given integer) number of places
  and prints it. 
     
* usage : ./caesar key
     
*/
 
#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
 
int main(int argc, string argv[])
{
    // Declare key
    int k;
     
    // Check for two commandsar line arguments
    if (argc == 2)
    {
        k = atoi(argv[1]);
    }
    else
    {
        printf("Please provide two command line arguments\n");
         
        return  1;
    }
         
          
    // To get plain text from user      
    string plain = GetString();
     
    // To cipher characters
    for (int i = 0, n = strlen(plain); i < n; i++)
    {
        
        // To cipher upper case characters
        if (isupper(plain[i]))
        {
            int cipher = ((((plain[i] + k) - 65) % 26) + 65);
            printf("%c",cipher);
        }
         
        // To cipher lower case characters
        else if (islower(plain[i]))
        {
            int cipher = ((((plain[i] + k) - 97) % 26) + 97); 
            printf("%c",cipher);  
        }
         
        // To print the rest unchanged
        else
        {
            printf("%c",plain[i]);
        }
    }
     
    // End of program
    printf("\n");
    return 0;
}
