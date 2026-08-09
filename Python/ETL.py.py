import pandas as pd

# ==========================
# Read Excel File
# ==========================
df = pd.read_excel(
    r"../Dataset/global_superstore_2016.xlsx",
    engine="openpyxl"
)

# Remove invalid rows
df = df.dropna(subset=["Customer ID"])

print("Dataset Shape After Cleaning:", df.shape)

# ==========================
# Customers Table
# ==========================
customers = (
    df[["Customer ID", "Customer Name", "Segment"]]
    .drop_duplicates()
    .sort_values("Customer ID")
)

customers.columns = [
    "customer_id",
    "customer_name",
    "segment"
]

customers.to_csv("../Database/customers.csv", index=False)

print("\nCustomers Table")
print("Total Rows:", len(customers))
print("Unique Customer IDs:", customers["customer_id"].nunique())
print("Missing Customer IDs:", customers["customer_id"].isna().sum())

# ==========================
# Products Table
# ==========================
products = (
    df[["Product ID", "Product Name", "Category", "Sub-Category"]]
    .drop_duplicates()
    .sort_values("Product ID")
)

products.columns = [
    "product_id",
    "product_name",
    "category",
    "sub_category"
]

products.to_csv("../Database/products.csv", index=False)

print("\nProducts Table")
print("Total Rows:", len(products))
print("Unique Product IDs:", products["product_id"].nunique())
print("Missing Product IDs:", products["product_id"].isna().sum())

# ==========================
# Locations Table
# ==========================
locations = (
    df[["Postal Code", "City", "Country"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

locations.insert(0, "location_id", range(1, len(locations) + 1))

locations.columns = [
    "location_id",
    "postal_code",
    "city",
    "country"
]

locations.to_csv("../Database/locations.csv", index=False)

print("\nLocations Table")
print("Total Rows:", len(locations))
print("Unique Location IDs:", locations["location_id"].nunique())
print("Missing Location IDs:", locations["location_id"].isna().sum())

print("\ncustomers.csv created successfully!")
print("products.csv created successfully!")
print("locations.csv created successfully!")



# ==========================
# Shipping Table
# ==========================

shipping = (
    df[["Ship Mode", "Order Priority"]]
    .drop_duplicates()
    .reset_index(drop=True)
)

shipping.insert(0, "shipping_id", range(1, len(shipping) + 1))

shipping.columns = [
    "shipping_id",
    "ship_mode",
    "order_priority"
]

shipping.to_csv("../Database/shipping.csv", index=False)

print("\nShipping Table")
print("Total Rows:", len(shipping))
print("Unique Shipping IDs:", shipping["shipping_id"].nunique())
print("Missing Shipping IDs:", shipping["shipping_id"].isna().sum())


# ==========================
# Create Location Lookup
# ==========================

location_lookup = locations.merge(
    df[["Postal Code", "City", "Country"]].drop_duplicates(),
    left_on=["postal_code", "city", "country"],
    right_on=["Postal Code", "City", "Country"],
    how="left"
)

# ==========================
# Create Shipping Lookup
# ==========================

shipping_lookup = shipping.merge(
    df[["Ship Mode", "Order Priority"]].drop_duplicates(),
    left_on=["ship_mode", "order_priority"],
    right_on=["Ship Mode", "Order Priority"],
    how="left"
)

# ==========================
# Orders Table
# ==========================

orders = df.copy()

# Add Location ID
orders = orders.merge(
    location_lookup[
        ["location_id", "Postal Code", "City", "Country"]
    ],
    on=["Postal Code", "City", "Country"],
    how="left"
)

# Add Shipping ID
orders = orders.merge(
    shipping_lookup[
        ["shipping_id", "Ship Mode", "Order Priority"]
    ],
    on=["Ship Mode", "Order Priority"],
    how="left"
)

# Select Columns
orders = orders[
    [
        "Row ID",
        "Order ID",
        "Order Date",
        "Ship Date",
        "Customer ID",
        "Product ID",
        "location_id",
        "shipping_id",
        "Sales",
        "Quantity",
        "Discount",
        "Profit",
        "Shipping Cost"
    ]
]

# Rename Columns
orders.columns = [
    "row_id",
    "order_id",
    "order_date",
    "ship_date",
    "customer_id",
    "product_id",
    "location_id",
    "shipping_id",
    "sales",
    "quantity",
    "discount",
    "profit",
    "shipping_cost"
]

# Save CSV
orders.to_csv(
    "../Database/orders.csv",
    index=False
)

print("\nOrders Table")
print("Total Rows:", len(orders))
print("Missing Location IDs:", orders["location_id"].isna().sum())
print("Missing Shipping IDs:", orders["shipping_id"].isna().sum())

print("\norders.csv created successfully!")