create database Bank_Application;
use Bank_Application;
create table user_details(
Account_No varchar(10) primary key,
Name varchar(50) not null,
DoB date not null,
City varchar(50) not null,
Contact_No varchar(10) not null,
Email varchar(320) unique not null,
Address varchar(255) not null
);
create table login_details(
Account_no varchar(10) primary key,
Password varchar(100) not null,
foreign key(Account_no) references user_details(Account_no)
on delete cascade
on update cascade
);
create table Status(
login_status bool not null,
logged_user varchar(10) not null
);
insert into Status(login_status,logged_user)
values
(0,'none');
create table Alloted_accounts(Account_No varchar(10),
foreign key (Account_No) references user_details(Account_No)
on delete cascade
on update cascade
);
create table Acc_balance(
Account_no varchar(10) primary key,
Balance int not null,
foreign key(Account_no) references user_details(Account_no)
on delete cascade
on update cascade
);
create table Transactions(     
TransactionID INT PRIMARY KEY AUTO_INCREMENT,     
Transaction_from varchar(10) not null,
Transaction_to varchar(10) not null,     
Type ENUM('Deposit','Withdrawal','Transfer'),     
Amount int,    
 Timestamp datetime
 );
  create table Activation(
Account_no varchar(10) primary key,
Activation_status enum('Active','Inactive'),
foreign key(Account_no) references user_details(Account_no)
on delete cascade
on update cascade
);