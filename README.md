# CitizenScienceDataManagement

# This application was designed to harvest whale sightings data collected using two smart phone apps (Whale Alert and Spotter Pro) from Conserve.io and preserve/organize the data into an SQLite database. 
http://conserve.io/

http://www.whalealert.org/

SpatiaLite was used to extend SQLite core to support fully fledged Spatial SQL capabilities. 

# Due to the proprietary nature of the app data, the login credentials have been purposely omitted. 

# The basic schema is:  
1. The application logs into the conserve.io server 
(website.py)

2. Scrapes/harvests each sighting JSON and parses each JSON 
(json_data.py)

3. Creates an empty SQLite database, and inserts the parsed data into relevant tables in the database 
(database.py)

4. Updates the database as new sightings are recorded 
(update_spotter.py & update_whalealert.py -> main.sh)

4. Virtual tables (views) within the database filter, flag, clean, and reformat the raw data to meet Ocean Biogeographic Information System (OBIS) data standards (https://obis.org/) 
(SQLite & SpatiaLite)

5. Finally, Docker was used to 'package' the application, so a user doesn’t need to have Python or install required libraries/modules. 
(Dockerfile)


