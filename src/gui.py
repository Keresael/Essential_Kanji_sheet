import subprocess
import threading
import tkinter as tk
from tkinter import ttk

from pdf_builder import create_kanji_sheet, DEFAULT_OUTPUT


def main_gui(root: tk.Tk) -> None:
    """Build and attach the main GUI to *root*."""
    root.title("Essential Kanji sheet")

    mainframe = ttk.Frame(root, padding=(3, 3, 12, 12))
    mainframe.grid(column=0, row=0, sticky=tk.N)

    kanji_var = tk.StringVar()
    kanji_entry = ttk.Entry(mainframe, width=7, textvariable=kanji_var)
    kanji_entry.grid(column=1, row=1, sticky=tk.N)

    ttk.Label(mainframe, text="Kanji").grid(column=2, row=1, sticky=tk.W)

    add_info_var = tk.BooleanVar()
    ttk.Checkbutton(mainframe, text="Add info", variable=add_info_var).grid(
        column=1, row=3, sticky=tk.N
    )

    status_var = tk.StringVar()
    status_label = ttk.Label(mainframe, textvariable=status_var, foreground="gray")
    status_label.grid(column=1, row=5, columnspan=2, sticky=tk.W, pady=(4, 0))

    generate_btn = ttk.Button(mainframe, text="Genera PDF")
    generate_btn.grid(column=2, row=4, sticky=tk.S)

    def _generate() -> None:
        kanji_char = kanji_var.get().strip()
        if not kanji_char:
            return

        generate_btn.configure(state="disabled")
        status_var.set("Generazione in corso…")

        def _run() -> None:
            try:
                create_kanji_sheet(kanji_char)
                # Apri automaticamente il PDF appena creato
                subprocess.Popen(["xdg-open", str(DEFAULT_OUTPUT)])
                root.after(0, lambda k=kanji_char: status_var.set(
                    f'\u2713 PDF generato per \u201c{k}\u201d \u2192 {DEFAULT_OUTPUT.name}'
                ))
            except Exception as exc:
                root.after(0, lambda e=exc: status_var.set(f'\u2717 Errore: {e}'))
            finally:
                root.after(0, lambda: generate_btn.configure(state="normal"))

        threading.Thread(target=_run, daemon=True).start()

    generate_btn.configure(command=_generate)
