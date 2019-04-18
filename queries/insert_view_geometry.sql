INSERT INTO views_geometry_columns
    (view_name, view_geometry, view_rowid, f_table_name, f_geometry_column, read_only)
  VALUES ('spotter_pro_obis', 'geom', 'row_id', 'sightings', 'geom', 1);
  
INSERT INTO views_geometry_columns
    (view_name, view_geometry, view_rowid, f_table_name, f_geometry_column, read_only)
  VALUES ('whale_alert_obis', 'geom', 'row_id', 'whale_alert', 'geom', 1);