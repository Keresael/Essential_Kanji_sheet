import sys
from dataclasses import dataclass
from pathlib import Path
from fpdf import FPDF


def _resource_dir() -> Path:
    """Return the directory that contains bundled resources (font file).
    Works both in normal Python and as a PyInstaller frozen bundle."""
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)  # type: ignore[attr-defined]
    return Path(__file__).parent


def _output_dir() -> Path:
    """Return the default directory for PDF output."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent  # next to the binary
    return Path(__file__).parent.parent  # project root in dev


FONT_PATH = _resource_dir() / "KanjiStrokeOrders_v4.005.ttf"
DEFAULT_OUTPUT = _output_dir() / "essential_kanji_sheet.pdf"


# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SheetLayout:
    """All sizing/spacing constants for the kanji practice sheet."""

    # Page
    page_w: float = 210
    margin: float = 5
    block_padding: float = 2.5

    # Column 1 – writing practice
    col1_w: float = 30
    large_box_size: float = 30
    box_v_gap: float = 5

    # Column 2 – info
    col_gap: float = 10

    # Reading rows
    label_w: float = 20
    reading_box_h: float = 9
    reading_box_gap: float = 4

    # Stroke practice
    stroke_box_size: float = 14
    stroke_box_gap: float = 3

    # Spaced-repetition checkboxes
    check_box_size: float = 5
    check_box_gap: float = 2
    check_label_h: float = 4

    # Sentence box
    sentence_box_h: float = 50
    sentence_line_h: float = 8

    @property
    def content_x(self) -> float:
        return self.margin + self.block_padding

    @property
    def content_y(self) -> float:
        return self.margin + self.block_padding

    @property
    def col2_w(self) -> float:
        return (self.page_w - 2 * self.margin) - (2 * self.block_padding) - self.col1_w - self.col_gap

    @property
    def col2_x(self) -> float:
        return self.content_x + self.col1_w + self.col_gap

    @property
    def reading_box_w(self) -> float:
        return self.col2_w - self.label_w - 2  # small gap before box


LAYOUT = SheetLayout()


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _draw_demo_column(pdf: FPDF, layout: SheetLayout, kanji_char: str) -> float:
    """Draw the left column (Kanji / Kun / On practice boxes).

    Returns the total column height so the outer border can be sized correctly.
    """
    labels = ["Kanji:", "Kun:", "On:"]
    x = layout.content_x + 2
    y = layout.content_y + 2

    for label in labels:
        # Label above box
        pdf.set_xy(x, y - 2)
        pdf.cell(0, 0, label)

        # Box
        pdf.rect(x, y, layout.large_box_size, layout.large_box_size)

        if label == "Kanji:" and kanji_char:
            # Draw glyph centred inside the box (y has not been advanced yet)
            pdf.set_font("Kanji", size=50)
            pdf.set_xy(x, y)
            pdf.cell(
                w=layout.large_box_size,
                h=layout.large_box_size,
                text=kanji_char,
                align="C",
            )
            pdf.set_font("Helvetica", "", 10)

        y += layout.large_box_size + layout.box_v_gap

    total_height = y - layout.box_v_gap - layout.content_y
    return total_height


def _draw_info_column(pdf: FPDF, layout: SheetLayout) -> float:
    """Draw the right column (readings, stroke practice, checkboxes, sentence box).

    Returns the total column height so the outer border can be sized correctly.
    """
    y = layout.content_y + 2

    # --- Reading rows ---
    reading_labels = ["Significati:", "Letture On:", "Letture Kun:", "Radicali:"]
    for label in reading_labels:
        pdf.set_xy(layout.col2_x, y + (layout.reading_box_h / 2) - 2)
        pdf.cell(layout.label_w, 0, label, align="R")
        pdf.rect(layout.col2_x + layout.label_w + 2, y, layout.reading_box_w, layout.reading_box_h)
        y += layout.reading_box_h + layout.reading_box_gap

    # --- Stroke practice boxes ---
    practice_row_y = y + 10
    x = layout.col2_x
    for _ in range(8):
        pdf.rect(x, practice_row_y, layout.stroke_box_size, layout.stroke_box_size)
        x += layout.stroke_box_size + layout.stroke_box_gap

    # --- Spaced-repetition checkboxes ---
    check_labels = ["D0", "D1", "D3", "D7", "D14"]
    x = layout.col2_x
    pdf.set_font_size(8)
    for label in check_labels:
        pdf.set_xy(x, y - layout.check_label_h + 2)
        pdf.cell(layout.check_box_size, 0, label, align="C")
        pdf.rect(x, y + 3, layout.check_box_size, layout.check_box_size)
        x += layout.check_box_size + layout.check_box_gap
    pdf.set_font_size(10)

    # --- Sentence box ---
    sentence_y = practice_row_y + layout.stroke_box_size + 10
    pdf.rect(layout.col2_x, sentence_y, layout.col2_w, layout.sentence_box_h)

    # Ruled lines inside sentence box
    pdf.set_draw_color(160, 160, 160)
    pdf.set_line_width(0.3)
    num_lines = int(layout.sentence_box_h / layout.sentence_line_h)
    line_y = sentence_y + 9
    for _ in range(num_lines):
        pdf.line(layout.col2_x + 2, line_y, layout.col2_x + layout.col2_w - 2, line_y)
        line_y += layout.sentence_line_h

    # Reset draw settings
    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.5)

    total_height = (sentence_y + layout.sentence_box_h) - layout.content_y
    return total_height


def _draw_outer_border(pdf: FPDF, layout: SheetLayout, col1_h: float, col2_h: float) -> None:
    """Draw the outer border rectangle around all content."""
    total_content_height = max(col1_h, col2_h)
    block_w = layout.page_w - 2 * layout.margin
    block_h = total_content_height + 2 * layout.block_padding
    pdf.rect(layout.margin, layout.margin, block_w, block_h)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def create_kanji_sheet(kanji_char: str, output_path: Path | str | None = None) -> None:
    """Generate a single-page kanji practice sheet and save it to *output_path*."""
    out = Path(output_path) if output_path is not None else DEFAULT_OUTPUT
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    pdf.add_font(family="Kanji", fname=str(FONT_PATH))

    pdf.set_draw_color(0, 0, 0)
    pdf.set_line_width(0.30)
    pdf.set_font("Helvetica", "", 10)

    col1_h = _draw_demo_column(pdf, LAYOUT, kanji_char)
    col2_h = _draw_info_column(pdf, LAYOUT)
    _draw_outer_border(pdf, LAYOUT, col1_h, col2_h)

    pdf.output(str(out))
