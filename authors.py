#Importing the modules
from selenium import webdriver
from time import sleep
import pandas as pd


class AuthorsInfo:
    def __init__(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference('permissions.default.image', 2)
        self.driver = webdriver.Firefox()

        url = "http://webapp1.dlib.indiana.edu/TEIgeneral/browse.do?type=creator&filter=A&brand=wright"

        self.driver.get(url)

        #Links of the authors on the page
        authors = self.driver.find_elements_by_xpath(
            "//h3[contains(@class, 'browseList')]/a")

        author_links = [link.get_attribute("href") for link in authors]

        #Initializing the List that will hold the data
        master_list = []

        for page in author_links:
            self.driver.get(page)

            item_books = self.driver.find_elements_by_class_name(
                "resultItemBOOK")

            for item in item_books:
                data_dict = {}

                #Extracting the details of the book
                title = item.find_element_by_xpath("//dd/h3").text
                author = item.find_element_by_xpath("//dd[2]").text
                pub_year = item.find_element_by_xpath("//dd[3]").text
                source = item.find_element_by_xpath("//dd[4]").text

                #Filling the Dict with the extracted data
                data_dict['Title'] = title
                data_dict['Author'] = author
                data_dict['Publication Year'] = pub_year
                data_dict['Source'] = source

                #Appending the colelcted data to our master_list
                master_list.append(data_dict)

        #Saving the collected data in an Excel file
        df = pd.DataFrame(master_list)
        df.to_excel('AutorsInfo.xlsx', engine='xlsxwriter')


AuthorsInfo()
"""
1. Index of fiction (simply from 0001 to 2887)
2. Title
3. Author
4. Publication Year
5. Source
6. Gender of the author
7. Source (e.g. a link) for point 6 (where did you find that information?)


"""