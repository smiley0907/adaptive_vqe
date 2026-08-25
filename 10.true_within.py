# ============================================================
# CELL 10: TRUE WITHIN-FAMILY VALIDATION
# ============================================================

from scipy.stats import pearsonr, spearmanr
import numpy as np
import pandas as pd


# ------------------------------------------------------------
# Metrics to validate
# ------------------------------------------------------------

metrics = {

    "Maximum Contextual Score":
        "Maximum_Contextual_Score",

    "Mean Contextual Score":
        "Mean_Contextual_Score",

    "Total Contextual Score":
        "Total_Contextual_Score",

    "High Exposure Gates":
        "High_Exposure_Gates"
}


results = []


# ------------------------------------------------------------
# Process each metric
# ------------------------------------------------------------

for metric_name, metric_column in metrics.items():

    df = contextual_noise_results_df.copy()

    # --------------------------------------------------------
    # Remove circuit-family means
    #
    # This gives TRUE within-family variation.
    # --------------------------------------------------------

    exposure_centered = (
        df[metric_column]
        -
        df.groupby("Circuit")[
            metric_column
        ].transform("mean")
    )

    fidelity_centered = (
        df["Fidelity_Loss"]
        -
        df.groupby("Circuit")[
            "Fidelity_Loss"
        ].transform("mean")
    )

    # --------------------------------------------------------
    # Remove zero-variance cases
    # --------------------------------------------------------

    valid = (
        exposure_centered.notna()
        &
        fidelity_centered.notna()
    )

    x = exposure_centered[
        valid
    ].astype(float)

    y = fidelity_centered[
        valid
    ].astype(float)

    # --------------------------------------------------------
    # True within-family Pearson correlation
    # --------------------------------------------------------

    pearson_r, pearson_p = pearsonr(
        x,
        y
    )

    # --------------------------------------------------------
    # True within-family Spearman correlation
    # --------------------------------------------------------

    spearman_rho, spearman_p = spearmanr(
        x,
        y
    )

    # --------------------------------------------------------
    # Store
    # --------------------------------------------------------

    results.append({

        "Metric":
            metric_name,

        "Within_Family_Pearson_r":
            pearson_r,

        "Within_Family_Pearson_p":
            pearson_p,

        "Within_Family_Spearman_rho":
            spearman_rho,

        "Within_Family_Spearman_p":
            spearman_p
    })


# ------------------------------------------------------------
# Results dataframe
# ------------------------------------------------------------

within_family_df = pd.DataFrame(
    results
)


# ------------------------------------------------------------
# Round
# ------------------------------------------------------------

within_family_df[
    [
        "Within_Family_Pearson_r",
        "Within_Family_Pearson_p",
        "Within_Family_Spearman_rho",
        "Within_Family_Spearman_p"
    ]
] = within_family_df[
    [
        "Within_Family_Pearson_r",
        "Within_Family_Pearson_p",
        "Within_Family_Spearman_rho",
        "Within_Family_Spearman_p"
    ]
].round(6)


# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print(
    "============================================================"
)

print(
    "TRUE WITHIN-FAMILY EXPOSURE VALIDATION"
)

print(
    "============================================================\n"
)

print(
    within_family_df.to_string(
        index=False
    )
)


# ------------------------------------------------------------
# Family-specific results
# ------------------------------------------------------------

print(
    "\n============================================================"
)

print(
    "FAMILY-SPECIFIC RESULTS"
)

print(
    "============================================================"
)


for family in CIRCUIT_FAMILIES:

    family_df = contextual_noise_results_df[
        contextual_noise_results_df[
            "Circuit"
        ] == family
    ].copy()

    print(
        f"\n----- {family} -----"
    )

    for metric_name, metric_column in (
        metrics.items()
    ):

        x = family_df[
            metric_column
        ].astype(float)

        y = family_df[
            "Fidelity_Loss"
        ].astype(float)

        r, p = pearsonr(
            x,
            y
        )

        print(
            f"{metric_name}: "
            f"r = {r:.6f}, "
            f"p = {p:.6f}"
        )


# ------------------------------------------------------------
# Primary metric
# ------------------------------------------------------------

primary = within_family_df.iloc[0]


print(
    "\n============================================================"
)

print(
    "PRIMARY WITHIN-FAMILY VALIDATION"
)

print(
    "============================================================"
)

print(
    "Metric:",
    primary["Metric"]
)

print(
    "Within-family Pearson r:",
    primary[
        "Within_Family_Pearson_r"
    ]
)

print(
    "Within-family Pearson p:",
    primary[
        "Within_Family_Pearson_p"
    ]
)

print(
    "Within-family Spearman rho:",
    primary[
        "Within_Family_Spearman_rho"
    ]
)

print(
    "Within-family Spearman p:",
    primary[
        "Within_Family_Spearman_p"
    ]
)


# ------------------------------------------------------------
# Final decision
# ------------------------------------------------------------

significant_count = 0

for _, row in within_family_df.iterrows():

    if (
        row[
            "Within_Family_Pearson_p"
        ] < 0.05
    ):

        significant_count += 1


print(
    "\n============================================================"
)

print(
    "FINAL RESEARCH DECISION"
)

print(
    "============================================================"
)


if (
    primary[
        "Within_Family_Pearson_p"
    ] < 0.05
):

    print(
        "PRIMARY METRIC VALIDATED."
    )

    print(
        "The contextual exposure metric shows "
        "a statistically significant within-family "
        "relationship with fidelity loss."
    )

elif significant_count >= 2:

    print(
        "PARTIAL VALIDATION."
    )

    print(
        "Multiple contextual exposure measures show "
        "within-family statistical relationships, "
        "but the primary metric is not significant."
    )

else:

    print(
        "NO PREDICTIVE VALIDATION."
    )

    print(
        "The contextual exposure metric should be "
        "presented as an exposure profiling method, "
        "not as a predictor of fidelity degradation."
    )


print(
    "\nCell 10 completed successfully."
)
