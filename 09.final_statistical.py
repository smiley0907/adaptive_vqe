# ============================================================
# CELL 9: FINAL STATISTICAL VALIDATION
# ============================================================

from scipy.stats import pearsonr, spearmanr
import numpy as np
import pandas as pd


# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

N_PERMUTATIONS = 20000
RANDOM_SEED = 12345

rng = np.random.default_rng(
    RANDOM_SEED
)


# ------------------------------------------------------------
# Metrics to validate
# ------------------------------------------------------------

validation_metrics = {

    "Maximum Contextual Score":
        "Maximum_Contextual_Score",

    "Mean Contextual Score":
        "Mean_Contextual_Score",

    "Total Contextual Score":
        "Total_Contextual_Score",

    "High Exposure Gates":
        "High_Exposure_Gates",

    "Exposure Concentration":
        "Exposure_Concentration_%",

    "Relative Top Exposure":
        "Relative_Top_Exposure"
}


# ------------------------------------------------------------
# Within-family permutation test
#
# Fidelity-loss values are shuffled ONLY within each
# circuit family. Therefore, family-level differences
# are preserved.
# ------------------------------------------------------------

def family_permutation_test(
    dataframe,
    x_column,
    y_column,
    n_permutations=20000,
    seed=12345
):

    local_rng = np.random.default_rng(
        seed
    )

    observed_x = (
        dataframe[x_column]
        .astype(float)
        .to_numpy()
    )

    observed_y = (
        dataframe[y_column]
        .astype(float)
        .to_numpy()
    )

    # --------------------------------------------------------
    # Observed Pearson correlation
    # --------------------------------------------------------

    observed_r, _ = pearsonr(
        observed_x,
        observed_y
    )

    # --------------------------------------------------------
    # Permutation distribution
    # --------------------------------------------------------

    permuted_correlations = []

    for _ in range(
        n_permutations
    ):

        shuffled_y = observed_y.copy()

        # Shuffle fidelity loss separately
        # inside each circuit family
        for family in CIRCUIT_FAMILIES:

            indices = dataframe.index[
                dataframe["Circuit"]
                == family
            ].to_numpy()

            positions = [
                dataframe.index.get_loc(i)
                for i in indices
            ]

            shuffled_values = (
                shuffled_y[
                    positions
                ].copy()
            )

            local_rng.shuffle(
                shuffled_values
            )

            shuffled_y[
                positions
            ] = shuffled_values

        try:

            perm_r, _ = pearsonr(
                observed_x,
                shuffled_y
            )

            if np.isfinite(perm_r):

                permuted_correlations.append(
                    perm_r
                )

        except Exception:

            pass


    permuted_correlations = np.array(
        permuted_correlations
    )

    # --------------------------------------------------------
    # Two-sided empirical p-value
    # --------------------------------------------------------

    extreme_count = np.sum(
        np.abs(
            permuted_correlations
        )
        >=
        abs(observed_r)
    )

    empirical_p = (
        extreme_count + 1
    ) / (
        len(permuted_correlations) + 1
    )

    return (
        observed_r,
        empirical_p
    )


# ------------------------------------------------------------
# Holm correction
# ------------------------------------------------------------

def holm_correction(p_values):

    p_values = np.asarray(
        p_values,
        dtype=float
    )

    order = np.argsort(
        p_values
    )

    adjusted = np.empty_like(
        p_values
    )

    previous = 0.0

    m = len(
        p_values
    )

    for rank, index in enumerate(
        order
    ):

        corrected = (
            m - rank
        ) * p_values[index]

        corrected = max(
            corrected,
            previous
        )

        corrected = min(
            corrected,
            1.0
        )

        adjusted[index] = corrected

        previous = corrected

    return adjusted


# ------------------------------------------------------------
# Overall validation
# ------------------------------------------------------------

validation_results = []


for metric_name, column in (
    validation_metrics.items()
):

    x = contextual_noise_results_df[
        column
    ].astype(float)

    y = contextual_noise_results_df[
        "Fidelity_Loss"
    ].astype(float)

    # Standard Pearson
    pearson_r, pearson_p = pearsonr(
        x,
        y
    )

    # Standard Spearman
    spearman_rho, spearman_p = spearmanr(
        x,
        y
    )

    # Family-controlled permutation
    controlled_r, controlled_p = (
        family_permutation_test(
            contextual_noise_results_df,
            column,
            "Fidelity_Loss",
            N_PERMUTATIONS,
            RANDOM_SEED
        )
    )

    validation_results.append({

        "Metric":
            metric_name,

        "Pearson_r":
            pearson_r,

        "Pearson_p":
            pearson_p,

        "Spearman_rho":
            spearman_rho,

        "Spearman_p":
            spearman_p,

        "Family_Controlled_r":
            controlled_r,

        "Family_Controlled_P":
            controlled_p
    })


validation_df = pd.DataFrame(
    validation_results
)


# ------------------------------------------------------------
# Holm correction
# ------------------------------------------------------------

validation_df[
    "Holm_Adjusted_P"
] = holm_correction(
    validation_df[
        "Family_Controlled_P"
    ].values
)


# ------------------------------------------------------------
# Effect interpretation
# ------------------------------------------------------------

def effect_label(r):

    magnitude = abs(r)

    if magnitude >= 0.70:
        return "Strong"

    elif magnitude >= 0.50:
        return "Moderate"

    elif magnitude >= 0.30:
        return "Weak"

    else:
        return "Very Weak"


validation_df[
    "Effect"
] = validation_df[
    "Family_Controlled_r"
].apply(
    effect_label
)


validation_df[
    "Significant_After_Holm"
] = (
    validation_df[
        "Holm_Adjusted_P"
    ]
    < 0.05
)


# ------------------------------------------------------------
# Round
# ------------------------------------------------------------

validation_df[
    [
        "Pearson_r",
        "Pearson_p",
        "Spearman_rho",
        "Spearman_p",
        "Family_Controlled_r",
        "Family_Controlled_P",
        "Holm_Adjusted_P"
    ]
] = validation_df[
    [
        "Pearson_r",
        "Pearson_p",
        "Spearman_rho",
        "Spearman_p",
        "Family_Controlled_r",
        "Family_Controlled_P",
        "Holm_Adjusted_P"
    ]
].round(6)


# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print(
    "============================================================"
)

print(
    "FINAL STATISTICAL VALIDATION"
)

print(
    "============================================================\n"
)

print(
    validation_df.to_string(
        index=False
    )
)


# ------------------------------------------------------------
# Primary metric
# ------------------------------------------------------------

primary_metric = validation_df[
    validation_df["Metric"]
    ==
    "Maximum Contextual Score"
].iloc[0]


print(
    "\n============================================================"
)

print(
    "PRIMARY METRIC VALIDATION"
)

print(
    "============================================================"
)

print(
    "Metric:",
    primary_metric["Metric"]
)

print(
    "Pearson r:",
    primary_metric["Pearson_r"]
)

print(
    "Pearson p:",
    primary_metric["Pearson_p"]
)

print(
    "Spearman rho:",
    primary_metric["Spearman_rho"]
)

print(
    "Spearman p:",
    primary_metric["Spearman_p"]
)

print(
    "Family-controlled r:",
    primary_metric[
        "Family_Controlled_r"
    ]
)

print(
    "Family-controlled p:",
    primary_metric[
        "Family_Controlled_P"
    ]
)

print(
    "Holm-adjusted p:",
    primary_metric[
        "Holm_Adjusted_P"
    ]
)

print(
    "Effect:",
    primary_metric[
        "Effect"
    ]
)


# ------------------------------------------------------------
# Identify significant metrics
# ------------------------------------------------------------

significant_metrics = validation_df[
    validation_df[
        "Significant_After_Holm"
    ]
]


print(
    "\n============================================================"
)

print(
    "VALIDATED METRICS"
)

print(
    "============================================================"
)


if len(
    significant_metrics
) > 0:

    for _, row in (
        significant_metrics.iterrows()
    ):

        print(
            row["Metric"],
            "| r =",
            row["Family_Controlled_r"],
            "| adjusted p =",
            row["Holm_Adjusted_P"]
        )

else:

    print(
        "No metric remains statistically significant "
        "after family control and Holm correction."
    )


# ------------------------------------------------------------
# Final evidence assessment
# ------------------------------------------------------------

primary_significant = (
    primary_metric[
        "Holm_Adjusted_P"
    ]
    < 0.05
)

strong_secondary = (
    len(
        significant_metrics
    ) >= 2
)


print(
    "\n============================================================"
)

print(
    "FINAL EXPERIMENTAL ASSESSMENT"
)

print(
    "============================================================"
)


if (
    primary_significant
    and
    strong_secondary
):

    print(
        "STRONG EVIDENCE: "
        "Contextual exposure is statistically supported."
    )

elif primary_significant:

    print(
        "PROMISING EVIDENCE: "
        "Primary contextual exposure relationship is supported, "
        "but additional validation should be discussed."
    )

else:

    print(
        "INSUFFICIENT STATISTICAL EVIDENCE: "
        "Do not claim predictive validity of the contextual "
        "exposure metric."
    )


print(
    "\nPermutations:",
    N_PERMUTATIONS
)

print(
    "Cell 9 completed successfully."
)
