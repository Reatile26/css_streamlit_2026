import os
import streamlit as st
import pandas as pd


# Optional PDF text extraction
try:
    import PyPDF2
except Exception:
    PyPDF2 = None


# =========================
# PATHS (robust + based on file location)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROFILE_PHOTO = os.path.join(BASE_DIR, "Reatile Prof Photo - Copy (1).jpg")
DEV_ECON_PDF  = os.path.join(BASE_DIR, "EDEV ESSAY ASSIGNMENT.pdf")
INT_ECON_PDF  = os.path.join(BASE_DIR, "Reatile Seekoei - 2021109463.pdf")
EOY_PDF       = os.path.join(BASE_DIR, "ReatileSeekoei_EoY_Oct2025.pdf")


# =========================
# HELPERS
# =========================
def exists(path: str) -> bool:
    return isinstance(path, str) and os.path.exists(path)

def download_button(label: str, path: str, file_name: str, mime: str):
    if not exists(path):
        st.warning(f"Missing file: {os.path.basename(path)} (check it’s in the same folder as run_streamlit.py)")
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
def extract_pdf_text(path: str, max_chars: int = 12000) -> str:
    """Extract text from a PDF (best-effort)."""
    if not exists(path):
        return ""
    if PyPDF2 is None:
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

def section_header(title: str, subtitle: str = ""):
    st.title(title)
    if subtitle:
        st.caption(subtitle)

def bullet_list(items):
    for x in items:
        st.write(f"• {x}")


# =========================
# MAIN APP
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

    

    # =========================
    # PROFILE
    # =========================
    if menu == "Profile":
        col1, col2 = st.columns([1, 2], gap="large")

        with col1:
            section_header("Reatile Seekoei", "BComHons Business Analytics• University of the Free State")

            if exists(PROFILE_PHOTO):
                st.image(PROFILE_PHOTO, caption="Profile Photo", use_container_width=True)
            else:
                st.info("Profile photo not found. Ensure it is in the same folder and the filename matches exactly.")

        with col2:
            st.header("About Me")
            st.write(
                "I am a driven finance student with an open-minded approach to learning. I’m pursuing a career in finance to deepen my understanding and strengthen my financial acumen. I’m also keenly interested in coding and data analysis, which complement my analytical mindset and problem-solving approach. I strive to make a meaningful impact wherever I go — as a problem solver, an innovator, and someone who adds measurable value."
            )

            st.subheader("Focus Areas")
            bullet_list([
                "Development economics (environment–development nexus, sustainability, inequality)",
                "International economics (technology, trade, productivity, labour market shifts)",
                "Macroeconomic reasoning & forecasting frameworks (policy signals + data)",
                "Data storytelling and clean visual analysis",
            ])


            st.subheader("Quick Links")
            st.text_input("Email", value="reatileseekoei@gmail.com")
            st.text_input("LinkedIn", value="https://www.linkedin.com/in/reatile-seekoei-6252b6228/")
            st.text_input("GitHub", value="https://github.com/Reatile26")

    # =========================
    # WRITING & RESEARCH
    # =========================
    elif menu == "Writing & Research":
        section_header("Writing & Research", "Your essays, key themes, and downloadable files")

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
                st.info("Install PyPDF2 for text preview: pip install PyPDF2")
            else:
                preview = extract_pdf_text(DEV_ECON_PDF)
                if preview:
                    with st.expander("Preview extracted text (best-effort)"):
                        st.write(preview)
                else:
                    st.info("No preview extracted (some PDFs don’t allow clean text extraction).")

        with tab2:
            st.subheader("International Economics Essay")
            

            bullet_list([
                "Examines how technological innovation reshapes global trade and productivity.",
                "Considers labour market implications (skills, displacement, job restructuring).",
                "Highlights policy emphasis on inclusion and narrowing digital divides.",
            ])

            download_button(
                "Download International Economics Essay (PDF)",
                INT_ECON_PDF,
                "International_Economics_Essay.pdf",
                "application/pdf",
            )

            if PyPDF2 is None:
                st.info("Install PyPDF2 for text preview: pip install PyPDF2")
            else:
                preview = extract_pdf_text(INT_ECON_PDF)
                if preview:
                    with st.expander("Preview extracted text (best-effort)"):
                        st.write(preview)
                else:
                    st.info("No preview extracted (some PDFs don’t allow clean text extraction).")

    # =========================
    # ECONOMIST OF THE YEAR
    # =========================
    elif menu == "Economist of the Year":
        section_header("Economist of the Year (EOY)")

        st.subheader("EOY Presentation")
        st.caption("File: ReatileSeekoei_EoY_Oct2025.pdf")

        bullet_list([
            "Demonstrates a structured forecasting approach grounded in data and policy signals.",
            "Highlights key macro indicators and disciplined reasoning under uncertainty.",
            "Reflects growth in economic interpretation, communication, and presentation skills.",
        ])

        download_button(
            "Download EOY Presentation (PDF)",
            EOY_PDF,
            "EOY_Presentation.pdf",
            "application/pdf",
        )

        st.markdown("### Key takeaways (edit these to match your exact message)")
        st.text_area(
            "What do you want people to remember?",
            value=(
                "• I built a structured forecasting framework that combines data trends with policy/market signals.\n"
                "• I learned to communicate uncertainty clearly and justify forecasts with evidence.\n"
                "• I improved my macroeconomic thinking and presentation ability under pressure."
            ),
            height=150,
        )

        if PyPDF2 is not None:
            preview = extract_pdf_text(EOY_PDF)
            if preview:
                with st.expander("Preview extracted text (best-effort)"):
                    st.write(preview)

    # =========================
    # ECONOMICS & DATA EXPLORER
    # =========================
    elif menu == "Economics & Data Explorer":
        section_header("Economics & Data Explorer", "Upload a CSV and explore it (filters + quick charts)")

        uploaded = st.file_uploader("Upload a CSV dataset", type=["csv"])

        if uploaded:
            try:
                df = pd.read_csv(uploaded)
            except Exception as e:
                st.error(f"Could not read CSV: {e}")
                return

            st.success(f"Loaded {df.shape[0]:,} rows × {df.shape[1]:,} columns")
            st.dataframe(df, use_container_width=True)

            st.markdown("### Quick stats")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Rows", f"{df.shape[0]:,}")
            with c2:
                st.metric("Columns", f"{df.shape[1]:,}")
            with c3:
                st.metric("Missing values", f"{int(df.isna().sum().sum()):,}")

            st.markdown("### Filter")
            col = st.selectbox("Choose a column to filter", df.columns.tolist())

            if pd.api.types.is_numeric_dtype(df[col]):
                min_v = float(df[col].min())
                max_v = float(df[col].max())
                lo, hi = st.slider("Range", min_v, max_v, (min_v, max_v))
                filtered = df[df[col].between(lo, hi)]
            else:
                unique_vals = sorted(df[col].dropna().astype(str).unique().tolist())
                picks = st.multiselect("Select values", unique_vals, default=unique_vals[: min(6, len(unique_vals))])
                filtered = df[df[col].astype(str).isin(picks)] if picks else df

            st.write("### Filtered data")
            st.dataframe(filtered, use_container_width=True)

            st.markdown("### Quick chart")
            numeric_cols = [c for c in df.columns if pd.api.types.is_numeric_dtype(df[c])]
            if numeric_cols:
                chart_col = st.selectbox("Select numeric column", numeric_cols)
                st.line_chart(filtered[chart_col])
            else:
                st.info("No numeric columns found for charting.")
        else:
            st.info("Upload any CSV (e.g., inflation, GDP, exchange rates, stock returns) to explore it here.")

    # =========================
    # CONTACT
    # =========================
    elif menu == "Contact":
        section_header("Contact", "Professional contact section")

    

        st.text_input("Email", value="reatileseekoei@gmail.com")
        st.text_input("LinkedIn", value="https://www.linkedin.com/in/reatile-seekoei-6252b6228/")

        st.markdown("### Message (demo)")
        with st.form("contact_form"):
            name = st.text_input("Your name")
            message = st.text_area("Message", height=140)
            submitted = st.form_submit_button("Submit")

        if submitted:
            st.success("Message captured (demo).")
            st.write("**From:**", name)
            st.write("**Message:**", message)


# Allows running directly: streamlit run app_profiler_menus.py
if __name__ == "__main__":
    main()
