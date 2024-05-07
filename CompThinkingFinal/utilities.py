#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 19:14:21 2023

@author: Dgpowers
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def process_data(df):
    # Drop the columns that will not be used to clean the data
    df = df.drop(columns='Holiday_Flag''Fuel_Price''Unemployment''Temperature')
    
    # Convert the 'Date' column to datetime format, after countless attempts and scouring the internet it still doesn't plot the x-axis right later on
    df['Date'] = pd.to_datetime(df['Date'], infer_datetime_format=True, errors='coerce')

    # Drop rows where the 'Date' column couldn't be converted
    df = df.dropna(subset=['Date'])

    # Create a new column 'Year' based on the 'Date' column
    df['Year'] = df['Date'].dt.year
    
    # Create a new column 'Month' based on the 'Date' column
    df['Month'] = df['Date'].dt.month
    
    # Create a new column 'Day' based on the 'Date' column
    df['Day'] = df['Date'].dt.day

    # Convert the 'Store' column to category type
    df['Store'] = df['Store'].astype('category')
    
    return df

def read_data(file_path):

   # Reads data from the CSV file and returns a DataFrame object.

    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return None

def plot_sales_by_store(dataframe):
    
    # Plots total sales by store
    
    sales_by_store = dataframe.groupby("Store").Weekly_Sales.sum() / 1e6 # swith the $ values from table to show as x Millions 
    
    # Highlight the lowest 3 bars in red and the highest 3 bars in green
    n = 3
    top_n_stores = sales_by_store.nlargest(n).index
    bottom_n_stores = sales_by_store.nsmallest(n).index
    color_dict = {store: "green" if store in top_n_stores else "red" if store in bottom_n_stores else "darkgrey" for store in sales_by_store.index}
    # Create plot
    ax = sales_by_store.plot(kind="bar", figsize=(16, 8), title="Total Sales by Store", color=[color_dict[store] for store in sales_by_store.index]) # create the chart as a bar chart  
    ax.set_ylabel("Sales in Millions ($)") # Set lable title for y axis
    ax.yaxis.set_major_formatter('${x:,.0f}M') # Format the millions values on plot *same on following functions 
   
    plt.savefig("sales_by_store.png")
    plt.show()

def plot_sales_by_cpi(dataframe):
    
    # Plots total sales by CPI.

    sales_by_cpi = dataframe.groupby("CPI").Weekly_Sales.sum()
    cpi_values = sales_by_cpi.index
    sales_values = sales_by_cpi.values / 1e6 # convert sales to millions 
    plt.figure(figsize=(16, 8))
    plt.scatter(cpi_values, sales_values)
    plt.title("Total Sales by CPI")
    plt.xlabel("CPI")
    plt.ylabel("Sales in Millions ($)")
    plt.gca().yaxis.set_major_formatter('${x:,.0f}M') # format y-axis values in millions $
    
    plt.savefig("sales_by_cpi.png")
    plt.show()

def plot_sales_by_date(dataframe):

    # Plots total sales by date.

    sales_by_date = dataframe.groupby("Date").Weekly_Sales.sum()
    sales_by_date = sales_by_date.reset_index()
    sales_by_date['Date'] = pd.to_datetime(sales_by_date['Date'], format='%d-%m-%Y') 
    sales_by_date = sales_by_date.sort_values(by='Date', ascending=True) # Sort the DataFrame by Date in ascending order
    ax = sales_by_date.plot(x='Date', y='Weekly_Sales', figsize=(12, 6), title="Total Sales by Date") 
    ax.set_ylabel("Sales in Millions ($)")
    ax.yaxis.set_major_formatter('${x:,.0f}M')
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=30))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%Y'))
    plt.tight_layout()
    
    plt.savefig("sales_by_date.png")
    plt.show()

