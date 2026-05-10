import pandas as pd
import json

metadata_path = 'github_sync/microbiome-results-db38/map_qiime2.txt'
df = pd.read_csv(metadata_path, sep='\t')
reads_col = 'reads_number' if 'reads_number' in df.columns else 'Reads_count_x'
df[reads_col] = pd.to_numeric(df[reads_col], errors='coerce').fillna(0)

df_filtered = df[df[reads_col] >= 4000]
pivot_df = df_filtered.groupby('Cohort').agg({
    '#SampleID': 'count',
    'sample_ID': 'nunique',
    'shannon': 'mean'
}).rename(columns={
    '#SampleID': 'Total Samples (>4k)',
    'sample_ID': 'Unique Samples',
    'shannon': 'Mean Shannon Diversity'
}).reset_index()

with open('github_sync/microbiome-results-db38/cohort_summary.html', 'w') as f:
    f.write('<h2>Cohort Summary (>4k reads)</h2>' + pivot_df.to_html(index=False, classes='table table-striped'))
