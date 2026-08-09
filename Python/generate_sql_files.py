import pandas as pd

# CSV files and corresponding table names
tables = {
    "customers": "../Database/customers.csv",
    "products": "../Database/products.csv",
    "locations": "../Database/locations.csv",
    "shipping": "../Database/shipping.csv",
    "orders": "../Database/orders.csv"
}

for table_name, csv_path in tables.items():

    print(f"Processing {table_name}...")

    df = pd.read_csv(csv_path)

    # Convert dates only for orders table
    if table_name == "orders":

        # Convert mixed Order Date formats
        df["order_date"] = pd.to_datetime(
            df["order_date"],
            format="mixed",
            dayfirst=True,
            errors="coerce"
        ).dt.strftime("%Y-%m-%d")

        # Convert mixed Ship Date formats
        df["ship_date"] = pd.to_datetime(
            df["ship_date"],
            format="mixed",
            dayfirst=True,
            errors="coerce"
        ).dt.strftime("%Y-%m-%d")

    output_file = f"../Database/insert_{table_name}.sql"

    with open(output_file, "w", encoding="utf-8") as f:

        columns = ", ".join(df.columns)

        for _, row in df.iterrows():

            values = []

            for value in row:

                if pd.isna(value):
                    values.append("NULL")

                elif isinstance(value, str):
                    value = value.replace("'", "''")
                    values.append(f"'{value}'")

                else:
                    values.append(f"'{value}'")

            sql = (
                f"INSERT INTO {table_name} "
                f"({columns}) VALUES ({', '.join(values)});\n"
            )

            f.write(sql)

    print(f"✔ insert_{table_name}.sql created successfully!")

print("\nAll SQL files created successfully!")