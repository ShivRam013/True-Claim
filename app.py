import json
import html

import streamlit as st

from main import verify_claim


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="True Claim | AI Claim Verification",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown(
    """
    <style>

    /* Main layout */

    .block-container {
        max-width: 1450px;
        width: 92%;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Header */

    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 0.2rem;
    }

    .main-subtitle {
        font-size: 1rem;
        color: #9ca3af;
        margin-bottom: 0.8rem;
    }

    .description {
        color: #a1a1aa;
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
    }

    /* Section labels */

    .section-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: #9ca3af;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 0.7rem;
    }

    /* Verdict cards */

    .verdict-card {
        padding: 1.5rem;
        border-radius: 14px;
        border: 1px solid;
        margin: 0.5rem 0 1rem 0;
    }

    .verdict-supported {
        background: rgba(22, 163, 74, 0.12);
        border-color: rgba(34, 197, 94, 0.45);
    }

    .verdict-contradicted {
        background: rgba(220, 38, 38, 0.12);
        border-color: rgba(239, 68, 68, 0.45);
    }

    .verdict-insufficient {
        background: rgba(202, 138, 4, 0.12);
        border-color: rgba(234, 179, 8, 0.45);
    }

    .verdict-title {
        font-size: 1.5rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }

    .verdict-description {
        color: #a1a1aa;
        font-size: 0.9rem;
    }

    /* Evidence cards */

    .evidence-card {
        padding: 1.2rem;
        border-radius: 12px;
        background: rgba(128, 128, 128, 0.07);
        border: 1px solid rgba(128, 128, 128, 0.2);
        min-height: 110px;
    }

    .evidence-number {
        font-size: 2rem;
        font-weight: 800;
    }

    .evidence-label {
        color: #a1a1aa;
        font-size: 0.85rem;
    }

    /* Sidebar */

    [data-testid="stSidebar"] {
        padding-top: 1rem;
    }

    /* Buttons */

    div.stButton > button {
        border-radius: 9px;
        font-weight: 650;
        min-height: 45px;
    }

    /* Text area */

    textarea {
        border-radius: 10px !important;
    }

    /* Dividers */

    hr {
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
        border-color: rgba(128, 128, 128, 0.2);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("## 🔍 True Claim")

    st.caption(
        "AI-powered scientific claim verification "
        "using evidence-based reasoning."
    )

    st.divider()

    st.markdown("### How it works")

    st.markdown(
        """
        **01.** Enter a claim

        **02.** Retrieve relevant evidence

        **03.** Analyze supporting and contradicting evidence

        **04.** Generate a final verdict
        """
    )

    st.divider()

    st.markdown("### Technology")

    st.markdown(
        """
        - LangGraph
        - LangChain
        - Advanced RAG
        - Hybrid Search
        - GraphRAG
        - Neo4j
        - Groq / LLM
        - RAGAS
        - LangSmith
        - Streamlit
        """
    )

    st.divider()

    st.markdown("### About")

    st.caption(
        "True Claim investigates scientific and factual "
        "claims using retrieved evidence and AI reasoning."
    )

    st.divider()

    st.caption(
        "AI-assisted verification. Always consult "
        "the cited sources before making important decisions."
    )


# =====================================================
# MAIN HEADER
# =====================================================

st.markdown(
    '<div class="main-title">🔍 True Claim</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'AI-Powered Scientific Claim Verification'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="description">'
    'Investigate claims using evidence retrieval, '
    'graph-based reasoning, and an agentic AI workflow.'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =====================================================
# CLAIM INPUT
# =====================================================

st.markdown(
    '<div class="section-label">START AN INVESTIGATION</div>',
    unsafe_allow_html=True
)

st.markdown("### Enter your claim")

st.caption(
    "Enter a scientific or factual claim that you want "
    "True Claim to investigate."
)

with st.form("claim_form"):

    claim = st.text_area(
        "Claim",
        placeholder=(
            "Example: The Student Placement Prediction System "
            "dataset contains approximately 100,000 student records."
        ),
        height=130,
        label_visibility="collapsed"
    )

    submitted = st.form_submit_button(
        "🔍 Investigate Claim",
        type="primary",
        use_container_width=True
    )


# =====================================================
# RUN INVESTIGATION
# =====================================================

if submitted:

    if not claim.strip():

        st.warning("Please enter a claim before starting.")

    else:

        try:

            with st.spinner(
                "Investigating claim using evidence and AI reasoning..."
            ):

                verdict, report_json = verify_claim(claim)

                report = json.loads(report_json)

            # Save results in Streamlit session state

            st.session_state["investigation_report"] = report
            st.session_state["investigation_verdict"] = verdict
            st.session_state["investigation_claim"] = claim

            st.success("Investigation completed!")

        except Exception as error:

            st.error("An error occurred during the investigation.")

            st.exception(error)


# =====================================================
# DISPLAY INVESTIGATION RESULTS
# =====================================================

if "investigation_report" in st.session_state:

    report = st.session_state["investigation_report"]

    verdict = report.get(
        "verdict",
        st.session_state.get("investigation_verdict", "Insufficient")
    )

    confidence = report.get("confidence", "Unknown")

    st.divider()

    # -------------------------------------------------
    # INVESTIGATED CLAIM
    # -------------------------------------------------

    st.markdown(
        '<div class="section-label">INVESTIGATED CLAIM</div>',
        unsafe_allow_html=True
    )

    st.info(st.session_state["investigation_claim"])


    # -------------------------------------------------
    # FINAL VERDICT
    # -------------------------------------------------

    st.markdown(
        '<div class="section-label">FINAL VERDICT</div>',
        unsafe_allow_html=True
    )

    verdict_styles = {
        "Supported": {
            "class": "verdict-supported",
            "icon": "✅",
            "description": "The available evidence supports this claim."
        },
        "Contradicted": {
            "class": "verdict-contradicted",
            "icon": "❌",
            "description": "The available evidence contradicts this claim."
        },
        "Insufficient": {
            "class": "verdict-insufficient",
            "icon": "⚠️",
            "description": "There is insufficient evidence to determine this claim."
        }
    }

    style = verdict_styles.get(
        verdict,
        verdict_styles["Insufficient"]
    )

    safe_verdict = html.escape(str(verdict))
    safe_confidence = html.escape(str(confidence))
    safe_description = html.escape(style["description"])

    st.markdown(
        f"""
        <div class="verdict-card {style['class']}">
            <div class="verdict-title">
                {style['icon']} {safe_verdict}
            </div>
            <div class="verdict-description">
                {safe_description}
            </div>
            <br>
            <strong>Confidence:</strong> {safe_confidence}
        </div>
        """,
        unsafe_allow_html=True
    )


    # -------------------------------------------------
    # AI REASONING
    # -------------------------------------------------

    st.markdown(
        '<div class="section-label">AI REASONING</div>',
        unsafe_allow_html=True
    )

    st.markdown("### 🧠 Why this verdict?")

    reasoning = report.get(
        "reasoning",
        "No reasoning available."
    )

    st.write(reasoning)


    # -------------------------------------------------
    # EVIDENCE ANALYSIS
    # -------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-label">EVIDENCE ANALYSIS</div>',
        unsafe_allow_html=True
    )

    supporting = report.get(
        "supporting_evidence",
        []
    )

    contradicting = report.get(
        "contradicting_evidence",
        []
    )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            f"""
            <div class="evidence-card">
                <div class="evidence-number">
                    {len(supporting)}
                </div>
                <div class="evidence-label">
                    ✅ Supporting Evidence
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            f"""
            <div class="evidence-card">
                <div class="evidence-number">
                    {len(contradicting)}
                </div>
                <div class="evidence-label">
                    ❌ Contradicting Evidence
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("#### Supporting Evidence IDs")

        if supporting:

            for evidence_id in supporting:

                st.write(f"Evidence ID: `{evidence_id}`")

        else:

            st.caption("No supporting evidence found.")

    with col2:

        st.markdown("#### Contradicting Evidence IDs")

        if contradicting:

            for evidence_id in contradicting:

                st.write(f"Evidence ID: `{evidence_id}`")

        else:

            st.caption("No contradicting evidence found.")


    # -------------------------------------------------
    # CITATIONS
    # -------------------------------------------------

    st.divider()

    st.markdown(
        '<div class="section-label">SOURCES & CITATIONS</div>',
        unsafe_allow_html=True
    )

    citations = report.get("citations", {})

    supporting_citations = citations.get(
        "supporting",
        []
    )

    contradicting_citations = citations.get(
        "contradicting",
        []
    )

    citation_groups = [
        ("Supporting Sources", supporting_citations),
        ("Contradicting Sources", contradicting_citations)
    ]

    citation_count = sum(
        len(group) for _, group in citation_groups
    )

    if citation_count:

        st.caption(f"{citation_count} citation(s) available.")

        for group_name, group in citation_groups:

            if group:

                st.markdown(f"#### {group_name}")

                for index, citation in enumerate(group, start=1):

                    source = citation.get(
                        "source",
                        "Unknown source"
                    )

                    page = citation.get(
                        "page",
                        "Unknown"
                    )

                    subclaim = citation.get(
                        "subclaim",
                        ""
                    )

                    evidence_text = citation.get(
                        "text",
                        ""
                    )

                    with st.expander(
                        f"📄 {source} — Page {page}"
                    ):

                        st.markdown(f"**Citation {index}**")

                        if subclaim:

                            st.markdown(
                                f"**Subclaim:** {subclaim}"
                            )

                        st.markdown("**Evidence:**")

                        st.write(evidence_text)

    else:

        st.caption("No citations available.")


    # -------------------------------------------------
    # LIMITATIONS
    # -------------------------------------------------

    limitations = report.get(
        "limitations",
        []
    )

    if limitations:

        st.divider()

        st.markdown(
            '<div class="section-label">LIMITATIONS</div>',
            unsafe_allow_html=True
        )

        st.markdown("### ⚠️ Investigation Limitations")

        for limitation in limitations:

            st.markdown(f"- {limitation}")


    # -------------------------------------------------
    # RAW REPORT (OPTIONAL)
    # -------------------------------------------------

    st.divider()

    with st.expander("View complete investigation report"):

        st.json(report)


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "True Claim | AI-Powered Scientific Claim Verification"
)