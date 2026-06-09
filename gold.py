# import pandas as pd
# from sqlalchemy import create_engine
# import os

# server = os.getenv("DB_SERVER", "localhost")
# database = "customer_churn_dwh"
# username = "sa"
# password = os.getenv("DB_PASSWORD", "12345")


# def gold():
#     from silver import silver

#     df = silver()

#     engine = create_engine(
#         f"mssql+pyodbc://{username}:{password}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
#     )

#     churn_table = df[["churn_category", "churn_reason", "customer_status"]]
#     payment_table = df[["payment_method", "contract", "paperless_billing"]]
#     service_table = df[
#         [
#             "phone_service",
#             "internet_service",
#             "internet_type",
#             "online_security",
#             "online_backup",
#             "device_protection_plan",
#             "premium_tech_support",
#             "streaming_tv",
#             "streaming_movies",
#             "streaming_music",
#             "unlimited_data",
#             "multiple_lines",
#             "offer",
#         ]
#     ]
#     address_table = df[["city", "zip_code", "latitude", "longitude"]]
#     customer_table = df[
#         ["customer_id", "age", "gender", "married", "number_of_dependents"]
#     ]

#     address_table.to_sql("address_dim", con=engine, if_exists="append", index=False)
#     churn_table.to_sql("churn_dim", con=engine, if_exists="append", index=False)
#     payment_table.to_sql("payment_dim", con=engine, if_exists="append", index=False)
#     service_table.to_sql("service_dim", con=engine, if_exists="append", index=False)
#     customer_table.to_sql("customer_dim", con=engine, if_exists="append", index=False)

#     customer_dim = pd.read_sql(
#         "SELECT customer_sk, customer_id FROM customer_dim", engine
#     )
#     service_dim = pd.read_sql(
#         "SELECT service_sk, phone_service, internet_service FROM service_dim", engine
#     )  # استخدم الأعمدة اللي بتميز الخدمة
#     address_dim = pd.read_sql(
#         "SELECT address_sk, zip_code FROM address_dim", engine
#     )  # أو الـ ID بتاع الـ address
#     payment_dim = pd.read_sql(
#         "SELECT payment_sk, payment_method, contract FROM payment_dim", engine
#     )
#     churn_dim = pd.read_sql("SELECT churn_sk, churn_category FROM churn_dim", engine)

#     # --- Mapping Address ---
#     addr_df = pd.read_sql("SELECT address_sk, zip_code FROM address_dim", engine)
#     addr_map = (
#         addr_df.drop_duplicates("zip_code")
#         .set_index("zip_code")["address_sk"]
#         .to_dict()
#     )
#     df["address_sk"] = df["zip_code"].map(addr_map)

#     # --- Mapping Customers ---
#     cust_df = pd.read_sql("SELECT customer_sk, customer_id FROM customer_dim", engine)
#     cust_map = (
#         cust_df.drop_duplicates("customer_id")
#         .set_index("customer_id")["customer_sk"]
#         .to_dict()
#     )
#     df["customer_sk"] = df["customer_id"].map(cust_map)

#     # --- Mapping Payment
#     pay_df = pd.read_sql(
#         "SELECT payment_sk, payment_method, contract FROM payment_dim", engine
#     )
#     pay_df["combined_key"] = pay_df["payment_method"] + "_" + pay_df["contract"]
#     pay_map = (
#         pay_df.drop_duplicates("combined_key")
#         .set_index("combined_key")["payment_sk"]
#         .to_dict()
#     )

#     df["payment_combined_key"] = df["payment_method"] + "_" + df["contract"]
#     df["payment_id_sk"] = df["payment_combined_key"].map(pay_map)

#     # --- Mapping Service ---
#     serv_df = pd.read_sql(
#         "SELECT service_sk, phone_service, internet_service FROM service_dim", engine
#     )
#     serv_df["combined_key"] = (
#         serv_df["phone_service"].astype(str)
#         + "_"
#         + serv_df["internet_service"].astype(str)
#     )
#     serv_map = (
#         serv_df.drop_duplicates("combined_key")
#         .set_index("combined_key")["service_sk"]
#         .to_dict()
#     )

#     df["service_combined_key"] = (
#         df["phone_service"].astype(str) + "_" + df["internet_service"].astype(str)
#     )
#     df["service_sk"] = df["service_combined_key"].map(serv_map)

#     # --- Mapping Churn ---
#     churn_df = pd.read_sql("SELECT churn_sk, churn_category FROM churn_dim", engine)
#     churn_map = (
#         churn_df.drop_duplicates("churn_category")
#         .set_index("churn_category")["churn_sk"]
#         .to_dict()
#     )
#     df["churn_sk"] = df["churn_category"].map(churn_map)

#     final_columns = [
#         "service_sk",
#         "address_sk",
#         "customer_sk",
#         "payment_id_sk",
#         "churn_sk",
#         "total_extra_data_charges",
#         "total_long_distance_charges",
#         "total_revenue",
#         "monthly_charge",
#         "total_charges",
#         "total_refunds",
#         "avg_monthly_gb_download",
#         "tenure_in_months",
#         "avg_monthly_long_distance_charges",
#         "number_of_referrals",
#     ]

#     df_final = df[final_columns]
#     df_final = df_final.drop_duplicates()

#     final_columns = [
#         "service_sk",
#         "address_sk",
#         "customer_sk",
#         "payment_sk",
#         "churn_sk",
#         "total_extra_data_charges",
#         "total_long_distance_charges",
#         "total_revenue",
#         "monthly_charge",
#         "total_charges",
#         "total_refunds",
#         "avg_monthly_gb_download",
#         "tenure_in_months",
#         "avg_monthly_long_distance_charges",
#         "number_of_referrals",
#     ]

#     if "payment_id_sk" in df_final.columns:
#         df_final = df_final.rename(columns={"payment_id_sk": "payment_sk"})

#     df_to_load = df_final[final_columns]

#     df_to_load.to_sql("fact_subscriptions", con=engine, if_exists="append", index=False)


# if __name__ == "__main__":
#     gold()

##------------------------------------------------------------#

import pandas as pd
from sqlalchemy import create_engine, text
import os
import time

# 1. دالة التأكد من وجود الداتابيز
def wait_for_db(conn_str, db_name="customer_churn_dwh"):
    base_conn = conn_str.replace(db_name, "master")
    engine_master = create_engine(base_conn, isolation_level="AUTOCOMMIT")
    
    print("Connecting to SQL Server...")
    for i in range(20):
        try:
            with engine_master.connect() as conn:
                exists = conn.execute(text(f"SELECT name FROM sys.databases WHERE name = '{db_name}'")).fetchone()
                if not exists:
                    print(f"Database {db_name} not found. Creating it...")
                    conn.execute(text(f"CREATE DATABASE {db_name}"))
                return create_engine(conn_str)
        except Exception as e:
            print(f"Attempt {i+1}/20: Waiting for SQL Server... ({e})")
            time.sleep(5)
    raise ConnectionError("Could not connect to SQL Server.")

# إعدادات الاتصال
server = os.getenv("DB_SERVER", "db")
database = "customer_churn_dwh"
username = "sa"
password = os.getenv("DB_PASSWORD", "YourStrongPassword123!")

conn_str = (
    f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}"
    "?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
)

def gold():
    from silver import silver
    df = silver()
    engine = wait_for_db(conn_str)

    # 2. مسح الجداول القديمة وبناؤها بالهيكل الصحيح (الضربة القاضية)
    with engine.begin() as conn:
        print("Forcing fresh Schema build (Drop and Recreate)...")
        
        # حذف الجداول بالترتيب لتجنب مشاكل العلاقات
        tables_to_drop = [
            "fact_subscriptions", "customer_dim", "address_dim", 
            "churn_dim", "payment_dim", "service_dim"
        ]
        for table in tables_to_drop:
            conn.execute(text(f"IF OBJECT_ID('{table}', 'U') IS NOT NULL DROP TABLE {table}"))

        print("Creating Tables...")
        
        conn.execute(text("""
            CREATE TABLE address_dim (
                address_sk INT IDENTITY(1,1) PRIMARY KEY,
                city NVARCHAR(255), zip_code NVARCHAR(255), latitude FLOAT, longitude FLOAT
            )
        """))

        conn.execute(text("""
            CREATE TABLE churn_dim (
                churn_sk INT IDENTITY(1,1) PRIMARY KEY,
                churn_category NVARCHAR(255), churn_reason NVARCHAR(MAX), customer_status NVARCHAR(255)
            )
        """))

        conn.execute(text("""
            CREATE TABLE payment_dim (
                payment_sk INT IDENTITY(1,1) PRIMARY KEY,
                payment_method NVARCHAR(255), contract NVARCHAR(255), paperless_billing NVARCHAR(255)
            )
        """))

        conn.execute(text("""
            CREATE TABLE service_dim (
                service_sk INT IDENTITY(1,1) PRIMARY KEY,
                phone_service NVARCHAR(255), 
                internet_service NVARCHAR(255), 
                internet_type NVARCHAR(255),
                online_security NVARCHAR(255), 
                online_backup NVARCHAR(255), 
                device_protection_plan NVARCHAR(255),
                premium_tech_support NVARCHAR(255), 
                streaming_tv NVARCHAR(255), 
                streaming_movies NVARCHAR(255),
                streaming_music NVARCHAR(255), 
                unlimited_data NVARCHAR(255), 
                multiple_lines NVARCHAR(255), 
                offer NVARCHAR(255)
            )
        """))

        conn.execute(text("""
            CREATE TABLE customer_dim (
                customer_sk INT IDENTITY(1,1) PRIMARY KEY,
                customer_id NVARCHAR(255), age INT, gender NVARCHAR(255), married NVARCHAR(255), number_of_dependents INT
            )
        """))

        conn.execute(text("""
            CREATE TABLE fact_subscriptions (
                fact_sk INT IDENTITY(1,1) PRIMARY KEY,
                service_sk INT, address_sk INT, customer_sk INT, payment_sk INT, churn_sk INT,
                total_extra_data_charges FLOAT, total_long_distance_charges FLOAT, total_revenue FLOAT,
                monthly_charge FLOAT, total_charges FLOAT, total_refunds FLOAT,
                avg_monthly_gb_download FLOAT, tenure_in_months INT, 
                avg_monthly_long_distance_charges FLOAT, number_of_referrals INT,
                foreign key (address_sk) references address_dim(address_sk),
                foreign key (customer_sk) references customer_dim(customer_sk),
                foreign key (payment_sk) references payment_dim(payment_sk),
                foreign key (churn_sk) references churn_dim(churn_sk),
                foreign key (service_sk) references service_dim(service_sk)
            )
        """))


    # 3. تحميل بيانات الـ Dimensions
    print("Uploading dimension data...")
    df[["city", "zip_code", "latitude", "longitude"]].drop_duplicates().to_sql("address_dim", engine, if_exists="append", index=False)
    df[["churn_category", "churn_reason", "customer_status"]].drop_duplicates().to_sql("churn_dim", engine, if_exists="append", index=False)
    df[["payment_method", "contract", "paperless_billing"]].drop_duplicates().to_sql("payment_dim", engine, if_exists="append", index=False)
    
    service_cols = ["phone_service", "internet_service", "internet_type", "online_security", "online_backup", 
                    "device_protection_plan", "premium_tech_support", "streaming_tv", "streaming_movies", 
                    "streaming_music", "unlimited_data", "multiple_lines", "offer"]
    df[service_cols].drop_duplicates().to_sql("service_dim", engine, if_exists="append", index=False)
    
    df[["customer_id", "age", "gender", "married", "number_of_dependents"]].drop_duplicates().to_sql("customer_dim", engine, if_exists="append", index=False)

    # 4. الـ Mapping لجلب الـ Keys (دلوقتي هتشتغل لأن العمود موجود)
    print("Mapping surrogate keys for Fact table...")
    
    addr_map = pd.read_sql("SELECT address_sk, zip_code FROM address_dim", engine).set_index("zip_code")["address_sk"].to_dict()
    df["address_sk"] = df["zip_code"].map(addr_map)

    cust_map = pd.read_sql("SELECT customer_sk, customer_id FROM customer_dim", engine).set_index("customer_id")["customer_sk"].to_dict()
    df["customer_sk"] = df["customer_id"].map(cust_map)

    pay_df = pd.read_sql("SELECT payment_sk, payment_method, contract FROM payment_dim", engine)
    pay_map = pay_df.set_index(["payment_method", "contract"])["payment_sk"].to_dict()
    df["payment_sk"] = df.set_index(["payment_method", "contract"]).index.map(pay_map)

    serv_df = pd.read_sql("SELECT service_sk, phone_service, internet_service FROM service_dim", engine)
    serv_map = serv_df.set_index(["phone_service", "internet_service"])["service_sk"].to_dict()
    df["service_sk"] = df.set_index(["phone_service", "internet_service"]).index.map(serv_map)

    churn_map = pd.read_sql("SELECT churn_sk, churn_category FROM churn_dim", engine).drop_duplicates("churn_category").set_index("churn_category")["churn_sk"].to_dict()
    df["churn_sk"] = df["churn_category"].map(churn_map)

    # 5. تحميل الـ Fact Table
    final_columns = [
        "service_sk", "address_sk", "customer_sk", "payment_sk", "churn_sk",
        "total_extra_data_charges", "total_long_distance_charges", "total_revenue",
        "monthly_charge", "total_charges", "total_refunds", "avg_monthly_gb_download",
        "tenure_in_months", "avg_monthly_long_distance_charges", "number_of_referrals"
    ]
    
    print("Uploading Fact table...")
    df[final_columns].drop_duplicates().to_sql("fact_subscriptions", engine, if_exists="append", index=False)
    print("--- SUCCESS: ETL Process Completed! ---")

if __name__ == "__main__":
    gold()