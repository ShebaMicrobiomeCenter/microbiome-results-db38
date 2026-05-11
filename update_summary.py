import pandas as pd
import json

metadata_path = 'github_sync/microbiome-results-db38/map_qiime2.txt'
df = pd.read_csv(metadata_path, sep='\t')
reads_col = 'reads_number' if 'reads_number' in df.columns else 'Reads_count_x'
df[reads_col] = pd.to_numeric(df[reads_col], errors='coerce').fillna(0)

# Aggregations
df_filtered = df[df[reads_col] >= 4000]

summary = df.groupby('Cohort').agg({
    '#SampleID': ['count']
})
summary.columns = ['Total Samples']

filtered_summary = df_filtered.groupby('Cohort').agg({
    '#SampleID': 'count',
    'sample_ID': 'nunique',
    'shannon': 'mean'
})
filtered_summary.columns = ['Samples (>4k)', 'Unique Samples (>4k)', 'Mean Shannon (>4k)']

pivot_df = pd.concat([summary, filtered_summary], axis=1).fillna(0)
pivot_df = pivot_df.astype({'Total Samples': int, 'Samples (>4k)': int, 'Unique Samples (>4k)': int})

with open('github_sync/microbiome-results-db38/cohort_summary.html', 'w') as f:
    f.write('<h2>Cohort Summary</h2>' + pivot_df.to_html(classes='table table-striped'))
