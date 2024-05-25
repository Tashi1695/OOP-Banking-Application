###############################
# Tashi Dorji
# 1st year Electrical department
# 02230082
###############################
# REFERENCES
# @https://codecamp.com/
# @https://www.gemini.ai/

import random #import random to generate random numbers for Accounts. 
import os #import os to interact with system.

#Account class
class Account:
    # initializing process.
    def __init__(self, account_num, password, account_type, balance=0):
        self.account_num = account_number #Initialized account number 
        self.password = password # Initilaized password
        self.account_type = account_type #initialized account type
        self.balance = balance #Initialized account balance # Default is 0
    
    # To deposit
    def deposit(self, amount):
        self.balance += amount  # Dipositing to the account balance 
        print(f'Deposited Ngultrum{amount}. New balance: Ngultrum{self.balance}') # indicating successful diposite.
    
    # To withdraw 
    def withdraw(self, amount):
        if amount > self.balance: # checking whether withdral balance is > account balance 
            print('Insufficient funds.')# indicating withdral failure.
        else:
            self.balance -= amount # checking whether withral balance is <= account balance
            print(f'Withdrew Ngultrum{amount}. New balance: Ngultrum{self.balance}') # indecating successful withdrawl.
    
    # To check balance.
    def check_balance(self):
        return self.balance #Returning 

    # To transfer to another acc.
    def transfer(self, amount, recipient_account):
        if amount > self.balance: # checking whether transfer amount <= account balance
            print('Insufficient funds.')# indicating transfer failure
        else:
            self.withdraw(amount) #Withdrawing fransfered amount from current account
            recipient_account.deposit(amount) #Depositing the transfered amount into recipient's account
            print(f'Transferred Ngultrum{amount} to account {recipient_account.account_number}')# indicating sucessful transfer

    # To change account number
    def change_account_number(self, new_account_number):
        self.account_number = new_account_number # updating acc. num

    # To change password
    def change_password(self, new_password):
        self.password = new_password # updating acc password

# BusinessAccount 
#class inheriting from Account
class BusinessAccount(Account):
    def __init__(self, account_number, password, balance=0, business_name=""):
        super().__init__(account_number, password, "Business", balance) # Initialized the Account class
        self.business_name = business_name #initialized business name

# PersonalAccount 
# class inheriting from Account
class PersonalAccount(Account):
    def __init__(self, account_number, password, balance=0, owner_name=""):
        super().__init__(account_number, password, "Personal", balance) # Initialized the Account class
        self.owner_name = owner_name # Initialized account holder name 

# To save accounts
def save_account(account):
    accounts = load_accounts() 
    accounts[account.account_number] = account # add or update the account
    with open('accounts.txt', 'w') as f: # Opening account file
        for acc in accounts.values():# using for loop
            f.write(f'{acc.account_num},{acc.password},{acc.account_type},Ngultrum {acc.balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n')  # writing account detail to file

# To load accounts from file
def load_accounts():
    accounts = {}  # Initialized empty dictionary 
    if os.path.exists('accounts.txt'):  # checking accounts files 
        with open('accounts.txt', 'r') as f: # Opening accounts files
            for line in f: 
                parts = line.strip().split(',')  # Split line
                account_num, password, account_type, balance = parts[:4]  # Retrieving account details
                balance = float(balance.split()[1]) # Converting account balance to float  
                if account_type == "Business":  # checking acc type
                    business_name = parts[4] # Retrieving business_name
                    accounts[account_num] = BusinessAccount(account_num, password, balance, business_name) # Creating BusinessAccount object
                elif account_type == "Personal":  # checking if account type is personal account or not
                    owner_name = parts[5] #Retrieving holders name
                    accounts[account_num] = PersonalAccount(account_num, password, balance, owner_name)  # Creating PersonalAccount object
    return accounts # return 

# To create a new account
def create_account():
    account_num = str(random.randint(100000000, 999999999))# Generating a 9-digit account number randomly
    password = str(random.randint(1000, 9999)) # Generating  4-digit password randomly
    account_type = input('Enter account type (Business/Personal): ') # asking user-input/choice for account type
    
    if account_type == "Business":  # checking if account type is business or not
        business_name = input('Enter business name: ') # asking user-input for business_name
        account = BusinessAccount(account_num, password, business_name=business_name) # Creating BusinessAccount object
    else: # if account type is personal
        owner_name = input('Enter holder name: ') # asking user-input for account holder name. 
        account = PersonalAccount(account_num, password, owner_name=owner_name)  # Creating PersonalAccount object

    save_account(account) # Save the new account to file
    print(f'Account successfully created! Your account number is {account_num} and password is {password}')  # indicates successful create acc

# To login 
def login(accounts):
    account_num = input('Enter account number: ') # asking user-input  for acc no. 
    password = input('Enter password: ') # asking  user-input for account password
    
    account = accounts.get(account_num)  # Retrieve account from accounts dictionary
    if account and account.password == password: # checking whether account exist. # if the password is entered correctly
        print(f'Welcome, {account.account_type} account holder!') # Welcome message.
        return account  # Returning the logged-in account
    else: # if account does not exists, or if the password entered incorrectly
        print('Invalid passord or account number.') # indicating error in user-input
        return None # Returning None 

# To delete an account
def delete_account(account):
    accounts = load_accounts() # To load existing account fromthe  file
    if account.account_num in accounts:  # checking whether account exists or not
        del accounts[account.account_num] # To delete account.
        with open('accounts.txt', 'w') as f: # Opening account files in 'write' mode
            for acc in accounts.values(): # going over all the remaining accounts
                f.write(f"{acc.account_num},{acc.password},{acc.account_type},{acc.balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n")  # writing account detail to file
        print('Account successfully deleated!')  # indicating successful deletion of acc
    else:
        print('Account not found!')

# To change account detail
def change_account_details(account):
    print('\n1. Change Account Number\n2. Change Password') # displaying choices for changing acc detail
    choice = input('Enter choice: ') # asking user-input for their choice
    
    if choice == '1': # To change acc no. 
        new_account_num = input('Enter new account number: ') # asking user-input for new account number 
        accounts = load_accounts() # To load exist accounts from file
        if new_account_num in accounts: # checking if new account number exists or not. 
            print(' This account number already exists!') # if it existed 
        else:
            old_account_num = account.account_num  # To store old acc no.
            account.change_account_num(new_account_num) # To change acc no.
            save_account(account) # Save account with changed acc. no
            #To delete old accounts
            if old_account_num in accounts:
                del accounts[old_account_num] # To delete old account from dictionary
                with open('accounts.txt', 'w') as f:  # Opening account file
                    for acc in accounts.values(): # going over the remaining accounts again
                        f.write(f'{acc.account_number},{acc.password},{acc.account_type},{acc.balance},{getattr(acc, 'business_name', '')},{getattr(acc, 'owner_name', '')}\n')  # writing account detail to file
            print('Account number changed successfully!') # indicating successful acc no. change
    elif choice == '2': #  to change account password
        new_password = input('Enter new password : ') # asking user-input for the  new password.
        account.change_password(new_password) # To change Password
        save_account(account) # Save account with new password
        print('Password changed successfully!') # indicating successful in changing password
    else:
        print('Invalid choice.')

# Main function.
def main():
    while True: # Infinite loop
        print('\n1. Create Account\n2. Login\n3. Exit') # print options/choices 
        choice = input('Enter choice: ') # asking user-input choice 
        
        if choice == '1': # To create account 
            create_account() # Calling create account function
        elif choice == '2': # To Login
            accounts = load_accounts()  # Load exiting accounts
            account = login(accounts)  # Login
            if account: # checking if  login were successful or not
                while True:
                    print('\n1. Deposit\n2. Withdraw\n3. Check Balance\n4. Transfer\n5. Delete Account\n6. Change Account Details\n7. Logout') # Printing choice
                    trans_choice = input('Enter choice : ') # asking user-input  choice 
                    
                    if trans_choice == '1': # To deposit 
                        amount = float(input('Enter amount to deposit: ')) # asking user-input for amount to deposit
                        account.deposit(amount) # Deposit amount
                        save_account(account)# Save update account detail
                    elif trans_choice == '2': # To withdraw
                        amount = float(input('Enter amount withdral: '))# asking user-input for amount of withdral
                        account.withdraw(amount) # withdral amount
                        save_account(account)# Save update account detail
                    elif trans_choice == '3': # To verify acc balance 
                        print(f'Balance: Nu. {account.check_balance()}') # Prints current balance
                    elif trans_choice == '4': # To transfer  
                        recipient_num = input('Enter recipient acc. no.: ') # asking  user-input for recipent acc no. 
                        recipient = accounts.get(recipient_num)  # obtaining recipients acc
                        if recipient: # checking whether recipient account exist or not 
                            amount = float(input('Enter amount to transfer: ')) # asking user-input for amount of tranfer
                            account.transfer(amount, recipient)  # amount to transfer
                            save_account(account)# Sav1ing sender's updated account details
                            save_account(recipient) # Save recipient's update account informations
                        else:
                            print('Recipient account does not exist.')
                    elif trans_choice == '5': # To deleteaccount
                        delete_account(account)
                        break #exit loop
                    elif trans_choice == '6':# To change account information
                        change_account_details(account)
                    elif trans_choice == '7': # To Logout 
                        save_account(account) # save account details 
                        print('logged out')
                        break #exit loop
        elif choice == '3': # to exit the loop
            print('thank you.')
            break #exit loop
        else:
            print('Invalid option. try again')

# makes sure main-function run once it's executed
if __name__ == "__main__":
    main() # call main-function