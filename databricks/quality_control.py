# Databricks notebook source
import glow
spark = glow.register(spark)
from pyspark.sql.functions import *

data = spark.read.format("vcf").load('abfss://genomics@datalakestoragesharedtre.dfs.core.windows.net/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz')

# COMMAND ----------

# display(data)

# COMMAND ----------


# path = "/databricks-datasets/genomics/1kg-vcfs/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz"
# df = spark.read.format("vcf").option("flattenInfoFields", True).load(path)

# COMMAND ----------

# dbutils.fs.cp('/databricks-datasets/genomics/1kg-vcfs/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz', 'abfss://genomics@datalakestoragesharedtre.dfs.core.windows.net/ALL.chr22.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz')

# COMMAND ----------

# display(data.where(col("INFO_SVTYPE").isNotNull()).select("*", glow.expand_struct(glow.call_summary_stats("genotypes"))).drop("genotypes").limit(10))

# COMMAND ----------

display(data.select("*", glow.expand_struct(glow.hardy_weinberg("genotypes"))).drop("genotypes").limit(10))

# COMMAND ----------

# output_delta_split_multiallelics = 'abfss://genomics@ssctredatalakeshared.dfs.core.windows.net/delta/multiallelic2'
# output_delta_split_multiallelics_normalize = 'abfss://genomics@ssctredatalakeshared.dfs.core.windows.net/delta/multiallelic_normalize2'
# output_delta_glow_qc_transformers = 'abfss://genomics@ssctredatalakeshared.dfs.core.windows.net/delta/gc_transformers2'

# COMMAND ----------

import pyspark.sql.functions as fx
multiallelic_df = data.where(fx.size(fx.col("alternateAlleles")) > 1)
multiallelic_df = glow.transform('split_multiallelics', multiallelic_df)
# bialleleic_df = data.where(fx.size(fx.col("alternateAlleles")) == 1)
 
# multiallelic_df.write.mode("overwrite").format("delta").save(output_delta_split_multiallelics)
# bialleleic_df.write.mode("append").format("delta").save(output_delta_split_multiallelics)

# COMMAND ----------

# split_multiallelic_df = spark.read.format("delta").load(output_delta_split_multiallelics)
snps_df = multiallelic_df.where((fx.length("referenceAllele") == 1) & (fx.length(fx.col("alternateAlleles")[0]) == 1))

# COMMAND ----------

# display(snps_df)

# COMMAND ----------

delta_gwas_vcf = (snps_df.withColumn('values', glow.mean_substitute(glow.genotype_states('genotypes'))). \
                  filter(fx.size(fx.array_distinct('values')) > 1)
                 )

# COMMAND ----------

summary_stats_df = snps_df.select(
    fx.expr("*"),
    glow.expand_struct(glow.call_summary_stats(fx.col("genotypes"))),
    glow.expand_struct(glow.hardy_weinberg(fx.col("genotypes")))
  ). \
    withColumn("log10pValueHwe", fx.when(fx.col("pValueHwe") == 0, 26).otherwise(-fx.log10(fx.col("pValueHwe"))))

# COMMAND ----------

def calculate_pval_bonferroni_cutoff(df, cutoff=0.05):
  bonferroni_p =  cutoff / df.count()
  return bonferroni_p

# COMMAND ----------



# COMMAND ----------

hwe_cutoff = calculate_pval_bonferroni_cutoff(summary_stats_df)


# COMMAND ----------

def plot_histogram(df, col, xlabel, xmin, xmax, nbins, plot_title, plot_style, color, vline, out_path):
  plt.close()
  plt.figure()
  bins = np.linspace(xmin, xmax, nbins)
  df = df.toPandas()
  plt.hist(df[col], bins, alpha=1, color=color)
  if vline:
    plt.axvline(x=vline, linestyle='dashed', linewidth=2.0, color='black')
  plot_layout(plot_title, plot_style, xlabel)
  plt.savefig(out_path)
  plt.show()
def plot_layout(plot_title, plot_style, xlabel):
  plt.style.use(plot_style) #e.g. ggplot, seaborn-colorblind, print(plt.style.available)
  plt.title(plot_title)
  plt.xlabel(r'${0}$'.format(xlabel))
  plt.gca().spines['right'].set_visible(False)
  plt.gca().spines['top'].set_visible(False)
  plt.gca().yaxis.set_ticks_position('left')
  plt.gca().xaxis.set_ticks_position('bottom')
  plt.tight_layout()

# COMMAND ----------

import numpy as np
import matplotlib.pyplot as plt

# COMMAND ----------

display(plot_histogram(df=summary_stats_df.select("log10pValueHwe"), 
                       col="log10pValueHwe",
                       xlabel='-log_{10}(P)',
                       xmin=0, 
                       xmax=25, 
                       nbins=50, 
                       plot_title="hardy-weinberg equilibrium", 
                       plot_style="ggplot",
                       color='#e41a1c',
                       vline = -np.log10(hwe_cutoff),
                       out_path = 'here.png'
                      ))

# COMMAND ----------


