# ============================================================
# CELL 8: CONTEXTUAL EXPOSURE VS FIDELITY LOSS
# ============================================================

from scipy.stats import pearsonr, spearmanr

correlation_pairs = {

    "Maximum Contextual Score vs Fidelity Loss": (
        "Maximum_Contextual_Score",
        "Fidelity_Loss"
    ),

    "Mean Contextual Score vs Fidelity Loss": (
        "Mean_Contextual_Score",
        "Fidelity_Loss"
    ),

    "Total Contextual Score vs Fidelity Loss": (
        "Total_Contextual_Score",
        "Fidelity_Loss"
    ),

    "High Exposure Gates vs Fidelity Loss": (
        "High_Exposure_Gates",
        "Fidelity_Loss"
    ),

    "Exposure Concentration vs Fidelity Loss": (
        "Exposure_Concentration_%",
        "Fidelity_Loss"
    ),

    "Relative Top Exposure vs Fidelity Loss": (
        "Relative_Top_Exposure",
        "Fidelity_Loss"
    )
}


correlation_results = []


# ------------------------------------------------------------
# Overall correlations
# ------------------------------------------------------------

for relationship, (
    x_column,
    y_column
) in correlation_pairs.items():

    x = contextual_noise_results_df[
        x_column
    ].astype(float)

    y = contextual_noise_results_df[
        y_column
    ].astype(float)

    pearson_r, pearson_p = pearsonr(
        x,
        y
    )

    spearman_rho, spearman_p = spearmanr(
        x,
        y
    )

    correlation_results.append({

        "Relationship":
            relationship,

        "Pearson_r":
            pearson_r,

        "Pearson_p":
            pearson_p,

        "Spearman_rho":
            spearman_rho,

        "Spearman_p":
            spearman_p
    })


correlation_df = pd.DataFrame(
    correlation_results
)


# ------------------------------------------------------------
# Round
# ------------------------------------------------------------

correlation_df[
    [
        "Pearson_r",
        "Pearson_p",
        "Spearman_rho",
        "Spearman_p"
    ]
] = correlation_df[
    [
        "Pearson_r",
        "Pearson_p",
        "Spearman_rho",
        "Spearman_p"
    ]
].round(6)


# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print(
    "============================================================"
)

print(
    "CONTEXTUAL EXPOSURE VS FIDELITY LOSS"
)

print(
    "============================================================\n"
)

print(
    correlation_df.to_string(
        index=False
    )
)


# ------------------------------------------------------------
# Family-wise validation
# ------------------------------------------------------------

print(
    "\n============================================================"
)

print(
    "FAMILY-WISE CONTEXTUAL EXPOSURE VALIDATION"
)

print(
    "============================================================\n"
)


family_results = []


for family in CIRCUIT_FAMILIES:

    family_df = contextual_noise_results_df[
        contextual_noise_results_df[
            "Circuit"
        ] == family
    ]

    x = family_df[
        "Maximum_Contextual_Score"
    ].astype(float)

    y = family_df[
        "Fidelity_Loss"
    ].astype(float)

    pearson_r, pearson_p = pearsonr(
        x,
        y
    )

    spearman_rho, spearman_p = spearmanr(
        x,
        y
    )

    family_results.append({

        "Circuit":
            family,

        "Pearson_r":
            pearson_r,

        "Pearson_p":
            pearson_p,

        "Spearman_rho":
            spearman_rho,

        "Spearman_p":
            spearman_p
    })


family_correlation_df = pd.DataFrame(
    family_results
)


family_correlation_df[
    [
        "Pearson_r",
        "Pearson_p",
        "Spearman_rho",
        "Spearman_p"
    ]
] = family_correlation_df[
    [
        "Pearson_r",
        "Pearson_p",
        "Spearman_rho",
        "Spearman_p"
    ]
].round(6)


print(
    family_correlation_df.to_string(
        index=False
    )
)


# ------------------------------------------------------------
# Primary result
# ------------------------------------------------------------

primary = correlation_df.iloc[0]

print(
    "\n============================================================"
)

print(
    "PRIMARY RELATIONSHIP"
)

print(
    "============================================================"
)

print(
    "Maximum Contextual Score vs Fidelity Loss"
)

print(
    "Pearson r    :",
    primary["Pearson_r"]
)

print(
    "Pearson p    :",
    primary["Pearson_p"]
)

print(
    "Spearman rho :",
    primary["Spearman_rho"]
)

print(
    "Spearman p   :",
    primary["Spearman_p"]
)


if (
    primary["Pearson_p"] < 0.05
    and
    primary["Spearman_p"] < 0.05
):

    print(
        "\nStatistically significant relationship established."
    )

else:

    print(
        "\nStatistical significance not established."
    )


print(
    "\nCell 8 completed successfully."
)
