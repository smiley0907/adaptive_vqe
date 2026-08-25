# ============================================================
# CELL 5: Top-10% Contextual Exposure Gate Identification
# ============================================================

contextual_regions = {}
contextual_region_summary = []

PERCENTILE_THRESHOLD = 90


for family in CIRCUIT_FAMILIES:

    contextual_regions[family] = {}

    for n in QUBIT_CONFIGS:

        df = contextual_exposure_profiles[
            family
        ][n].copy()

        # ----------------------------------------------------
        # Circuit-specific percentile threshold
        # ----------------------------------------------------

        threshold = np.percentile(
            df["Contextual_Exposure_Score"],
            PERCENTILE_THRESHOLD
        )

        df["Exposure_Threshold"] = threshold

        df["High_Exposure"] = (
            df["Contextual_Exposure_Score"]
            >= threshold
        )

        # ----------------------------------------------------
        # Identify high exposure gates
        # ----------------------------------------------------

        high_indices = df.index[
            df["High_Exposure"]
        ].tolist()

        # ----------------------------------------------------
        # Group consecutive high exposure gates
        # ----------------------------------------------------

        regions = []

        if high_indices:

            start = high_indices[0]
            previous = high_indices[0]

            for idx in high_indices[1:]:

                if idx == previous + 1:

                    previous = idx

                else:

                    regions.append(
                        (start, previous)
                    )

                    start = idx
                    previous = idx

            regions.append(
                (start, previous)
            )

        # ----------------------------------------------------
        # Region records
        # ----------------------------------------------------

        region_records = []

        for region_id, (
            start,
            end
        ) in enumerate(
            regions,
            start=1
        ):

            region_df = df.loc[
                start:end
            ]

            region_records.append({

                "Region_ID":
                    region_id,

                "Start_Gate":
                    start,

                "End_Gate":
                    end,

                "Region_Size":
                    len(region_df),

                "Maximum_Contextual_Score":
                    region_df[
                        "Contextual_Exposure_Score"
                    ].max(),

                "Mean_Contextual_Score":
                    region_df[
                        "Contextual_Exposure_Score"
                    ].mean()
            })

        region_table = pd.DataFrame(
            region_records
        )

        # ----------------------------------------------------
        # Store detailed information
        # ----------------------------------------------------

        contextual_regions[
            family
        ][n] = {

            "Gate_Profile":
                df,

            "Regions":
                region_table,

            "Threshold":
                threshold
        }

        # ----------------------------------------------------
        # Summary
        # ----------------------------------------------------

        high_gate_count = int(
            df["High_Exposure"].sum()
        )

        region_count = len(
            region_records
        )

        largest_region = max(
            [
                r["Region_Size"]
                for r in region_records
            ],
            default=0
        )

        maximum_score = df[
            "Contextual_Exposure_Score"
        ].max()

        contextual_region_summary.append({

            "Circuit":
                family,

            "Qubits":
                n,

            "Exposure_Threshold":
                threshold,

            "High_Exposure_Gates":
                high_gate_count,

            "High_Exposure_Regions":
                region_count,

            "Largest_Region":
                largest_region,

            "Maximum_Contextual_Score":
                maximum_score
        })


# ------------------------------------------------------------
# Summary dataframe
# ------------------------------------------------------------

contextual_region_summary_df = pd.DataFrame(
    contextual_region_summary
)


# ------------------------------------------------------------
# Round values
# ------------------------------------------------------------

contextual_region_summary_df[
    [
        "Exposure_Threshold",
        "Maximum_Contextual_Score"
    ]
] = contextual_region_summary_df[
    [
        "Exposure_Threshold",
        "Maximum_Contextual_Score"
    ]
].round(8)


# ------------------------------------------------------------
# Display
# ------------------------------------------------------------

print(
    "============================================================"
)

print(
    "TOP-10% CONTEXTUAL EXPOSURE GATE IDENTIFICATION"
)

print(
    "============================================================\n"
)

print(
    contextual_region_summary_df.to_string(
        index=False
    )
)

print(
    "\nExposure percentile threshold:",
    PERCENTILE_THRESHOLD
)

print(
    "\nCell 5 completed successfully."
)
