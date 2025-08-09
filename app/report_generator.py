
import os
from pylatex import Document, Section, Figure, NoEscape
from pylatex.utils import italic

def generate_full_report(doc_title, author, date, client, stats, visuals, insights, anomalies, recommendations, output_path):
    """
    Generates a professional PDF report using the pylatex library.
    """
    geometry_options = {"tmargin": "1in", "lmargin": "1in"}
    doc = Document(geometry_options=geometry_options)

    # --- Title Page ---
    doc.preamble.append(NoEscape(r'\title{' + doc_title + r'}'))
    doc.preamble.append(NoEscape(r'\author{' + author + r'}'))
    doc.preamble.append(NoEscape(r'\date{' + date + r'}'))
    doc.append(NoEscape(r'\maketitle'))
    doc.append(NoEscape(r'\thispagestyle{empty}'))
    doc.append(NoEscape(r'\newpage'))

    # --- Table of Contents ---
    doc.append(NoEscape(r'\tableofcontents'))
    doc.append(NoEscape(r'\newpage'))

    # --- Executive Summary ---
    with doc.create(Section('Executive Summary')):
        doc.append("This report provides a comprehensive analysis of...")
        doc.append("\n\nKey findings include:")
        doc.append(NoEscape(r'\begin{itemize}'))
        doc.append(NoEscape(r'\item Key finding 1...'))
        doc.append(NoEscape(r'\item Key finding 2...'))
        doc.append(NoEscape(r'\item Key finding 3...'))
        doc.append(NoEscape(r'\end{itemize}'))

    # --- Data Overview ---
    with doc.create(Section('Data Overview')):
        doc.append("The data used in this analysis comes from...")
        # Add more details about the data

    # --- Descriptive Statistics ---
    with doc.create(Section('Descriptive Statistics')):
        doc.append("The following table summarizes the descriptive statistics of the numeric columns:")
        doc.append(italic('\n(Placeholder for summary tables)\n'))
        doc.append(stats)

    # --- Exploratory Data Analysis (EDA) ---
    with doc.create(Section('Exploratory Data Analysis (EDA)')):
        doc.append("This section explores the data through visualizations.")
        for chart_type, chart_paths in visuals.items():
            with doc.create(Section(chart_type.replace('_', ' ').title(), numbering=False)):
                for chart_path in chart_paths:
                    with doc.create(Figure(position='htbp')) as fig:
                        fig.add_image(chart_path, width=NoEscape(r'\linewidth'))

    # --- Key Insights & Trends ---
    with doc.create(Section('Key Insights & Trends')):
        doc.append(italic('(Placeholder for insights and trends)\n'))
        doc.append(insights)

    # --- Anomalies & Exceptions ---
    with doc.create(Section('Anomalies & Exceptions')):
        doc.append(italic('(Placeholder for anomalies and exceptions)\n'))
        doc.append(anomalies)

    # --- Recommendations & Next Steps ---
    with doc.create(Section('Recommendations & Next Steps')):
        doc.append(italic('(Placeholder for recommendations and next steps)\n'))
        doc.append(recommendations)

    # --- Generate PDF ---
    doc.generate_pdf(output_path, clean_tex=False)
    return f"{output_path}.pdf"
