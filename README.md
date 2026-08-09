# Sales Data Analysis and Forecasting

## Project Overview

This project analyzes a global sales dataset to identify sales trends,
regional performance, product performance, profitability patterns and
future sales trends.

The project includes data cleaning, exploratory data analysis,
visualization, correlation analysis and machine learning-based
sales forecasting.

## Objectives

- Clean and prepare the raw sales dataset
- Handle missing values and incorrect data types
- Perform exploratory data analysis
- Analyze sales by category and region
- Analyze monthly sales and profit trends
- Identify top-performing products
- Study relationships between sales, profit, discount and shipping cost
- Build and evaluate sales forecasting models
- Present business-friendly insights

## Dataset

The dataset contains global sales transaction records.

### Dataset Details

- Original records: 51,298
- Cleaned records: 51,290
- Number of columns: 21
- Number of countries: 165
- Regions: America, Europe, Asia, Africa and Oceania

The dataset contains information about orders, customers, products,
sales, quantity, discount, profit, shipping cost and order priority.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Scikit-learn
- Jupyter Notebook
- Git
- GitHub

## Project Workflow

### 1. Data Loading

The raw sales dataset was loaded into Python using Pandas.

### 2. Data Cleaning

The dataset was inspected for:

- Missing values
- Duplicate records
- Invalid rows
- Incorrect data types
- Date formatting issues

The cleaned dataset contains 51,290 records.

The `Order Date` and `Ship Date` columns were converted to datetime
format.

### 3. Exploratory Data Analysis

Several visualizations were created to understand the dataset including:

- Sales distribution
- Total sales by category
- Regional analysis
- Monthly profit trend
- Top 10 products by sales
- Sales vs Profit
- Correlation heatmap
- Discount vs Profit

## Key Findings

### Category Performance

Technology generated the highest total sales among the three major
categories followed by Furniture and Office Supplies.

### Regional Analysis

The dataset contains records from 165 countries.

America has the highest number of records followed by Europe, Asia,
Africa and Oceania.

### Product Performance

Technology products particularly smartphones appear prominently among
the top-performing products by total sales.

Apple Smart Phone, Full Size was the highest-selling product among the
top 10 products analyzed.

### Sales and Profit

Sales and Profit have a correlation of approximately 0.485.

This indicates a moderate positive relationship between sales and profit.

### Discount and Profit

Discount and Profit have a correlation of approximately -0.316.

This indicates that higher discount levels are generally associated with
lower profitability.

### Shipping Cost and Sales

Sales and Shipping Cost have a correlation of approximately 0.77
indicating a strong positive relationship between the two variables.

## Sales Forecasting

Monthly sales were aggregated and used to build forecasting models.

The following models were tested:

1. Linear Regression
2. Random Forest Regression
3. Linear Regression with lag features

### Model Comparison

| Model                               |       MAE |      RMSE |     R² |
| ----------------------------------- | --------: | --------: | -----: |
| Linear Regression                   | 51,799.47 | 62,484.63 |  0.153 |
| Random Forest                       | 78,192.13 | 90,176.88 | -0.763 |
| Linear Regression with Lag Features | 36,656.75 | 43,625.22 |  0.598 |

### Final Model

The Linear Regression model with lag features was selected as the final
model.

The model used:

- Previous month's sales (`Lag_1`)
- Sales from two months earlier (`Lag_2`)
- Sales from the same month in the previous year (`Lag_12`)

### Final Model Performance

- MAE: 36,656.75
- RMSE: 43,625.22
- R²: 0.598

The final model performed better than the baseline Linear Regression and
Random Forest models.

## Project Structure

```text
Sales Performance Analytics/
│
├── Dataset/
│   ├── raw_sales.csv
│   └── cleaned_sales.csv
│
├── Notebook/
│   └── Sales_Analysis_and_Forecasting.ipynb
│
├── README.md
│
└── requirements.txt