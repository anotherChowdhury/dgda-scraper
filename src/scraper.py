from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

products_dict_list = []
page = 1


def get_rows(browser: webdriver) -> None:
    global page
    print("In get rows")

    if page > 884:
        rows = browser.find_elements_by_css_selector("#gridData > tbody tr")

        for row in rows:
            price = row.find_element_by_css_selector("td:nth-child(7)").text
            if price.strip() == "0":
                continue
            name_of_the_company = row.find_element_by_css_selector(
                "td:nth-child(2)"
            ).text
            brand_name = row.find_element_by_css_selector("td:nth-child(3)").text
            generic_name = row.find_element_by_css_selector("td:nth-child(4)").text
            strength = row.find_element_by_css_selector("td:nth-child(5)").text
            form = row.find_element_by_css_selector("td:nth-child(6)").text

            for_ = row.find_element_by_css_selector("td:nth-child(8)").text
            dar = row.find_element_by_css_selector("td:nth-child(9)").text

            product_dict = {
                "Company Name": name_of_the_company,
                "Brand Name": brand_name,
                "Generic Name": generic_name,
                "Strength": strength,
                "Form": form,
                "Price": price,
                "Used For": for_,
                "DAR": dar,
            }
            print(product_dict)
            products_dict_list.append(product_dict)

        browser.find_element_by_id("gridData_next").click()
        time.sleep(15)

        print("*" * 50)
        print("Loaded another page")
        print(f"Page Number : {page}")
        print("*" * 50)
        page = page + 1

    else:
        browser.find_element_by_id("gridData_next").click()
        time.sleep(5)

        print("*" * 50)
        print("Loaded another page")
        print(f"Page Number : {page}")
        print("*" * 50)
        page = page + 1


options = Options()
options.add_argument("--headless")

try:
    browser = webdriver.Firefox(
        executable_path="webdrivers/geckodriver", options=options
    )
    browser.get("https://dgda.gov.bd/index.php/registered-products/allopathic")

    while page < 1252:
        get_rows(browser)


except Exception as e:
    print(e)
    browser.quit()


fields = [
    "Company Name",
    "Brand Name",
    "Generic Name",
    "Strength",
    "Form",
    "Price",
    "Used For",
    "DAR",
]
# fields = ['bangla_name']
# name of csv file
filename = "dgda.csv"
# writing to csv file
with open(filename, "a") as csvfile:
    # creating a csv writer object
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    # writing headers (field names)
    # writer.writeheader()
    # writing data rows
    writer.writerows(products_dict_list)
