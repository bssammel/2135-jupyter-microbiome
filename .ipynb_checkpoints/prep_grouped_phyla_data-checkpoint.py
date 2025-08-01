import pandas as pd

# Load your dataset (replace 'your_file.csv')
df = pd.read_csv("all_phyla_crop_data.csv")

# Clean and normalize taxonomic data
# Assuming a column 'Phylum' and columns for samples

# Group by phylum and calculate total abundance
phylum_counts = df.groupby("Phylum").sum().T
relative_abundance = phylum_counts.div(phylum_counts.sum(axis=1), axis=0)

# Identify top 8 phyla
top8 = relative_abundance.sum().sort_values(ascending=False).head(8).index

# Create new column to group all other bacteria
is_bacteria = df["Kingdom"] == "Bacteria"
top8_bacteria = df["Phylum"].isin(top8)
df["Group"] = "Other Bacteria"
df.loc[~is_bacteria, "Group"] = df["Kingdom"]
df.loc[top8_bacteria, "Group"] = df["Phylum"]

# Regroup and aggregate again
grouped = df.groupby("Group").sum().T
grouped_rel = grouped.div(grouped.sum(axis=1), axis=0)

# Now you can plot it
import matplotlib.pyplot as plt

grouped_rel.plot(kind="bar", stacked=True, figsize=(12, 6))
plt.title("Relative Abundance of Microbial Phyla by Sample")
plt.ylabel("Relative Abundance")
plt.xlabel("Sample")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
