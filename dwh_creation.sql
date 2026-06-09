create table customer_dim (
customer_sk int identity(1,1) primary key,
customer_id varchar(50),
age int,
gender varchar(10),
married varchar(10),
number_of_dependents int,
)

create table address_dim(
address_sk int identity(1,1) primary key,
city varchar(50),
zip_code varchar(50),
latitude Decimal(10,7),
longitude Decimal(10,7)
)

create table churn_dim(
churn_sk int identity(1,1) primary key,
churn_category varchar(50),
churn_reason varchar(50),
customer_status varchar(50)
)

create table payment_dim(
payment_sk int identity(1,1) primary key,
payment_method varchar(50),
contract varchar(50),
paperless_billing varchar(50)
)

create table service_dim(
service_sk int identity(1,1) primary key,
phone_service varchar(50),
internet_service varchar(50),
internet_type varchar(50),
online_security varchar(50),
online_backup varchar(50),
device_protection_plan varchar(50),
premium_tech_support varchar(50),
streaming_tv varchar(50),
streaming_movies varchar(50),
streaming_music varchar(50),
unlimited_data varchar(50),
multiple_lines varchar(50),
offer varchar(50)
)


create table fact_subscriptions(
fact_service_sk int identity(1,1) primary key,
address_sk int,
customer_sk int,
payment_sk int,
churn_sk int,
service_sk int,
total_extra_data_charges int,
total_long_distance_charges Decimal(10,2),
total_revenue Decimal(10,2),
monthly_charge Decimal(10,2), 
total_charges Decimal(10,2), 
total_refunds Decimal(10,2),
avg_monthly_gb_download Decimal(10,2),
tenure_in_months int, 
avg_monthly_long_distance_charges Decimal(10,2),
number_of_referrals int,

foreign key (address_sk) references address_dim(address_sk),
foreign key (customer_sk) references customer_dim(customer_sk),
foreign key (payment_sk) references payment_dim(payment_sk),
foreign key (churn_sk) references churn_dim(churn_sk),
foreign key (service_sk) references service_dim(service_sk)
)

drop table service_dim
drop table customer_dim
drop table fact_subscriptions

drop table address_dim

truncate table churn_dim
truncate table service_dim
truncate table payment_dim
truncate table customer_dim
truncate table address_dim

select * from churn_dim

select * from fact_subscriptions


USE customer_churn_dwh;
 
SELECT 

    fk.name AS FK_name,

    tp.name AS parent_table,

    tr.name AS referenced_table

FROM sys.foreign_keys fk

JOIN sys.tables tp ON fk.parent_object_id = tp.object_id

JOIN sys.tables tr ON fk.referenced_object_id = tr.object_id;
 
