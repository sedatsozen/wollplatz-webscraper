from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import re

#Selenium is used for interaction with the webpage

class Scraper:
    def __init__(self, url): #Parameters that will be set in the moment of initilization
        self.url = url #Root page url
        self.driver = webdriver.Chrome() #Driver must be configured, might not work depending on your browser and its version
        self.driver.get(self.url) #Start from the root page
        self.count = 0 #Will be used for pagination later
        self.has_pagination = False #Will be used for pagination later

    def print_page_content(self):
        print(self.driver.page_source) #Get source HTML

    def get_elements_by_tag(self, element): #Get wanted elements with error handling
        try:
            searched_elements = self.driver.find_elements(By.TAG_NAME, value=element) #Search for the wanted element
            extracted_values = []

            for i in searched_elements:
                extracted_values.append(i.text) # Extract every matching value

            return extracted_values
        except NoSuchElementException:
            return "Not available" # The wanted element cannot be found, do not exit, just print this statement and move on

    def click_link(self, link_name):
        try:
            link = WebDriverWait(self.driver, 10).until( # Wait for page to load for 10 seconds, then try clicking on a link with the given name
                EC.presence_of_element_located((By.LINK_TEXT, link_name))
            )
            link.send_keys("\n") #Clicking action, link.click() does not work sometimes
        except:
            print("Does not exist (link)")

    def get_yarns_by_manufacturer(self, manufacturer):
        self.click_link(manufacturer) #Manufacturer names also contain a link to thier page, click on that

        yarn_specs = {"Hersteller": manufacturer, "Name": "", "Preis": "", "Lieferzeit": "", "Nadelstaerke": "", "Zusammenstellung": ""} #Specs of yarns
        searched_yarns = []

        self.get_rid_of_pagination(searched_yarns, yarn_specs) #Loop through every page

        return searched_yarns

    def get_yarns_in_page(self, searched_yarns, yarn_specs):
        yarns = self.get_elements_by_tag("h3") #Yarns inside a manufacturers page are represented as h3 tags
        yarns.pop() # An excess h3 tag which is not a yarn is gotten rid of
        print(yarns)

        for yarn in yarns:
            try:
                self.click_link(yarn) #Like manufacturers, yarn names are actually links
                specs = self.traverse_table() #Loop through the table in the bottom of the page to extract values
                yarn_specs["Name"] = yarn
                yarn_specs["Preis"] = self.driver.find_element(By.CLASS_NAME, "product-price-amount").text
                yarn_specs["Lieferzeit"] = "Not available"
                yarn_specs["Nadelstaerke"] = specs["Nadelstaerke"]
                yarn_specs["Zusammenstellung"] = specs["Zusammenstellung"]
                searched_yarns.append(yarn_specs.copy()) #Do not change the original dictionary, use a copy to avoid problems
                self.driver.back() #Go back to the manufacturers page
            except NoSuchElementException: #If yarn page gives an error
                print("Does not exist get yarns in page")
                self.driver.back()

    def traverse_table(self):
        wanted_specs = {"Nadelstaerke": "", "Zusammenstellung": ""} #Extractable values from the bottom table
        specs = self.get_elements_by_tag("td") #Table elements
        for spec in specs:
            if spec == "Nadelstärke":
                index = specs.index(spec) + 1 #[... ,"Nadelstaerke", "3 mm", ...], find the index of the word "Nadelstaerke", the element which is after this index is the mm value
                wanted_specs["Nadelstaerke"] = specs[index]
            if spec == "Zusammenstellung":
                index = specs.index(spec) + 1 #Same logic here
                wanted_specs["Zusammenstellung"] = specs[index]

        return wanted_specs

    def get_rid_of_pagination(self, searched_yarns, yarn_specs):
        try:
            # select = Select(self.driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_drpdnMaxItemsPerPage"))
            # select.select_by_value("96") #Deprecated, not very efficient

            test_url = self.driver.current_url #To construct new urls

            pagination = self.driver.find_element(By.CLASS_NAME, "paginavan").text #Find how many pages are paginated

            if pagination != "": #If there is no pagination (only a single page)
                limits = re.findall(r'\d+', pagination) #Extract number from "Seite x von y"
                pages = []
                for i in range(int(limits[0]), int(limits[1])): #Start and end values
                    pages.append(i)
                    i = i + 1
                pages.append(pages[-1] + 1)
                del pages[0] #Seite 1 von 4 -> pages = [2, 3, 4]
                print(pages)

                self.get_yarns_in_page(searched_yarns, yarn_specs)

                for page in pages: #Iterate through pages
                    new_url = test_url + "?page=" + str(page) #Link format is .../?page=2
                    print(new_url)
                    self.driver.get(new_url) #Go to next page
                    self.get_yarns_in_page(searched_yarns, yarn_specs)
                    if page == pages[-1]: #When at the last page
                        self.driver.get(test_url)
                self.go_to_root() #All pages of a manufacturer are searched, go back to root
            else:
                print("No pagination")
                self.get_yarns_in_page(searched_yarns, yarn_specs)
        except NoSuchElementException:
            print("Does not exist pagination")
            self.driver.back()

    def go_to_root(self):
        self.driver.get(self.url)

    def quit_browser(self):
        self.driver.quit()
