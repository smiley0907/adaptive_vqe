# ============================================================
# CELL 6: Contextual Exposure Ranking and Concentration
# ============================================================

contextual_ranking = []

for family in CIRCUIT_FAMILIES:

    for n in QUBIT_CONFIGS:

        df = contextual_regions[
            family
        ][n]["Gate_Profile"].copy()

        # ----------------------------------------------------
        # Rank gates by contextual exposure score
        # ----------------------------------------------------

        df = df.sort_values(
            "Contextual_Exposure_Score",
            ascending=False
        ).reset_index(
            drop=True
        )

        df["Exposure_Rank"] = (
            np.arange(len(df)) + 1
        )

        # ----------------------------------------------------
        # Top 10% gates
        # ----------------------------------------------------

        top_count = max(
            1,
            int(
                np.ceil(
                    0.10 * len(df)
                )
            )
        )

        top_gates = df.iloc[
            :top_count
        ]

        # ----------------------------------------------------
        # Total contextual exposure
        # ----------------------------------------------------

        total_exposure = df[
            "Contextual_Exposure_Score"
        ].sum()

        top_exposure = top_gates[
            "Contextual_Exposure_Score"
        ].sum()

        # ----------------------------------------------------
        # Exposure concentration
        # ----------------------------------------------------

        if total_exposure > 0:

            concentration = (
                top_exposure
                /
                total_exposure
            ) * 100.0

        else:

            concentration = 0.0

        # ----------------------------------------------------
        # Highest scoring gate
        # ----------------------------------------------------

        highest_gate = df.iloc[0]

        # ----------------------------------------------------
        # Mean score comparison
        # ----------------------------------------------------

        top_mean = top_gates[
            "Contextual_Exposure_Score"
        ].mean()

        overall_mean = df[
            "Contextual_Exposure_Score"
        ].mean()

        if overall_mean > 0:

            relative_exposure = (
                top_mean
                /
                overall_mean
            )

        else:

            relative_exposure = 0.0

        # ----------------------------------------------------
        # Store results
        # ----------------------------------------------------

        contextual_ranking.append({

            "Circuit":
                family,

            "Qubits":
                n,

            "Total_Gates":
                len(df),

            "Top_10_Percent_Gates":
                top_count,

            "Highest_Exposure_Gate":
                int(
                    highest_gate[
                        "Gate_Index"
                    ]
                ),

            "Maximum_Contextual_Score":
                highest_gate[
                    "Contextual_Exposure_Score"
                ],

            "Top_10_Exposure_Concentration_%":
                concentration,

            "Top_10_Mean_Exposure":
                top_mean,

            "Overall_Mean_Exposure":
                overall_mean,

            "Relative_Top_Exposure":
                relative_exposure
        })


# ------------------------------------------------------------
# Create dataframe
# ------------------------------------------------------------

contextual_ranking_df = pd.DataFrame(
    contextual_ranking
)


# ------------------------------------------------------------
# Round values
# ------------------------------------------------------------

contextual_ranking_df[
    [
        "Maximum_Contextual_Score",
        "Top_10_Exposure_Concentration_%",
        "Top_10_Mean_Exposure",
        "Overall_Mean_Exposure",
        "Relative_Top_Exposure"
    ]
] = contextual_ranking_df[
    [
        "Maximum_Contextual_Score",
        "Top_10_Exposure_Concentration_%",
        "Top_10_Mean_Exposure",
        "Overall_Mean_Exposure",
        "Relative_Top_Exposure"
    ]
].round(6)


# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print(
    "============================================================"
)

print(
    "CONTEXTUAL EXPOSURE RANKING AND CONCENTRATION"
)

print(
    "============================================================\n"
)

print(
    contextual_ranking_df.to_string(
        index=False
    )
)

print(
    "\nCell 6 completed successfully."
)
