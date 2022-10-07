import rasterio
import matplotlib.pyplot as plt
import pandas as pd

hour = 25

filename = 'geomet-weather_RDPS.ETA_TT_2022-04-10T0000Z_PT{}H (1).tif'.format(str(hour))
print(filename)

dataset = rasterio.open('/dbfs/mnt/geospatial/{}'.format(filename))

dataset.read(1)

plt.imshow(dataset.read(1), cmap='turbo')

#processing is not shown here
df = processing(dataset,hour)

%sql
drop table if exists weather;
CREATE TABLE weather (
      lat DOUBLE,
      long DOUBLE,
      value DOUBLE,
      temperature STRING,
      datetime TIMESTAMP,
      hoursahead LONG
) USING DELTA
location 'abfss://geospatial@datalakestoragesharedtre.dfs.core.windows.net/delta/weather'

spark_df = spark.createDataFrame(df)
spark_df.write.format("delta").mode("append").saveAsTable("weather")

%sql select * from weather

%sql select datetime, temperature, hoursahead,min(value) mintempvalue from weather where lat < 44.6 and lat > 44.4 and long < -78.4 and long > -79.1 group by temperature, datetime, hoursahead
