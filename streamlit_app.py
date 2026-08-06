import streamlit as st
import pandas as pd

from engine import analyze_dataframe

st.set_page_config(
    page_title="FlyRank AI",
    page_icon="",
    layout="wide"
)

st.title(" FlyRank AI Content Opportunity Engine")

st.markdown(
    "Analyze SEO datasets using AI-powered opportunity scoring, "
    "intent classification, and Gemini recommendations."
)

st.divider()

uploaded_file = st.file_uploader(
    " Upload SEO Dataset (.csv)",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.success(f" {uploaded_file.name} uploaded successfully!")

    st.subheader("Dataset Preview")

    st.dataframe(
        df,
        use_container_width=True
    )

    if st.button(
        "🚀 Analyze Dataset",
        type="primary",
        use_container_width=True
    ):

        with st.spinner("Analyzing dataset with AI..."):

            report = analyze_dataframe(df)

        st.success(" Analysis Complete!")

        # =====================================
        # KPI CARDS
        # =====================================

        st.subheader(" Dashboard")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                " Total Pages",
                len(report)
            )

        with col2:
            st.metric(
                " Avg Score",
                round(report["Opportunity Score"].mean(), 1)
            )

        with col3:
            st.metric(
                " High Priority",
                len(report[report["Priority"] == "High"])
            )

        with col4:
            st.metric(
                " Avg CTR",
                f"{report['ctr'].mean():.2f}%"
            )

        st.divider()

        # =====================================
        # REPORT TABLE
        # =====================================

        st.subheader(" SEO Opportunity Report")

        st.dataframe(
            report[
                [
                    "Priority Rank",
                    "page",
                    "query",
                    "Opportunity Score",
                    "Priority",
                    "Intent"
                ]
            ],
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # =====================================
        # AI RECOMMENDATIONS
        # =====================================

        st.subheader(" AI Recommendations")

        for _, row in report.iterrows():

            with st.expander(
                f"#{row['Priority Rank']} | {row['page']}"
            ):

                st.markdown(f"###  Query")
                st.write(row["query"])

                st.markdown(f"###  Search Intent")
                st.info(row["Intent"])

                st.markdown(f"###  Opportunity Score")
                st.progress(
                    min(row["Opportunity Score"] / 100, 1.0)
                )
                st.write(f"{row['Opportunity Score']:.1f}/100")

                st.markdown("###  Priority")
                st.success(row["Priority"])

                st.markdown("###  Best Action")
                st.write(row["Best Action"])

                st.markdown("###  Gemini Recommendation")
                st.write(row["AI Recommendation"])

        st.divider()

        # =====================================
        # DOWNLOAD REPORT
        # =====================================

        csv = report.to_csv(index=False)

        st.download_button(
            label="⬇ Download Opportunity Report",
            data=csv,
            file_name="opportunity_report.csv",
            mime="text/csv",
            use_container_width=True
        )
