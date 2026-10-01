from fpdf import FPDF

pdf = FPDF()
pdf.add_page()

pdf.set_font("Helvetica", size=14)

pdf.write(
    10,
    "Visit our website: "
)

pdf.set_text_color(0, 0, 255)
pdf.write(
    10,
    "The Pentecostal Matrimony",
    link="https://example.com"
)

pdf.output("output.pdf")