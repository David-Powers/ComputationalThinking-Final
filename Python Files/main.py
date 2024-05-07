#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May  1 22:16:18 2023

@author: Dgpowers
"""
import utilities

# Read data from CSV file
file_path = "Walmart Data Analysis and Forcasting.csv"
dataframe = utilities.read_data(file_path)

# Plot sales by store
utilities.plot_sales_by_store(dataframe)

# Plot sales by cpi
utilities.plot_sales_by_cpi(dataframe)

# Plot sales by date
utilities.plot_sales_by_date(dataframe)
