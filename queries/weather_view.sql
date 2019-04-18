CREATE VIEW spotter_pro_weather AS
SELECT
row_id,
trip_id,
create_date,
"Beaufort Scale" AS beaufort_scale,
(COALESCE("Swell",'') || " " || COALESCE("Swell (keyboard)", '')) AS "swell",
(COALESCE("Visibility",'') || " " || COALESCE("Visbility (Keyboard)", '')) AS "visibility",
(COALESCE("Cloud Cover",'') || " " || COALESCE("Cloud Cover (Keyboard)", '')) AS "cloud_cover"
FROM weather
WHERE VISIBILITY >=0; 