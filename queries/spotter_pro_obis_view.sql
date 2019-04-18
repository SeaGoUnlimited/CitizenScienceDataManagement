DROP VIEW IF EXISTS spotter_pro_obis;

CREATE VIEW spotter_pro_obis AS
SELECT DISTINCT
id as OccurenceID, 
create_date as EventDate,
scientific_name as scientificName,  
species as vernacularName,
COALESCE(number_sighted + "Total Sighted (Including Calves)", 
number_sighted, "Total Sighted (Including Calves)", 0) AS "individualCount",
lat as DecimalLatitude, 
lon as DecimalLongitude,
app_used, 
trip_id as collectionID,
Certainty as occurenceStatus,
basisOfRecord,
scientificNameID, 
wkt as footprintWKT,
sightingsgeom, INTERSECTS(sightings.geom, world_ocean.geom) AS in_ocean
FROM sightings, world_ocean
LEFT JOIN scientific_names ON species = scientific_names.common_name
WHERE individualCount >0
AND individualCount <= 10000
AND in_ocean=1
AND scientificName IS NOT NULL;
