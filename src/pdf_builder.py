from fpdf import *

def pdf_builder(kanji):
    pdf = FPDF()
    pdf.add_page()

    pdf.add_font("Kanji", style="", fname="../KanjiStrokeOrders_v4.005.ttf")
    pdf.set_font("Kanji", size=110)
    pdf.text(kanji, 10, "Kanji")


    pdf.output("pdf.pdf")