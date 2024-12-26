import pymysql.cursors
import cryptography
from random import randint
from time import strftime
from tabulate import tabulate
from sys import exit

# Connect to the database
connection = pymysql.connect(host='localhost',
                             user='',  #Enter your mysql username
                             password='',  #Enter your mysql password
                             database='Bank_Application',
                             )            

def menu():#THIS FUNCTION SHOWS THE MENU OF WHEN A USER IS LOGGED IN
    global logged_user,act_status
    print("MENU".center(20,"*"))
    print()
    print("1.Show Profile")
    print("2.Show Balance")
    print("3.Credit Amount")
    print("4.Debit Amount")
    print("5.Transfer Amount")
    print("6.Show Transactions")
    print("7.Change Password")
    print("8.Update Profile")
    print("9.Activate/Deactivate Account")
    print("10.Logout")
    print("11.Remove Account")
    print("12.Exit")
    action=input("Enter your choice: ").title()
    if action=="Show Profile" or action=="1":
        show_profile() 
    elif action=="Show Balance" or action=="2":
        show_balance()
    elif action=="Credit Amount" or action=="3":
        credit(logged_user)
    elif action=="Debit Amount" or action=="4":
        debit()
    elif action=="Transfer Amount" or action=="5":
        transfer()
    elif action=="Show Transactions" or action=="6":
        show_transactions()
    elif action=="Change Password" or action=="7":
        change_password()
    elif action=="Update Profile" or action=="8":
        update_profile()
    elif action=="Activate/Deactivate Account" or action=="9":
        activation()
    elif action=="Logout" or action=="10":
        logout()
    elif action=="Remove Account" or action=="11":
        remove_account()
    elif action=="Exit" or action=="12":
        exit("Thank you for using our Banking Application,hope to see you again")
    else:
        print("Invalid Input")
        menu()
def menu2():#THIS FUNCTIONS SHOWS THE MENU OF WHEN NO USER IS LOGGED IN
    print("MENU".center(20,"*"))
    print()
    print("Select Action:")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice=input("enter your choice: ").upper()
    if choice=="1" or choice=="REGISTER":
        registration()
    if choice=="2" or choice=="LOGIN":
        login()
    if choice=="3" or choice=="EXIT":
        exit("Thank you for using our Banking Application,hope to see you again")
def registration():#THIS FUNCTION REGISTERS USER AND STORES THEIR DATA IN THE DATABASE
    print("\nREGISTRATION PAGE:")
    with connection.cursor() as cursor:
        while(True):
            print("INSTRUCTION- Name can only contain alphabets and spaces")
            name=input("Enter your name:").title().strip()
            n=name
            n=n.replace(" ","")
            if (n.isalpha()):
                break
        dob=input("Enter your date of birth(YYYY-MM-DD): ").strip()
        city=input("Enter your city: ").strip().title()
        while(True):
            print("INSTRUCTION- Password should be NUMERIC and 6 digit long ")
            pword=input("enter your password: ").strip()
            if (pword.isdigit() and len(pword)==6):
                break
        while(True):
            balance=int(input("Enter initial balance: "))
            if not (balance<2000):
                break
        while(True):
            print("INSTRUCTION-Contact number should be 10 digit long")
            contact=input("Enter your contact number: ").strip()
            if (contact.isdigit() and len(contact)==10):
                break
        while(True):
            print("INSTRUCTION- The Email ID should be GMAIL or OUTLOOK")
            email=input("Enter your Email ID: ").lower().strip()
            if (email.endswith("gmail.com") or email.endswith("outlook.com")):
                break
                            
        address=input("Enter your residential address: ").strip()
        sql="select Account_No from Alloted_accounts"
        cursor.execute(sql)
        accounts=cursor.fetchall()
        while(True):
            acc=randint(1101000000,1101999999)
            if((f"{acc}",) not in accounts):
                break
        sql1="insert into user_details(Account_No,Name,DoB,City,Contact_No,Email,Address) values(%s,%s,%s,%s,%s,%s,%s)"
        val=(acc,name,dob,city,contact,email,address)
        cursor.execute(sql1,val)
        connection.commit()
        sql2="insert into login_details(Account_No,Password) values(%s,%s)"
        val2=(acc,pword)
        cursor.execute(sql2,val2)
        connection.commit()
        sql3="insert into Alloted_accounts(Account_No) values(%s)"
        val3=(acc)
        cursor.execute(sql3,val3)
        connection.commit()
        sql4="insert into acc_balance(Account_No,balance) values(%s,%s)"
        val4=(acc,balance)
        cursor.execute(sql4,val4)
        connection.commit()
        sql4="insert into Activation(Account_No,Activation_status) values(%s,%s)"
        val4=(acc,"Active")
        cursor.execute(sql4,val4)
        connection.commit()
        sql="insert into transactions(Transaction_from,Transaction_to,Type,Amount,Timestamp) values(%s,%s,%s,%s,%s)"
        timestamp=strftime("%Y-%m-%d %H:%M:%S")
        val=(acc,acc,"Deposit",balance,timestamp)
        cursor.execute(sql,val)
        connection.commit() 
        print("Registration Successfull")
        print(f"Your Account Number is: {acc}\n")
        login()
def login():#THIS FUNCTION LOGINS USER AND UPDATES THE LOGIN STATUS
    global logged_user,act_status
    with connection.cursor() as cursor:
        print("LOGIN PAGE:")
        sql="select Account_No from Alloted_accounts"
        cursor.execute(sql)
        accounts=cursor.fetchall()
        while(True):
            print("INSTRUCTION- account number should be 10 digit long")
            accno=input("Enter your account number: ").strip()
            if (accno.isdigit() and len(accno)==10):
                break
        if (f"{accno}",)  in accounts:
            pword=input("enter your password: ").strip()
            sql1="select Password from login_details where Account_No=%s"
            val=(accno)
            cursor.execute(sql1,val)
            password=cursor.fetchone()
            while (pword!=password[0]):
                print("Incorrect Password")
                pword=input("enter your password: ").lower()   
            if (pword==password[0]):
                print("Login Successfull")
                sql2=f"update Status set login_status=1 where login_status=0"
                sql3="update Status set logged_user=%s where logged_user='None'"
                val1=(accno)
                cursor.execute(sql2)
                cursor.execute(sql3,val1)
                connection.commit()
                logged_user=accno
                sql1=f"select Activation_status from Activation"  #THIS CODE CHECKS THE ACCOUNT ACTIVATION STATUS OF THE LOGGED USER
                cursor.execute(sql1)
                result=cursor.fetchone()
                act_status=result[0]
                
                menu()
        else:
            print("Unregistered User")
            registration()
def show_profile():#THIS FUNCTION FETCH USER DETAILS FROM THE DATABASE AND DISPLAYS THEM
    global logged_user
    if act_status=="Active":
        with connection.cursor() as cursor:
            sql2="select * from User_details where Account_No=%s"
            val=(logged_user)
            cursor.execute(sql2,val)
            result=cursor.fetchone()
            print()
            print("USER INFORMATION\n")
            print(f"Account Number: {result[0]}")
            print(f"Name: {result[1]}")
            print(f"Date of Birth: {result[2]}")
            print(f"City: {result[3]}")
            print(f"Contact Number: {result[4]}")
            print(f"Email ID: {result[5]}")
            print(f"Resedential Address: {result[6]}")
            input("\nPress ENTER to return to MENU:")
            menu()
    else:
        print("Your account is INACTIVE")
        print("Activate it to perform this operation")
        input("\nPress ENTER to return to MENU:")
        menu()  
def show_balance():
    global logged_user
    if act_status=="Active":
        with connection.cursor() as cursor:
            sql2="select balance from acc_balance where Account_No=%s"
            val=(logged_user)
            cursor.execute(sql2,val)
            result=cursor.fetchone()
            balance=result[0]
            print(f"Your account balance is {balance} Rs")
            input("\nPress ENTER to return to MENU:")
            menu()
    else:
        print("Your account is INACTIVE")
        print("Activate it to perform this operation")
        input("\nPress ENTER to return to MENU:")
        menu()        
def logout():#THIS FUNCTION LOGOUT USER AND UPDATES LOGIN STATUS
     with connection.cursor() as cursor:
            sql2=f"update Status set login_status=0"
            sql3="update Status set logged_user='None'"
            cursor.execute(sql2)
            cursor.execute(sql3)
            connection.commit()
            print("Logged Out Successfully")
            menu2()
def credit(iuser,amount=0,m="c"):
    if act_status=="Active":
        if m=="c":
            damount=int(input("Enter the amount you want to deposit: "))
        if m=="t":
            damount=amount
        with connection.cursor() as cursor:
            sql2="select balance from acc_balance where Account_No=%s"
            val=(iuser)
            cursor.execute(sql2,val)
            result=cursor.fetchone()
            balance=result[0]
            balance=balance+damount
            sql3="update acc_balance set balance=%s where Account_No=%s"
            val3=(balance,iuser)
            cursor.execute(sql3,val3)
            if m=="c":
                sql="insert into transactions(Transaction_from,Transaction_to,Type,Amount,Timestamp) values(%s,%s,%s,%s,%s)"
                timestamp=strftime("%Y-%m-%d %H:%M:%S")
                val=(iuser,iuser,"Deposit",damount,timestamp)
                cursor.execute(sql,val)
                connection.commit() 
                print(f"{damount} Rs has been successfully credited to your account")
                input("\nPress ENTER to return to MENU:")
                menu()
            connection.commit()
    else:
        print("Your account is INACTIVE")
        print("Activate it to perform this operation")
        input("\nPress ENTER to return to MENU:")
        menu()  
def debit(amount=0,m="d"):
    if act_status=="Active":
        global logged_user
        if m=="d":
            wamount=int(input("Enter the amount you want to withdraw: "))
        if m=="t":
            wamount=amount
        with connection.cursor() as cursor:
            sql2="select balance from acc_balance where Account_No=%s"
            val=(logged_user)
            cursor.execute(sql2,val)
            result=cursor.fetchone()
            balance=result[0]
            if wamount>balance:
                print("Insufficient Balance")
                input("\nPress ENTER to return to MENU:")
                menu()
            else:
                balance=balance-wamount
                sql3="update acc_balance set balance=%s where Account_No=%s"
                val3=(balance,logged_user)
                cursor.execute(sql3,val3)
                if m=="d":
                    sql="insert into transactions(Transaction_from,Transaction_to,Type,Amount,Timestamp) values(%s,%s,%s,%s,%s)"
                    timestamp=strftime("%Y-%m-%d %H:%M:%S")
                    val=(logged_user,logged_user,"Withdrawal",wamount,timestamp)
                    cursor.execute(sql,val)
                    connection.commit()
                    print(f"{wamount} Rs has been successfully debited to your account")
                    input("\nPress ENTER to return to MENU:")
                    menu()
                connection.commit()
    else:
        print("Your account is INACTIVE")
        print("Activate it to perform this operation")
        input("\nPress ENTER to return to MENU:")
        menu()  
def change_password():
    if act_status=="Active":
        global logged_user
        with connection.cursor() as cursor:
            sql1="select Password from login_details where Account_No=%s"
            val=(logged_user)
            cursor.execute(sql1,val)
            result=cursor.fetchone()
            cpass=result[0]
            password=input("Enter your current password: ")
            while(password!=cpass):
                print("Incorrect password")
                password=input("Enter your current password again: ")
                
            if password==cpass:
                while(True):
                    print("INSTRUCTION- Password should be NUMERIC and 6 digit long ")
                    npass=input("Enter your new password: ").strip()
                    if (npass.isdigit() and len(npass)==6):
                        break
                sql2="update login_details set Password=%s where Account_No=%s"
                val=(npass,logged_user)
                cursor.execute(sql2,val)
                connection.commit()
                print("Your password has been updated successfully")
                input("\nPress ENTER to return to MENU:")
                menu()
    else:
        print("Your account is INACTIVE")
        print("Activate it to perform this operation")
        input("\nPress ENTER to return to MENU:")
        menu()  
def update_profile():
    if act_status=="Active":
        global logged_user
        print("What do you want to update?")
        print("1.Name")
        print("2.Date of Birth")
        print("3.City")
        print("4.Contact Number")
        print("5.Email ID")
        print("6.Residential Address")
        print("7.Exit")
        action=input("Enter your choice: ").title()
        with connection.cursor() as cursor:

            if action=="Name" or action=="1":
                while(True):
                    print("INSTRUCTION- Name can only contain alphabets and spaces")
                    name=input("Enter your new name:").title().strip()
                    n=name
                    n=n.replace(" ","")
                    if (n.isalpha()):
                        break
                sql1="update user_details set Name=%s where Account_No=%s"
                val=(name,logged_user)
                cursor.execute(sql1,val)
                print("Your name has been updated successfully")
            elif action=="Date Of Birth" or action=="2":
                dob=input("Enter your date of birth(YYYY-MM-DD): ").strip()
                sql1="update user_details set DoB=%s where Account_No=%s"
                val=(dob,logged_user)
                cursor.execute(sql1,val)
                print("Your Date of Birth has been updated successfully")
            elif action=="City" or action=="3":
                city=input("Enter your city: ").strip()
                sql1="update user_details set City=%s where Account_No=%s"
                val=(city,logged_user)
                cursor.execute(sql1,val)
                print("Your City has been updated successfully")
            elif action=="Contact Number" or action=="4":
                while(True):
                    print("INSTRUCTION-Contact number should be 10 digit long")
                    contact=input("Enter your contact number: ").strip()
                    if (contact.isdigit() and len(contact)==10):
                        break
                sql1="update user_details set Contact_No=%s where Account_No=%s"
                val=(contact,logged_user)
                cursor.execute(sql1,val)
                print("Your Contact Number has been updated successfully")
            elif action=="Email Id" or action=="5":
                while(True):
                    print("INSTRUCTION- The Email ID should be GMAIL or OUTLOOK")
                    email=input("Enter your Email ID: ").lower().strip()
                    if (email.endswith("gmail.com") or email.endswith("outlook.com")):
                        break
                sql1="update user_details set Email=%s where Account_No=%s"
                val=(email,logged_user)
                cursor.execute(sql1,val)
                print("Your Email ID has been updated successfully")
            elif action=="Residential Address" or action=="6":
                address=input("Enter your residential address: ").strip()
                sql1="update user_details set Address=%s where Account_No=%s"
                val=(address,logged_user)
                cursor.execute(sql1,val)
                print("Your Residential Address has been updated successfully")
            elif action=="Exit" or action=="7":
                menu()
            else:
                print("Invalid Input")
            if action!="7" or action!="Exit":
                choice=input("Do you want to update anything else?(y/n)").lower().strip()
                if choice=="y":
                    update_profile()
                if choice=="n":
                    connection.commit()
                    input("\nPress ENTER to return to MENU:")
                    menu()
    else:
        print("Your account is INACTIVE")
        print("Activate it to perform this operation")
        input("\nPress ENTER to return to MENU:")
        menu()  
def transfer():
    if act_status=="Active":
        global logged_user
        with connection.cursor() as cursor:
            sql="select Account_No from Alloted_accounts"
            cursor.execute(sql)
            accounts=cursor.fetchall()
            reciever=input("Enter the reciever's account number: ").strip()
            while((f"{reciever}",)  not in accounts):
                print(f"Account number {reciever} does not exist")
                reciever=input("Enter the reciever's account number again: ").strip()
            tamount=int(input("Enter the amount you want to transfer: "))
            debit(tamount,"t")
            credit(reciever,tamount,"t")
            sql="insert into transactions(Transaction_from,Transaction_to,Type,Amount,Timestamp) values(%s,%s,%s,%s,%s)"
            timestamp=strftime("%Y-%m-%d %H:%M:%S")
            val=(logged_user,reciever,"Transfer",tamount,timestamp)
            cursor.execute(sql,val)
            connection.commit()
            print(f"{tamount} Rs has been successfully transferred to account number-{reciever}")
            input("\nPress ENTER to return to MENU:")
            menu()   
    else:
        print("Your account is INACTIVE")
        print("Activate it to perform this operation")
        input("\nPress ENTER to return to MENU:")
        menu()       
def show_transactions():
    if act_status=="Active":
        global logged_user
        with connection.cursor() as cursor:
            sql="select * from transactions where transaction_from =%s or transaction_to=%s"
            val=(logged_user,logged_user)
            cursor.execute(sql,val)
            result=cursor.fetchall()
            print(tabulate(result,headers=['TID','Transaction_from', 'Transaction_to','Type','Amount','Timestamp']))
            input("\nPress ENTER to return to MENU:")
            menu()
    else:
        print("Your account is INACTIVE")
        print("Activate it to perform this operation")
        input("\nPress ENTER to return to MENU:")
        menu()    
def activation():
    global act_status
    print("Choose action:")
    print("1.Activate account")
    print("2.Deactivate account")
    print("3.Exit")
    choice=input("Enter your choice: ")
    with connection.cursor() as cursor:  
        if choice=="1" or choice=="Activate account":
            sql2="update Activation set Activation_status=%s where Account_No=%s"
            val2=("Active",logged_user)
            cursor.execute(sql2,val2)
            connection.commit()
            act_status="Active"             
            print("Your account has been activated successfully")
            input("\nPress ENTER to return to MENU:")
            menu()
        if choice=="2" or choice=="Deactivate account":
            sql2="update Activation set Activation_status=%s where Account_No=%s"
            val2=("Inactive",logged_user)
            cursor.execute(sql2,val2)
            connection.commit()
            act_status="Inactive"             
            print("Your account has been deactivated successfully")
            input("\nPress ENTER to return to MENU:")
            menu()
        if choice=="3" or choice=="Exit":
            menu()
def remove_account():
    global logged_user
    pword=input("enter your password: ").strip()
    sql1="select Password from login_details where Account_No=%s"
    val=(logged_user)
    cursor.execute(sql1,val)
    password=cursor.fetchone()
    if pword==password[0]:
        print("WARNING-Your account and all the data related to it will be deleted")
        choice=input("Do you still want to continue(yes/no)")
        if choice=="yes":
            sql="delete from user_details where Account_No=%s"
            val=(logged_user)
            cursor.execute(sql,val)
            logout()
            menu2()
        elif choice=="no":
            input("\nPress ENTER to return to MENU:")
            menu()
    else:
        print("Incorrect password,You will redirected to menu")
        menu()

print("WELCOME TO OUR BANK APPLICATION".center(50,"_"))
print()
with connection.cursor() as cursor:
    sql1=f"select login_status,logged_user from status"  #THIS CODE CHECKS IF A USER IS ALREADY LOGGED IN OR NOT
    cursor.execute(sql1)
    result=cursor.fetchone()
    if(result[0]==1):
        logged_user=result[1]
        sql1=f"select Activation_status from Activation"  #THIS CODE CHECKS THE ACCOUNT ACTIVATION STATUS OF THE LOGGED USER
        cursor.execute(sql1)
        result=cursor.fetchone()
        act_status=result[0]
        menu()
    else:
        menu2()
