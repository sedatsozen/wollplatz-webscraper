# wollplatz-webscraper
A webscraper with flask interface for the website wollplatz.de

ENGLISH:

This program searches through every yarn inside the website and gets the manufacturer, name, price, delivery time, needle size and material information for each yarn with the method of web scraping. Then, the yarns are saved into a text file, after that the text file is converted into a usable csv file and a local SQLite database. Lastly, by using flask, the yarns in the database are shown on a localhost website as a table. The user has the option to filter the manufacturer and needle size information in order to get mathing yarns.

DEUTSCH:

Dieses Programm durchsucht jedes Garn innerhalb der Website und ermittelt mit der Methode des Web Scraping Hersteller, Name, Preis, Lieferzeit, Nadelstärke und Materialinformationen für jedes Garn. Dann werden die Garne in einer Textdatei gespeichert, danach wird die Textdatei in eine verwendbare csv-Datei und eine lokale SQLite-Datenbank konvertiert. Schließlich werden durch die Verwendung von Flask die Garne in der Datenbank auf einer localhost-Website als Tabelle angezeigt. Der Benutzer hat die Möglichkeit, die Hersteller- und Nadelstaerkeinformationen zu filtern, um passende Garne zu erhalten.
