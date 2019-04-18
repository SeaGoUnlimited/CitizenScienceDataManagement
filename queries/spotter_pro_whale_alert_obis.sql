DROP VIEW IF EXISTS spotter_pro_whale_alert_obis;

CREATE VIEW  spotter_pro_whale_alert_obis AS
SELECT * FROM spotter_pro_obis
UNION ALL SELECT * FROM whale_alert_obis;
