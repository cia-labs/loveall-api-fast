import mysql.connector
from mysql.connector import Error
from datetime import datetime
from passlib.context import CryptContext

pwd_context =CryptContext(schemes=["sha256_crypt"], deprecated="auto")
# MySQL connection configuration
config = {
    'user': 'root',
    'password': '',
    'host': '127.0.0.1',
    'database': 'lall'
}

# Sample user data
raw_users = [
    (1,"Admin", "admin@cialabs.tech", "admin", "CUSTOMER", 1),
    (2,"Surya Murugan", "surya@cialabs.com", "surya", "CUSTOMER", 1),
    (3,"John", "john@cialabs.tech", "john", "MERCHANT", 1),
    (4,"Raj", "raj@raj.tech", "raj", "CUSTOMER", 1),
    (5,"Kaushik Raju", "kaushik@cialabs.tech", "kaushik", "MERCHANT", 1),
    (6,"Tejus", "tejus@tejus.tech", "tejus", "CUSTOMER", 1),
    (7,"Thanmay", "thanmay@thanmay.tech", "thanmay", "MERCHANT", 1),
    (8,"Vamshita", "vamshita@vamshita.tech", "vamshita", "MERCHANT", 1),
]

stores = [
    (1,"Radisson Blu Atria", "5-star hotel", "1, Palace Road, Bengaluru, Karnataka 560001", "080 2220 5205", 5, "Admin",'{"gmaps":"https://maps.app.goo.gl/uRk7BKcwWvCaWJWa8" , "images" : { "primary": {} , "secondary": [] }}',"2024-03-15 16:14:59","2024-03-15 16:14:59"),
    (2,"The Ritz-Carlton", "5-star hotel", "99, Residency Rd, Shanthala Nagar, Ashok Nagar, Bengaluru, Karnataka 560025", "080 4914 8000", 3, "Admin",'{"gmaps":"https://maps.app.goo.gl/sgJ2z7p7A9enu84P9" , "images" : { "primary": {} , "secondary": [] }}',"2024-03-15 16:14:59","2024-03-15 16:14:59"),
    (3,"The Oberoi", "5-star hotel", "37-39, Mahatma Gandhi Road, Bengaluru, Karnataka 560001", "080 2558 5858", 7, "Admin",'{"gmaps":"https://maps.app.goo.gl/cJLYnMGm2pSHB6aU6" , "images" : { "primary": {} , "secondary": [] }}',"2024-03-15 16:14:59","2024-03-15 16:14:59"),
    (4,"Taj West End", "5-star hotel","37-39, Mahatma Gandhi Road, Bengaluru, Karnataka 560001", "080 2558 5858", 8, "Admin",'{"gmaps":"https://maps.app.goo.gl/bnNz3a68QtvVWXVY6" , "images" : { "primary": {} , "secondary": [] }}',"2024-03-15 16:14:59","2024-03-15 16:14:59"),
]

offer_type = [
    (1,"Weekday","offer that depicts only weekly","FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR","Admin","2024-03-15 16:14:59","2024-03-15 16:14:59",1),
    (2,"Weekend","offer that depicts only weekly","FREQ=WEEKLY;BYDAY=SA,SU","Admin","2024-03-15 16:14:59","2024-03-15 16:14:59",1),
    (3,"Daily","offer that depicts only weekly","FREQ=DAILY","Admin","2024-03-15 16:14:59","2024-03-15 16:14:59",1),
    (4,"Monthly","offer that depicts only weekly","FREQ=MONTHLY","Admin","2024-03-15 16:14:59","2024-03-15 16:14:59",1),
]

subscription_type = [
    (1,"Gold","Gold Subscription",10,'{}',"Admin","2024-03-15 16:14:59","2024-03-15 16:14:59"),
    (2,"Silver","Silver Subscription",5,'{}',"Admin","2024-03-15 16:14:59","2024-03-15 16:14:59"),
    (3,"Platinum","Platinum Subscription",15,'{}',"Admin","2024-03-15 16:14:59","2024-03-15 16:14:59"),
]

all_offers =  [
    (1,"Gold_Daily","Gold Offer for daily","2024-03-20","2024-03-31","09:00:00","22:00:00",10,1,1,3,5,1,1,"admin","2024-03-15 12:00:00","2024-03-15 12:00:00"),
    (2,"Gold_Weekend","Gold Offer for weekend","2024-03-20","2024-03-31","09:00:00","22:00:00",20,1,2,3,5,1,1,"admin","2024-03-15 12:00:00","2024-03-15 12:00:00"),

    (3,"Gold_Daily","Gold Offer for daily","2024-03-20","2024-03-31","09:00:00","22:00:00",10,1,1,3,3,2,1,"admin","2024-03-15 12:00:00","2024-03-15 12:00:00"),
    (4,"Gold_Weekend","Gold Offer for weekend","2024-03-20","2024-03-31","09:00:00","22:00:00",20,1,2,3,3,2,1,"admin","2024-03-15 12:00:00","2024-03-15 12:00:00"),
]


all_subscription = [
    (1,"Gold_Surya","ALL001",2,1,'6ba7b810-9dad-11d1-80b4-00c04fd430c8',"2024-03-15 12:00:00","2025-03-15 12:00:00",1,"admin","2024-03-15 12:00:00","2024-03-15 12:00:00"),
    (2,"Gold_Raj","ALL002",4,1,'F2D6E0E8-9998-4A83-B9AB-891806D8DD45',"2024-03-25 12:00:00","2025-03-25 12:00:00",1,"admin","2024-03-15 12:00:00","2024-03-15 12:00:00"),
    (3,"Gold_Tejus","ALL003",6,1,'57354895-0E87-4C7C-9809-0A1A9457162B',"2024-03-05 12:00:00","2025-03-05 12:00:00",1,"admin","2024-03-15 12:00:00","2024-03-15 12:00:00"),
]

all_transactions = [
    (1,1,1,1,20,1,5,1000,900,"123456123","2024-03-26 12:00:00","kausik","2024-03-26 12:00:00","2024-03-26 12:00:00"),
    (2,1,1,1,20,1,5,100,90,"123456124","2024-03-26 12:00:00","kausik","2024-03-27 12:00:00","2024-03-27 12:00:00"),
    (3,1,1,1,20,1,5,10000,9000,"123456125","2024-03-26 12:00:00","kausik","2024-03-28 12:00:00","2024-03-28 12:00:00"),
    (4,1,1,1,20,1,5,2000,1800,"123456126","2024-03-26 12:00:00","kausik","2024-03-15 12:00:00","2024-03-15 12:00:00"),
    (5,1,1,1,20,1,5,5000,4500,"123456127","2024-03-26 12:00:00","kausik","2024-03-16 12:00:00","2024-03-16 12:00:00"),
    (6,1,1,1,20,1,5,7000,6300,"123456128","2024-03-26 12:00:00","kausik","2024-03-17 12:00:00","2024-03-17 12:00:00"),
    (7,1,1,1,20,1,5,8000,7200,"123456129","2024-03-26 12:00:00","kausik","2024-03-18 12:00:00","2024-03-18 12:00:00"),
    (8,1,1,1,20,1,5,9000,900,"123456112","2024-03-26 12:00:00","kausik","2024-03-19 12:00:00","2024-03-19 12:00:00"),
    (9,1,1,1,20,1,5,6500,5850,"123456113","2024-03-26 12:00:00","kausik","2024-03-20 12:00:00","2024-03-20 12:00:00"),
]

users=[]
for user in raw_users:
    user_password = pwd_context.hash(user[3])
    user = (*user[:3], user_password, user[4], user[5])
    print(user)
    users.append(user)


# SQL query to insert a user
insert_query = "INSERT INTO `user` (id,name, email, password, role, is_active, creation_time, modification_time) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)"

try:
    # Connect to MySQL database
    connection = mysql.connector.connect(**config)

    if connection.is_connected():
        cursor = connection.cursor()

        # Insert each user into the table
        for user in users:
            user_data = (*user, datetime.now(), datetime.now())
            print(user_data)
            cursor.execute(insert_query, user_data)
            connection.commit()
        print("Users inserted successfully!")

        for store in stores:
            print(store)
            cursor.execute("INSERT INTO `store` (id, name, description, address, phone, merchant_id, created_by, meta_data,creation_time,modification_time) VALUES (%s,%s, %s, %s, %s, %s, %s, %s,%s,%s)", store)
            connection.commit()

        for offer in offer_type:
            print(offer)
            cursor.execute("INSERT INTO `offer_type` (id, name, description, recurrence_pattern, created_by, creation_time, modification_time,is_active) VALUES (%s,%s, %s, %s, %s, %s, %s,%s)", offer)
            connection.commit()
        for subscription in subscription_type:
            print(subscription)
            cursor.execute("INSERT INTO `subscription_type` (id, name, description, discount_rate, meta_data, created_by, creation_time, modification_time) VALUES (%s,%s, %s, %s, %s, %s, %s, %s)", subscription)
            connection.commit()
        
        for offer in all_offers:
            cursor.execute("INSERT INTO `offer` (id, name, description, start_date, end_date, start_time, end_time, discount_rate, priority,is_active, offer_type_id, merchant_id,store_id,subscription_type_id, created_by, creation_time, modification_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", offer)
            connection.commit()
        
        for subscription in all_subscription:
            cursor.execute("INSERT INTO `subscription` (id, name, sub_number, customer_id, subscription_type_id, uuid, start_date, end_date, enabled, created_by, creation_time, modification_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", subscription)
            connection.commit()
        
        for transaction in all_transactions:
            cursor.execute("INSERT INTO `transaction` (id, subscription_id, store_id, offer_id, discount_rate, customer_id, merchant_id, total_amount, offer_amount, bill_number, bill_date, created_by, creation_time, modification_time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", transaction)
            connection.commit()

except Error as e:
    print("Error while connecting to MySQL", e)

finally:
    # Close database connection
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

#delete from subscription_type where 1=1;delete from offer_type where 1=1;delete from store where 1=1;delete from user where 1=1;delete from offer where 1=1;delete from subscription where 1=1;delete from transaction where 1=1;delete from storage where 1=1;
