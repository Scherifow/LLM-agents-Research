from scipy.stats import fisher_exact, ttest_ind
import numpy as np

# ── Raw data from Calculation.xlsx / Sheet: List1 ──────────────────────────
# Times in seconds; failed runs excluded from t-test (treated as missing)

rpa_p2   = [53, 56, 53, 53, 53, 53, 55, 55, 55, 53]   # n=10
agent_p2 = [77, 79, 88, 232, 90, 87, 83, 122, 130]     # n=9  (1 failed run excluded)

rpa_p3   = [19, 22, 20, 22, 18, 17, 24, 17, 20, 21]    # n=10
agent_p3 = [181, 173, 241, 192, 208, 222]               # n=6  (4 failed runs excluded)

# ── Table 2: Welch's t-test (H1 — execution speed) ─────────────────────────
print("=" * 60)
print("TABLE 2 — Welch's t-test (H1: execution speed)")
print("=" * 60)

for name, rpa, agent in [("P2", rpa_p2, agent_p2), ("P3", rpa_p3, agent_p3)]:
    t, p = ttest_ind(rpa, agent, equal_var=False)

    # Cohen's d (pooled SD, Welch variant uses simple pooled here)
    mean_diff = np.mean(rpa) - np.mean(agent)
    pooled_sd = np.sqrt((np.std(rpa, ddof=1)**2 + np.std(agent, ddof=1)**2) / 2)
    d = mean_diff / pooled_sd

    # 95% CI on mean difference via t-distribution
    from scipy.stats import t as t_dist
    se = np.sqrt(np.var(rpa, ddof=1)/len(rpa) + np.var(agent, ddof=1)/len(agent))
    # Welch–Satterthwaite df
    s1, s2, n1, n2 = np.var(rpa, ddof=1), np.var(agent, ddof=1), len(rpa), len(agent)
    df = (s1/n1 + s2/n2)**2 / ((s1/n1)**2/(n1-1) + (s2/n2)**2/(n2-1))
    margin = t_dist.ppf(0.975, df) * se
    ci_lo, ci_hi = mean_diff - margin, mean_diff + margin

    print(f"\nProcess {name}:")
    print(f"  RPA   mean={np.mean(rpa):.2f}s  n={len(rpa)}")
    print(f"  Agent mean={np.mean(agent):.2f}s  n={len(agent)}")
    print(f"  t = {t:.3f},  p = {p:.4f},  Cohen's d = {abs(d):.2f}")
    print(f"  95% CI (mean diff) = [{ci_lo:.1f}, {ci_hi:.1f}] s")

# ── Table 3: Fisher's Exact Test (H2 — reliability) ────────────────────────
print("\n" + "=" * 60)
print("TABLE 3 — Fisher's Exact Test (H2: reliability / success rate)")
print("=" * 60)

# Contingency tables: rows = [Agent, RPA], cols = [Success, Fail]
# (alternative: swap rows — scipy reports OR as (row0_success/row0_fail)/(row1_success/row1_fail))
contingency = {
    "P2": [[9, 1],   # Agent: 9 success, 1 fail
           [10, 0]], # RPA:   10 success, 0 fail
    "P3": [[6, 4],   # Agent: 6 success, 4 fail
           [10, 0]], # RPA:   10 success, 0 fail
}

for name, table in contingency.items():
    or_, p = fisher_exact(table, alternative="two-sided")
    print(f"\nProcess {name}:")
    print(f"  Agent  success={table[0][0]}, fail={table[0][1]}")
    print(f"  RPA    success={table[1][0]}, fail={table[1][1]}")
    print(f"  Odds Ratio = {or_},  p = {p:.3f}")
