DROP VIEW IF EXISTS whale_alert_obis

CREATE VIEW whale_alert_obis AS
SELECT DISTINCT 
id AS OccurenceID, 
create_date AS EventDate, 
scientific_name AS scientificName, 
IFNULL("Whale Alert Species", "Whale Alert Other Species") AS vernacularName, 
"Number Sighted" AS individualCount, 
lat AS DecimalLatitude, 
lon AS DecimalLongitude, 
app_used, 
trip_id AS collectionID, 
"Animal Status" AS occurenceStatus, 
basisOfRecord, 
scientificNameID, 
wkt AS footprintWKT, 
whale_alert.geom,
INTERSECTS(whale_alert.geom, world_ocean.geom)AS "in_ocean"
FROM whale_alert, world_ocean
LEFT JOIN scientific_names ON 
IFNULL(whale_alert."Whale Alert Species", whale_alert."Whale Alert Other Species") = scientific_names.common_name 
WHERE vernacularName != "Unspecified" 
AND "in_ocean"=1
AND scientificName IS NOT NULL;
