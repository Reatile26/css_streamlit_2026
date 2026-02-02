from pathlib import Path
import streamlit as st
import pandas as pd

# Optional: PDF text extraction (only for previews)
try:
    import PyPDF2
except Exception:
    PyPDF2 = None


# =========================
# Robust Paths (work locally + on Streamlit Cloud)
# =========================
BASE_DIR = Path(__file__).resolve().parent
ASSETS = BASE_DIR / "assets"

PROFILE_PHOTO = ASSETS / "profile.jpg"
DEV_ECON_PDF  = ASSETS / "dev_econ.pdf"
INT_ECON_PDF  = ASSETS / "int_econ.pdf"
EOY_PDF       = ASSETS / "eoy.pdf"


# =========================
# Helpers
# =========================
def exists(path: Path) -> bool:
    return path is not None and path.exists()

def download_button(label: str, path: Path, file_name: str, mime: str):
    if not exists(path):
        st.warning(f"Missing file: {path.name}. Check it exists inside the assets/ folder in GitHub.")
        return

    with open(path, "rb") as f:
        st.download_button(
            label=label,
            data=f.read(),
            file_name=file_name,
            mime=mime,
            use_container_width=True
        )

@st.cache_data(show_spinner=False)
def extract_pdf_text(path: Path, max_chars: int = 12000) -> str:
    """Extract text from a PDF (best-effort)."""
    if not exists(path) or PyPDF2 is None:
        return ""

    try:
        text_parts = []
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                t = page.extract_text() or ""
                if t.strip():
                    text_parts.append(t.strip())
        text = "\n\n".join(text_parts)
        return text[:max_chars] + ("\n\n[Preview truncated]" if len(text) > max_chars else "")
    except Exception:
        return ""

def bullet_list(items):
    for x in items:
        st.write(f"• {x}")


# =========================
# Main App
# =========================
def main():
    st.set_page_config(
        page_title="Reatile Seekoei | Economics & Data Portfolio",
        layout="wide",
    )

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    menu = st.sidebar.radio(
        "Go to:",
        ["Profile", "Writing & Research", "Economist of the Year", "Economics & Data Explorer", "Contact"]
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Deployed via GitHub + Streamlit Cloud")

    # =========================
    # Profile
    # =========================
    if menu == "Profile":
        col1, col2 = st.columns([1, 2], gap="large")

        with col1:
            st.title("Reatile Seekoei")
            st.caption("BComHons Business Analytics • University of the Free State")

            if exists(PROFILE_PHOTO):
                st.image(PROFILE_PHOTO, caption="Profile Photo", use_container_width=True)
            else:
                st.info(
                    "Profile photo not found. Ensure you have assets/profile.jpg in your GitHub repo "
                    "and that the filename matches exactly."
                )

        with col2:
            st.header("About Me")
            st.write(
                "I am a student with a strong interest in economics, development challenges, and "
                "data-driven analysis. I enjoy turning complex theory into clear insight through writing, "
                "presentations, and interactive tools."
            )

            st.subheader("Focus Areas")
            bullet_list([
                "Development economics (environment–development nexus, sustainability, inequality)",
                "International economics (technology, trade, productivity, labour market shifts)",
                "Macroeconomic reasoning & forecasting frameworks",
                "Data storytelling and dashboard-style reporting",
            ])

            st.subheader("Links")
            st.text_input("Email", value="reatileseekoei@gmail.com")
            st.text_input("LinkedIn", value="https://www.linkedin.com/in/reatile-seekoei-6252b6228/")
            st.text_input("GitHub", value="https://github.com/Reatile26")

    # =========================
    # Writing & Research
    # =========================
    elif menu == "Writing & Research":
        st.title("Writing & Research")
        st.caption("Your essays with summaries + download links")

        tab1, tab2 = st.tabs(["Development Economics Essay", "International Economics Essay"])

        with tab1:
            st.subheader("Development Economics Essay")
            bullet_list([
                "Explores development challenges in Sub-Saharan Africa through an environment–development lens.",
                "Discusses sustainability, inequality, and the balance between growth and ecological limits.",
                "Builds an argument around structural constraints and long-term policy relevance.",
            ])

            download_button(
                "Download Development Economics Essay (PDF)",
                DEV_ECON_PDF,
                "Development_Economics_Essay.pdf",
                "application/pdf",
            )

            if PyPDF2 is None:
                st.info("Install PyPDF2 for text preview: pip install PyPDF2 (and add it to requirements.txt)")
            else:
                preview = extract_pdf_text(DEV_ECON_PDF)
                if preview:
                    with st.expander("Preview extracted text (best-effort)"):
                        st.write(preview)

        with tab2:
            st.subheader("International Economics Essay")
            bullet_list([
                "Examines how technological innovation reshapes global trade and productivity.",
                "Considers labour market impacts: skills, displacement, job restructuring.",
                "Highlights the need for inclusion and narrowing digital divides.",
            ])

            download_button(
                "Download International Economics Essay (PDF)",
                INT_ECON_PDF,
                "International_Economics_Essay.pdf",
                "application/pdf",
            )

            if PyPDF2 is None:
                st.info("Install PyPDF2 for text preview: pip install PyPDF2 (and add it to requirements.txt)")
            else:
                preview = extract_pdf_text(INT_ECON_PDF)
                if preview:
                    with st.expander("Preview extracted text (best-effort)"):
                        st.write(preview)

    # =========================
    # Economist of the Year
    # =========================
    elif menu == "Economist of the Year":
        st.title("Economist of the Year (EOY)")
        st.caption("Competitive forecasting and macroeconomic reasoning")

        st.subheader("EOY Presentation")
        bullet_list([
            "Demonstrates a structured forecasting approach grounded in data and policy signals.",
            "Highlights key macro indicators and disciplined reasoning under uncertainty.",
            "Reflects growth in economic interpretation and communication.",
        ])

        download_button(
            "Download EOY Presentation (PDF)",
            EOY_PDF,
            "EOY_Presentation.pdf",
            "application/pdf",
        )

        st.markdown("### Key takeaways (editable)")
        st.text_area(
            "What do you want viewers to remember?",
            value=(
                "• I built a structured forecasting framework combining data trends with policy/market signals.\n"
                "• I communicate uncertainty clearly and justify forecasts with evidence.\n"
                "• I improved my macroeconomic interpretation and presentation ability."
            ),
            height=140,
        )

    # =========================
    # Economics & Data Explorer
    # =========================
    elif menu == "Economics & Data Explorer":
        st.title("Economics & Data Explorer")
        st.caption("Upload a CSV and explore it with filters + quick charts")

        uploaded = st.file_uploader("Upload a CSV dataset", type=["csv"])

        if uploaded:
            try:
                df = pd.read_csv(uploaded)
            except Exception as e:
                st.error(f"Could not read CSV: {e}")
                return

            st.success(f"Loaded {df.shape[0]:,} rows × {df.shape[1]:,} columns")
            st.dataframe(df, use_container_width=True)

            st.markdown("### Filter")
            col = st.selectbox("Choose a column to filter", df.columns.tolist())

            if pd.api.types.is_numeric_dtype(df[col]):
                lo, hi = st.slider("Select range", float(df[col].min()), float(df[col].max()),
                                   (float(df[col].min()), float(df[col].max())))
                filtered = df[df[col].between(lo, hi)]
            else:
                vals = sorted(df[col].dropna().astype(str).unique().tolist())
                picks = st.multiselect("Select values", vals, default=vals[: min(6, len(vals))])
                filtered = df[df[col].astype(str).isin(picks)] if picks else df

            st.write("### Filtered data")
            st.dataframe(filtered, use_container_width=True)

            st.markdown("### Quick chart")
            numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
            if numeric_cols:
                chart_col = st.selectbox("Choose numeric column", numeric_cols)
                st.line_chart(filtered[chart_col])
            else:
                st.info("No numeric columns found for charting.")
        else:
            st.info("Upload any CSV (inflation, GDP, exchange rates, returns) to explore it here.")

    # =========================
    # Contact
    # =========================
    elif menu == "Contact":
        st.title("Contact")
        st.caption("Professional contact section")

        st.text_input("Email", value="reatileseekoei@gmail.com")
        st.text_input("LinkedIn", value="https://www.linkedin.com/in/reatile-seekoei-6252b6228/")

        st.markdown("### Message ")
        with st.form("contact_form"):
            sender = st.text_input("Your name")
            message = st.text_area("Message", height=140)
            submitted = st.form_submit_button("Submit")

        if submitted:
            st.success("Message captured (demo).")
            st.write("**From:**", sender)
            st.write("**Message:**", message)


if __name__ == "__main__":
    main()
