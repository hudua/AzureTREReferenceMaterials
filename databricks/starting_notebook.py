# Databricks notebook source
df = spark.read.format("vcf").load('abfss://genomics@datalakestoragesharedtre.dfs.core.windows.net/D13.snp4.1.vcf.gz')

# COMMAND ----------

display(df)

# COMMAND ----------

# df.write.format('delta').partitionBy('contigName').mode('append').save('abfss://genomics@datalakestoragesharedtre.dfs.core.windows.net/delta/sample-genomics')

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC -- create table samplegenomics2 using delta location 'abfss://genomics@datalakestoragesharedtre.dfs.core.windows.net/delta/sample-genomics'

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC select count(*) from samplegenomics2

# COMMAND ----------

# MAGIC %sql
# MAGIC 
# MAGIC select * from samplegenomics2

# COMMAND ----------

# MAGIC %r
# MAGIC library(SparkR)
# MAGIC sparkR.session()

# COMMAND ----------

# MAGIC %r
# MAGIC sample_df = tableToDF("samplegenomics")
# MAGIC 
# MAGIC display(sample_df)

# COMMAND ----------

import pandas as pd
import numpy as np

df_pd = pd.DataFrame({'contigName':['Chr01','Chr02','Chr03','Chr04','Chr05','Chr05'], 'descrName':['This is the first chromosome','2nd','3rd','4th chromosome','5th chrom.', 'this is 6th'], 'numbers': np.array(1)})

# COMMAND ----------

df_spark = spark.createDataFrame(df_pd)
data = spark.sql('select * from samplegenomics limit 10').cache()

# COMMAND ----------

final = data.join(df_spark, data['contigName']==df_spark['contigName'], 'outer')

# COMMAND ----------

display(final)

# COMMAND ----------


