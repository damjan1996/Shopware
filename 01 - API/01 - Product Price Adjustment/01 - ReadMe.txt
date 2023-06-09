Title: Python Product Price Updater

Description:
This repository contains a Python script designed to automate the updating of product prices on a website using API calls.
The script reads data from an Excel file, retrieves the current product information via the API, and updates the prices on the website if they differ from those in the Excel file.

Here's a detailed breakdown of the script:

1. read_data:
This function reads the product number and price information from an Excel file, cleans up the data, and returns it as a list of tuples.

2. login:
This function logs into the API using the provided access and secret keys, returning an access token for subsequent requests.

3. get_all_product:
This function retrieves all products' data using the API.

4. get_product_by_productNumber:
This function retrieves a specific product's information using its product number.

5. update_product_price:
This function updates a product's price, based on its product ID and the new gross price.

main:
This is the main function which combines the above functions to execute the full flow of the program:
reading the data, retrieving the products, and updating the prices as required.

The script logs progress and errors in a text file for easy tracking of the price updating process.

Ensure to replace placeholders in the constant variables (ACCESS_KEY, SECRET_KEY, URL, TAX, and FILE_PATH) with your actual values before running the script.
