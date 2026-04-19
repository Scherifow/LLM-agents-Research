"""
Statistical Validation Script
==============================
Computes Cohen's d, 95% confidence intervals, power analysis,
and skewness for the RPA vs AACU comparison study.
 
INSTRUCTIONS:
  Replace the placeholder arrays below with your actual experimental data
  (execution times in seconds for each of the 10 runs).
"""
 
import numpy as np
from scipy import stats
 
# ============================================================
# >>>  REPLACE THESE WITH YOUR ACTUAL DATA  <<<
# ============================================================
# P2 execution times (seconds) — successful runs only
rpa_p2 = np.array([53.0, 56.0, 53.0, 53.0, 53.0, 53.0, 55.0, 55.0, 55.0, 53.0])   # 10/10 successful
aacu_p2 = np.array([77.0, 79.0, 88.0, 232.0, 90.0, 87.0, 83.0, 122.0, 130.0])      # 9/10 successful

# P3 execution times (seconds) — successful runs only
rpa_p3 = np.array([19.0, 22.0, 20.0, 22.0, 18.0, 17.0, 24.0, 17.0, 20.0, 21.0])   # 10/10 successful
aacu_p3 = np.array([181.0, 173.0, 241.0, 192.0, 208.0, 222.0])                      # 6/10 successful

# P2 success/failure counts (out of 10 runs)
rpa_p2_success = 10
rpa_p2_fail = 0
aacu_p2_success = 9
aacu_p2_fail = 1

# P3 success/failure counts (out of 10 runs)
rpa_p3_success = 10
rpa_p3_fail = 0
aacu_p3_success = 6
aacu_p3_fail = 4
# ============================================================
 
 
def cohens_d_welch(group1, group2):
    """Cohen's d using pooled SD (for two independent groups)."""
    n1, n2 = len(group1), len(group2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    pooled_sd = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    d = (np.mean(group1) - np.mean(group2)) / pooled_sd
    return d, pooled_sd
 
 
def ci_mean_difference(group1, group2, confidence=0.95):
    """95% CI for the difference in means using Welch's t-test df."""
    n1, n2 = len(group1), len(group2)
    mean_diff = np.mean(group1) - np.mean(group2)
    se = np.sqrt(np.var(group1, ddof=1) / n1 + np.var(group2, ddof=1) / n2)
    var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    df = ((var1 / n1 + var2 / n2) ** 2 /
          ((var1 / n1) ** 2 / (n1 - 1) + (var2 / n2) ** 2 / (n2 - 1)))
    t_crit = stats.t.ppf((1 + confidence) / 2, df)
    ci_lower = mean_diff - t_crit * se
    ci_upper = mean_diff + t_crit * se
    return mean_diff, ci_lower, ci_upper, se, df
 
 
def fisher_exact_with_ci(s1, f1, s2, f2):
    """Fisher's Exact Test + 95% CI for difference in proportions."""
    table = np.array([[s1, f1], [s2, f2]])
    odds_ratio, p_value = stats.fisher_exact(table)
    n1, n2 = s1 + f1, s2 + f2
    p1, p2 = s1 / n1, s2 / n2
    diff = p1 - p2
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    ci_lower = diff - 1.96 * se
    ci_upper = diff + 1.96 * se
    return odds_ratio, p_value, diff, ci_lower, ci_upper
 
 
def power_fisher(s1, f1, s2, f2, alpha=0.05, n_sim=100_000):
    """Monte Carlo power estimate for Fisher's Exact Test."""
    n1, n2 = s1 + f1, s2 + f2
    p1_hat, p2_hat = s1 / n1, s2 / n2
    np.random.seed(42)
    sig_count = 0
    for _ in range(n_sim):
        x1 = np.random.binomial(n1, p1_hat)
        x2 = np.random.binomial(n2, p2_hat)
        sim_table = [[x1, n1 - x1], [x2, n2 - x2]]
        _, p = stats.fisher_exact(sim_table)
        if p < alpha:
            sig_count += 1
    return sig_count / n_sim
 
 
print("=" * 70)
print("STATISTICAL VALIDATION REPORT")
print("=" * 70)
 
# H1 — P2
print("\nH1 — PROCESS P2 (Execution Time)")
t_p2, p_p2 = stats.ttest_ind(rpa_p2, aacu_p2, equal_var=False)
d_p2, pooled_p2 = cohens_d_welch(rpa_p2, aacu_p2)
diff_p2, ci_lo_p2, ci_hi_p2, se_p2, df_p2 = ci_mean_difference(rpa_p2, aacu_p2)
print(f"  RPA  mean: {np.mean(rpa_p2):.2f}s, SD: {np.std(rpa_p2, ddof=1):.2f}s")
print(f"  AACU mean: {np.mean(aacu_p2):.2f}s, SD: {np.std(aacu_p2, ddof=1):.2f}s")
print(f"  Welch t={t_p2:.4f}, p={p_p2:.6f}")
print(f"  Cohen's d={d_p2:.4f} (pooled SD={pooled_p2:.2f})")
print(f"  Mean diff={diff_p2:.2f}s, 95% CI=[{ci_lo_p2:.2f}, {ci_hi_p2:.2f}]")
print(f"  Skewness — RPA: {stats.skew(rpa_p2):.4f}, AACU: {stats.skew(aacu_p2):.4f}")
print(f"  Shapiro-Wilk — RPA: {stats.shapiro(rpa_p2)}, AACU: {stats.shapiro(aacu_p2)}")
 
# H1 — P3
print("\nH1 — PROCESS P3 (Execution Time)")
t_p3, p_p3 = stats.ttest_ind(rpa_p3, aacu_p3, equal_var=False)
d_p3, pooled_p3 = cohens_d_welch(rpa_p3, aacu_p3)
diff_p3, ci_lo_p3, ci_hi_p3, se_p3, df_p3 = ci_mean_difference(rpa_p3, aacu_p3)
print(f"  RPA  mean: {np.mean(rpa_p3):.2f}s, SD: {np.std(rpa_p3, ddof=1):.2f}s")
print(f"  AACU mean: {np.mean(aacu_p3):.2f}s, SD: {np.std(aacu_p3, ddof=1):.2f}s")
print(f"  Welch t={t_p3:.4f}, p={p_p3:.6f}")
print(f"  Cohen's d={d_p3:.4f} (pooled SD={pooled_p3:.2f})")
print(f"  Mean diff={diff_p3:.2f}s, 95% CI=[{ci_lo_p3:.2f}, {ci_hi_p3:.2f}]")
print(f"  Skewness — RPA: {stats.skew(rpa_p3):.4f}, AACU: {stats.skew(aacu_p3):.4f}")
print(f"  Shapiro-Wilk — RPA: {stats.shapiro(rpa_p3)}, AACU: {stats.shapiro(aacu_p3)}")
 
# H2 — P2
print("\nH2 — PROCESS P2 (Reliability)")
or2, fp2, fd2, fc2l, fc2h = fisher_exact_with_ci(rpa_p2_success, rpa_p2_fail, aacu_p2_success, aacu_p2_fail)
print(f"  Fisher p={fp2:.4f}, OR={or2}, Diff={fd2:.2f}, 95% CI=[{fc2l:.4f}, {fc2h:.4f}]")
pw2 = power_fisher(rpa_p2_success, rpa_p2_fail, aacu_p2_success, aacu_p2_fail)
print(f"  Power={pw2:.4f}")
 
# H2 — P3
print("\nH2 — PROCESS P3 (Reliability)")
or3, fp3, fd3, fc3l, fc3h = fisher_exact_with_ci(rpa_p3_success, rpa_p3_fail, aacu_p3_success, aacu_p3_fail)
print(f"  Fisher p={fp3:.4f}, OR={or3}, Diff={fd3:.2f}, 95% CI=[{fc3l:.4f}, {fc3h:.4f}]")
pw3 = power_fisher(rpa_p3_success, rpa_p3_fail, aacu_p3_success, aacu_p3_fail)
print(f"  Power={pw3:.4f}")
