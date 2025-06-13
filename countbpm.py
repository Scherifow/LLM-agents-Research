# %%
from scipy.stats import fisher_exact

# Contingency table: rows = [RPA, Agent], columns = [Success, Fail]
table = [[9, 1],
         [10, 0]
         ]

oddsratio, p_value = fisher_exact(table)

print(f"Odds Ratio: {oddsratio}")
print(f"p-value: {p_value}")

# %%
