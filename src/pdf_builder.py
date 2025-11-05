from fpdf import FPDF

def create_kanji_sheet():
     # --- Costanti di Layout (in mm) ---
    # Dimensioni Pagina
    PAGE_W = 210
    MARGIN = 5
    BLOCK_PADDING = 2.5 # Il padding interno del .kanji-block

    # Coordinate di partenza del contenuto (dopo il padding del blocco)
    CONTENT_X_START = MARGIN + BLOCK_PADDING
    CONTENT_Y_START = MARGIN + BLOCK_PADDING

    # Colonna 1 (Sinistra - Pratica Scrittura)
    COL1_W = 30
    LARGE_BOX_SIZE = 30
    BOX_V_GAP = 5  # Spazio verticale tra i box grandi

    # Colonna 2 (Destra - Info)
    COL_GAP = 10
    COL2_X_START = CONTENT_X_START + COL1_W + COL_GAP

    # Larghezza Colonna 2 = Larghezza Pagina - margini - padding - col1 - gap
    COL2_W = (PAGE_W - 2 * MARGIN) - (2 * BLOCK_PADDING) - COL1_W - COL_GAP

    #Tabella per Esercitazioni
    LABEL_W = 20  # Larghezza etichette (Significati:, On:, etc.)
    READING_BOX_H = 9  # Altezza box letture
    READING_BOX_GAP = 4  # Spazio tra box letture
    READING_BOX_W = COL2_W - LABEL_W - 2  # -2 per un piccolo stacco

    STROKE_BOX_SIZE = 14
    STROKE_BOX_GAP = 3

    # Tabella per le ripetizioni
    CHECK_BOX_SIZE = 5
    CHECK_BOX_GAP = 2
    CHECK_LABEL_H = 4 # Spazio fra box e etichetta ripetizioni

    SENTENCE_BOX_H = 50  # Altezza box frasi
    SENTENCE_LINE_H = 8

    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    #pdf.set_auto_page_break(False)

    # Impostazioni di disegno
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.30)  # Simula 2px border
    pdf.set_font("Helvetica", "", 10)

    # Tabella caratteri dimostrativi
    current_y = CONTENT_Y_START + 2
    current_x = CONTENT_X_START + 2
    labels = ["Kanji:", "Kun:", "On:"]

    for label in labels:
        #etichetta
        pdf.set_xy(current_x, current_y - 2)
        pdf.cell(0, 0, label)
        #box
        pdf.rect(current_x, current_y, LARGE_BOX_SIZE, LARGE_BOX_SIZE)
        current_y += LARGE_BOX_SIZE + BOX_V_GAP

    # Salva l'altezza totale della colonna 1
    col1_total_height = current_y - BOX_V_GAP - CONTENT_Y_START

    #Tabella per Esercitazioni
    current_y = CONTENT_Y_START + 2

    #Letture
    reading_labels = ["Significati:", "Letture On:", "Letture Kun:", "Radicali:"]

    for label in reading_labels:
        #etichetta
        pdf.set_xy(COL2_X_START, current_y + (READING_BOX_H / 2) - 2)  # Centra verticalmente
        pdf.cell(LABEL_W, 0, label, align="R")
        #box
        pdf.rect(COL2_X_START + LABEL_W + 2, current_y, READING_BOX_W, READING_BOX_H)
        current_y += READING_BOX_H + READING_BOX_GAP

    # Riga Pratica (Stroke order + Checks)
    practice_row_y = current_y + 10  # Gap
    current_x = COL2_X_START

    # 8 Stroke boxes
    for _ in range(8):
        pdf.rect(current_x, practice_row_y, STROKE_BOX_SIZE, STROKE_BOX_SIZE)
        current_x += STROKE_BOX_SIZE + STROKE_BOX_GAP

    current_x = COL2_X_START

    # Tabella per le ripetizioni
    check_labels = ["D0", "D1", "D3", "D7", "D14"]

    pdf.set_font_size(8)
    for label in check_labels:
        # Etichetta
        pdf.set_xy(current_x, current_y - CHECK_LABEL_H + 1)
        pdf.cell(CHECK_BOX_SIZE, 0, label, align="C")
        # Box
        pdf.rect(current_x, current_y, CHECK_BOX_SIZE, CHECK_BOX_SIZE)
        current_x += CHECK_BOX_SIZE + CHECK_BOX_GAP

    pdf.set_font_size(10)  # Resetta font

    # Box Frasi
    current_y = practice_row_y + STROKE_BOX_SIZE + 10  # Gap

    pdf.rect(COL2_X_START, current_y, COL2_W, SENTENCE_BOX_H)

    # Righe nel box frasi
    pdf.set_draw_color(160, 160, 160)  # Grigio
    pdf.set_line_width(0.3)

    num_lines = int((SENTENCE_BOX_H - 10) / SENTENCE_LINE_H)  #Padding 5mm top/bottom
    line_y = current_y + 8  #Inizia con padding

    for _ in range(num_lines):
        pdf.line(COL2_X_START + 2, line_y, COL2_X_START + COL2_W - 2, line_y)
        line_y += SENTENCE_LINE_H

    #Resetta impostazioni disegno
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.5)

    #Salva altezza totale colonna 2
    col2_total_height = (current_y + SENTENCE_BOX_H) - CONTENT_Y_START

    # --- Bordo Esterno (kanji-block) ---

    # Calcola l'altezza massima basandosi sulla colonna più alta
    total_content_height = max(col1_total_height, col2_total_height)

    block_width = PAGE_W - (2 * MARGIN)
    block_height = total_content_height + (2 * BLOCK_PADDING)

    pdf.rect(MARGIN, MARGIN, block_width, block_height)

    # --- Output ---
    pdf.output("essential_kanji_sheet.pdf")
    print("File 'essential_kanji_sheet.pdf' creato con successo.")


if __name__ == "__main__":
    create_kanji_sheet()
