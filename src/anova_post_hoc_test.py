# Which cancer pairs have significantly different mutation burdens?

# Tukey's HSD(Honestly Significant Difference) cpz ANOVA doesn't tell us which pair differ. HSD will see BRCA vs COAD, BRCA vs LUAS, COAD vs LUAD

# BRCA vs COAD, reject=True: COAD mutation burden is significantly different from BRCA.
# COAD vs LUAD, reject=False: No significant difference detected between COAD and LUAD mutation burden.
# Column	Meaning
# meandiff	Difference between means
# p-adj	Multiple-testing corrected p-value
# lower	Lower CI
# upper	Upper CI
# reject	Significant?

import pandas as pd

from statsmodels.stats.multicomp import (
    pairwise_tukeyhsd
)

df = pd.read_csv(
    "data/processed/combined_mutations.csv"
)

# Mutation burden per sample
burden = (
    df.groupby(
        ["sample_id", "cancer_type"]
    )
    .size()
    .reset_index(
        name="mutation_burden"
    )
)

tukey = pairwise_tukeyhsd(
    endog=burden["mutation_burden"],
    groups=burden["cancer_type"],
    alpha=0.05
)

results = pd.DataFrame(
    data=tukey._results_table.data[1:],
    columns=tukey._results_table.data[0]
)

results.to_csv(
    "data/processed/analysis/tukey_hsd_results.csv",
    index=False
)

print(results)
