import uuid 
import sys, os 

#Adding path to pycaboose module
sys.path.append('../')
from pycaboose import Value

#==============================Simple Bank Account Manager==============================#

# What can it do?
# ==> Update user name, email. View Account Details. 
# ==> Maintain account details and balance persistently using Pycaboose whilst perform account operations like Withdraw and Deposit.

def main():


    print("\n Welcome! This program will help you to maintain your account details.")
    print("\n Please update your bank details when you run this program for the first time.")
    print ("\n Enter the number corresponding to the option")

    while(True):

        #Setting up Pycaboose values for account balance, name and email
        balance = Value(0)
        name = Value("Pycaboose")
        email = Value("pycaboose@pycaboose.com")
        menu = 0
        menu = input("""
        1. Withdraw Money
        2. Deposit Money
        3. View Account Details
        4. Update Account Name
        5. Update Account Email
        6. Quit
        """)

        if menu == '1':

            withdraw_amount = int(input(" Enter amount to be Withdrawn: ")) 
            amount = int(input(" Enter amount to be Deposited: ")) 
            if balance.value >= withdraw_amount: 

                #Updating account balance, Pycaboose value will retrieve the most recent value for our variable
                balance.value = balance.value - withdraw_amount 
                print("\n Money Withdrawn is: ", withdraw_amount)
                print("\n Updated Balance is: ",balance.value)
                
            else:
                
                print("\n Operation cannot be completed due to insufficient balance!") 

        elif menu == '2':

            #Updating account balance after deposit
            amount = int(input(" Enter amount to be Deposited: ")) 
            balance.value = balance.value + amount 
            print("\n Amount Deposited is:",amount) 
            print("\n Updated Balance is: ",balance.value)

        elif menu == '3':

            # Displaying account details
            print("\n User {} has a balance of {}".format(name.value,balance.value))
            print("\n User Email Id is {}".format(email.value))

        elif menu == '4':

            #Updating account name 
            name_new = input(" Enter Updated name: ")
            name.value = name_new
            print("\n Updated Name is:",name.value)


        elif menu == '5':

            #Updating account email
            email_new = input(" Enter Updated EmailId: ")
            email.value = email_new
            print("\n Updated EmailId is:",email.value)

        elif menu == '6':

            #Break statment to quit loop
            print("\n Thank you!")
            break



#Driver Code
if __name__ == "__main__":
    main()
