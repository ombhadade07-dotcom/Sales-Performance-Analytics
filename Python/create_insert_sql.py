import pandas as pd

# Read CSV
df = pd.read_csv("../Database/customers.csv")

# Open output SQL file
with open("../Database/insert_customers.sql", "w", encoding="utf-8") as f:

    for _, row in df.iterrows():

        customer_id = str(row["customer_id"]).replace("'", "''")
        customer_name = str(row["customer_name"]).replace("'", "''")
        segment = str(row["segment"]).replace("'", "''")

        sql = f"""INSERT INTO customers
(customer_id, customer_name, segment)
VALUES
('{customer_id}', '{customer_name}', '{segment}');
"""

        f.write(sql)

print("insert_customers.sql created successfully!")