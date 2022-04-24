import sqlite3
import ast
import csv
import pandas as pd

class Database: #Custom local database class for simplicity
    def __init__(self, data):
        self.already_created = False #To prevent creating an already existing database
        try:
            self.data = data #yarns.txt
            self.connection = sqlite3.connect("searched_yarns.db", check_same_thread=False) #Create a database
            self.cursor = self.connection.cursor() #Init cursor
            self.cursor.execute( #Create a fitting table for the yarns inside the database
                """CREATE TABLE yarns (Hersteller text, Name text, Preis text, Lieferzeit text, Nadelstaerke text, Zusammenstellung text)""")
        except sqlite3.OperationalError: #If database is already created
            self.already_created = True
            print("Database already exists")
            self.connection = sqlite3.connect("searched_yarns.db", check_same_thread=False) #Connect with the existing database
            self.cursor = self.connection.cursor()

    def convert_data(self): #Convert txt data to list of dict
        with open(self.data) as f:
            yarns = f.read()

        yarns_list = sum(ast.literal_eval(yarns), []) #Convert list formatted string to list
        return yarns_list

    def insert_into_database(self):
        if self.already_created is False: #If the database is already created, do not do this step. Website updates are not taken into consideration
            yarns_list = self.convert_data()
            for yarn in yarns_list: #For every yarn
                self.cursor.execute("INSERT INTO yarns VALUES (:Hersteller, :Name, :Preis, :Lieferzeit, :Nadelstaerke, :Zusammenstellung)"
                                    , {"Hersteller": yarn["Hersteller"], "Name": yarn["Name"],
                                       "Preis": yarn["Preis"], "Lieferzeit": yarn["Lieferzeit"], "Nadelstaerke": yarn["Nadelstaerke"],
                                       "Zusammenstellung": yarn["Zusammenstellung"]})
                self.connection.commit()

            self.cursor.execute("SELECT * FROM yarns") #Get every value
            self.cursor.fetchall()
            self.connection.close()

    def write_to_csv(self): #Write yarns into csv for later usage
        yarns = self.convert_data()
        keys = yarns[0].keys() #Table headers as keys of the yarns dict

        with open('yarns.csv', 'w', newline='') as output_file: #Write dict into a csv file
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(yarns)
            output_file.close()

    def write_to_xlsx(self): #An excel spreadsheet can also be created by using pandas
        yarns = self.convert_data()
        df = pd.DataFrame.from_dict(yarns)
        df.to_excel('yarns.xlsx')

    def insert_csv_into_database(self): #Insert created csv file into the database, this method is preferred in this application
        if self.already_created is False: #Do not append same values into the database
            self.write_to_csv()
            data = pd.read_csv(r'yarns.csv')
            df = pd.DataFrame(data)

            for yarn in df.itertuples(): #Write to database by choosing the correct values at correct indexes
                self.cursor.execute(
                    "INSERT INTO yarns VALUES (?, ?, ?, ?, ?, ?)"
                    , (yarn[1], yarn[2],
                       yarn[3], yarn[4], yarn[5],
                       yarn[6]))
            self.connection.commit()

    def get_data(self, hersteller, nadelstaerke): #Get data according to the filtering conditions
        if (hersteller == "All") and (nadelstaerke == "All"): #Without filter, get every yarn
            print("Get All")
            self.cursor.execute("SELECT * FROM yarns")
            return self.cursor.fetchall()
        elif (hersteller != "") and (nadelstaerke == "All"): #If a manufacturer size is specified
            print(hersteller, nadelstaerke)
            self.cursor.execute("SELECT * FROM yarns WHERE Hersteller = ?", (hersteller,))
            return self.cursor.fetchall()
        elif (hersteller == "All") and (nadelstaerke != ""): #If a needle size is specified
            print(hersteller, nadelstaerke)
            self.cursor.execute("SELECT * FROM yarns WHERE Nadelstaerke = ?", (nadelstaerke,))
            return self.cursor.fetchall()
        elif (hersteller != "") and (nadelstaerke != ""): #If both are specified
            print(hersteller, nadelstaerke)
            self.cursor.execute("SELECT * FROM yarns WHERE Nadelstaerke = ? AND Hersteller = ?", (nadelstaerke, hersteller))
            return self.cursor.fetchall()


