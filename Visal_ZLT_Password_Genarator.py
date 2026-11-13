
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import re

AMBIGUOUS = "1ILil"

BG = "#0b1120"
PANEL = "#151f32"
CARD = "#1c2940"
INPUT = "#101a2d"
BLUE = "#38bdf8"
BLUE_DARK = "#0284c7"
GREEN = "#16a34a"
WHITE = "#f1f5f9"
MUTED = "#94a3b8"
BORDER = "#293850"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


def alphabet_char(m):
    return chr(48 + m) if m < 10 else chr(55 + m) if m < 36 else chr(61 + m)


def generate_from(data, filter_ambiguous=True, numeric_only=False):
    if not data:
        return ""

    out = []

    for i in range(8):
        seed = 1

        for j in range(len(data)):
            while seed > 0xFFFFFF:
                seed = (~seed) & 0xFFFFFF

            idx = (i + j) % len(data)
            product = ((i + 1) * (j + 1)) & 0xFF
            seed += data[idx] * product

        while seed > 0xFFFFFF:
            seed = (~seed) & 0xFFFFFF

        if numeric_only:
            ch = chr(48 + (seed % 10))
        else:
            ch = alphabet_char(seed % 52)

            if filter_ambiguous and ch in AMBIGUOUS:
                ch = chr(ord(ch) + 1)

        out.append(ch)

    return "".join(out)


def format_mac_bytes(mac):
    filtered = re.sub(r"[^0-9A-Fa-f]", "", mac).upper()
    pairs = [filtered[i:i + 2] for i in range(0, len(filtered), 2)]
    formatted = ":".join(pairs)
    return [ord(c) for c in formatted], formatted


def operator_pass(imei):
    c = re.sub(r"\s+", "", str(imei or ""))

    if len(c) < 15:
        return None

    return generate_from([ord(ch) for ch in c])


def user_pass(mac):
    data, _ = format_mac_bytes(mac or "")

    if not data:
        return None

    return generate_from(data)


def test_password(imei):
    c = re.sub(r"\s+", "", str(imei or ""))

    if len(c) < 15:
        return None

    if not all("0" <= ch <= "9" for ch in c):
        return None

    r = c[7:15]
    acc = 0
    out = []

    for i in range(8):
        acc = i + acc + (ord(r[i]) - 48)
        out.append(chr(48 + (acc % 10)))

    return "".join(out)


class VisalZLTPasswordGenerator:

    def __init__(self, root):
        self.root = root

        self.root.title("Visal ZLT Password Generator v1.0")
        self.root.geometry("1100x800")
        self.root.minsize(900, 900)
        self.root.configure(fg_color=BG)

        self.results = {
            "imei": "",
            "mac": "",
            "test": "",
            "operator": "",
            "user": ""
        }

        self.format_var = tk.StringVar(value="TXT")

        self.create_ui()

    def create_ui(self):

        main = ctk.CTkFrame(
            self.root,
            fg_color="transparent"
        )
        main.pack(fill="both", expand=True, padx=30, pady=25)

        self.create_header(main)

        content = ctk.CTkFrame(
            main,
            fg_color="transparent"
        )
        content.pack(fill="both", expand=True, pady=(25, 0))

        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        self.create_input_panel(content)
        self.create_output_panel(content)

        self.create_footer(main)

    def create_header(self, parent):

        header = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        header.pack(fill="x")

        branding = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )
        branding.pack(side="left")

        logo = ctk.CTkFrame(
            branding,
            width=58,
            height=58,
            corner_radius=16,
            fg_color=BLUE_DARK
        )
        logo.pack(side="left", padx=(0, 15))
        logo.pack_propagate(False)

        ctk.CTkLabel(
            logo,
            text="V",
            font=("Segoe UI", 29, "bold"),
            text_color=WHITE
        ).pack(expand=True)

        title_frame = ctk.CTkFrame(
            branding,
            fg_color="transparent"
        )
        title_frame.pack(side="left")

        ctk.CTkLabel(
            title_frame,
            text="VISAL ZLT",
            font=("Segoe UI", 25, "bold"),
            text_color=BLUE
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="PASSWORD GENERATOR",
            font=("Segoe UI", 11, "bold"),
            text_color=WHITE
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="IMEI & MAC password generation tool",
            font=("Segoe UI", 9),
            text_color=MUTED
        ).pack(anchor="w", pady=(3, 0))

        export = ctk.CTkFrame(
            header,
            fg_color=PANEL,
            corner_radius=16,
            border_width=1,
            border_color=BORDER
        )
        export.pack(side="right")

        ctk.CTkLabel(
            export,
            text="EXPORT RESULTS",
            font=("Segoe UI", 10, "bold"),
            text_color=WHITE
        ).pack(anchor="w", padx=16, pady=(12, 7))

        options = ctk.CTkFrame(
            export,
            fg_color="transparent"
        )
        options.pack(fill="x", padx=15)

        self.format_selector = ctk.CTkSegmentedButton(
            options,
            values=["TXT", "PDF"],
            variable=self.format_var,
            selected_color=BLUE_DARK,
            selected_hover_color="#0369a1",
            unselected_color=INPUT,
            unselected_hover_color=CARD,
            text_color=WHITE,
            corner_radius=10,
            border_width=0,
            font=("Segoe UI", 10, "bold")
        )
        self.format_selector.pack(fill="x")

        self.rounded_button(
            export,
            "↓   DOWNLOAD",
            self.download_results,
            GREEN,
            "#15803d",
            height=36
        ).pack(fill="x", padx=15, pady=12)

    def create_input_panel(self, parent):

        panel = ctk.CTkFrame(
            parent,
            fg_color=PANEL,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        panel.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 12)
        )

        panel.grid_columnconfigure(0, weight=1)

        inner = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )
        inner.pack(fill="both", expand=True, padx=22, pady=22)

        self.section_title(
            inner,
            "DEVICE INFORMATION",
            "Enter your router device details."
        )

        self.imei_entry = self.create_input(
            inner,
            "IMEI NUMBER",
            "Enter 15-digit IMEI"
        )

        self.mac_entry = self.create_input(
            inner,
            "MAC ADDRESS",
            "Example: FC:3F:FC:90:90:90"
        )

        self.rounded_button(
            inner,
            "GENERATE PASSWORDS     →",
            self.generate,
            BLUE_DARK,
            "#0369a1",
            height=48
        ).pack(fill="x", pady=(23, 12))

        self.separator(inner)

        self.small_heading(inner, "SUPPORTED INPUTS")

        self.info_card(inner, "IMEI", "15 numeric digits")
        self.info_card(inner, "MAC", "12 hexadecimal characters")

        ctk.CTkLabel(
            inner,
            text="You can enter either one or both values.",
            font=("Segoe UI", 9),
            text_color=MUTED
        ).pack(anchor="w", pady=(15, 0))

    def create_output_panel(self, parent):

        panel = ctk.CTkFrame(
            parent,
            fg_color=PANEL,
            corner_radius=18,
            border_width=1,
            border_color=BORDER
        )

        panel.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(12, 0)
        )

        inner = ctk.CTkFrame(
            panel,
            fg_color="transparent"
        )
        inner.pack(fill="both", expand=True, padx=22, pady=22)

        self.section_title(
            inner,
            "GENERATED PASSWORDS",
            "Your generated passwords appear below."
        )

        self.test_output = self.create_output(
            inner,
            "TEST PASSWORD",
            "Numeric password",
            "01"
        )

        self.operator_output = self.create_output(
            inner,
            "OPERATOR PASSWORD",
            "IMEI-based password",
            "02"
        )

        self.user_output = self.create_output(
            inner,
            "USER PASSWORD",
            "MAC-based password",
            "03"
        )

        self.separator(inner)

        self.small_heading(inner, "PASSWORD INFORMATION")

        ctk.CTkLabel(
            inner,
            text="Generate passwords before downloading.\n"
                 "Use COPY to copy individual results.",
            font=("Segoe UI", 9),
            text_color=MUTED,
            justify="left"
        ).pack(anchor="w", pady=(10, 0))

    def create_footer(self, parent):

        footer = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        footer.pack(fill="x", pady=(20, 0))

        self.separator(footer)

        self.rounded_button(
            footer,
            "CLEAR ALL",
            self.clear_all,
            "#26364d",
            "#334155",
            height=37,
            width=120
        ).pack(side="left", pady=(13, 0))

        ctk.CTkLabel(
            footer,
            text="Made by Visal",
            font=("Segoe UI", 9),
            text_color=MUTED
        ).pack(side="right", pady=(23, 0))

    def section_title(self, parent, title, subtitle):

        ctk.CTkLabel(
            parent,
            text=title,
            font=("Segoe UI", 13, "bold"),
            text_color=WHITE
        ).pack(anchor="w")

        ctk.CTkLabel(
            parent,
            text=subtitle,
            font=("Segoe UI", 9),
            text_color=MUTED
        ).pack(anchor="w", pady=(5, 23))

    def small_heading(self, parent, text):

        ctk.CTkLabel(
            parent,
            text=text,
            font=("Segoe UI", 9, "bold"),
            text_color=BLUE
        ).pack(anchor="w", pady=(0, 10))

    def separator(self, parent):

        ctk.CTkFrame(
            parent,
            height=1,
            fg_color=BORDER,
            corner_radius=1
        ).pack(fill="x", pady=18)

    def rounded_button(
        self,
        parent,
        text,
        command,
        color,
        hover,
        height=42,
        width=None
    ):

        return ctk.CTkButton(
            parent,
            text=text,
            command=command,
            height=height,
            width=width or 0,
            corner_radius=11,
            fg_color=color,
            hover_color=hover,
            text_color=WHITE,
            font=("Segoe UI", 10, "bold"),
            border_width=0,
            cursor="hand2"
        )

    def create_input(self, parent, label, placeholder):

        frame = ctk.CTkFrame(
            parent,
            fg_color="transparent"
        )
        frame.pack(fill="x", pady=(0, 17))

        ctk.CTkLabel(
            frame,
            text=label,
            font=("Segoe UI", 9, "bold"),
            text_color="#cbd5e1"
        ).pack(anchor="w", pady=(0, 8))

        entry = ctk.CTkEntry(
            frame,
            placeholder_text=placeholder,
            height=48,
            corner_radius=12,
            border_width=1,
            border_color=BORDER,
            fg_color=INPUT,
            text_color=WHITE,
            placeholder_text_color="#64748b",
            font=("Consolas", 12)
)

        entry.pack(fill="x")

        return entry

    def info_card(self, parent, label, description):

        card = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            corner_radius=11
        )
        card.pack(fill="x", pady=5)

        ctk.CTkLabel(
            card,
            text=label,
            font=("Segoe UI", 9, "bold"),
            text_color=BLUE,
            width=55
        ).pack(side="left", padx=(12, 5), pady=12)

        ctk.CTkLabel(
            card,
            text=description,
            font=("Segoe UI", 9),
            text_color=WHITE
        ).pack(side="left", pady=12)

    def create_output(self, parent, label, description, number):

        frame = ctk.CTkFrame(
            parent,
            fg_color=CARD,
            corner_radius=14,
            border_width=1,
            border_color=BORDER
        )
        frame.pack(fill="x", pady=(0, 13))

        top = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )
        top.pack(fill="x", padx=13, pady=(12, 0))

        ctk.CTkLabel(
            top,
            text=number,
            font=("Segoe UI", 8, "bold"),
            text_color=BLUE,
            fg_color=INPUT,
            corner_radius=6,
            width=27,
            height=24
        ).pack(side="left")

        ctk.CTkLabel(
            top,
            text=label,
            font=("Segoe UI", 9, "bold"),
            text_color=WHITE
        ).pack(side="left", padx=9)

        ctk.CTkLabel(
            frame,
            text=description,
            font=("Segoe UI", 8),
            text_color=MUTED
        ).pack(anchor="w", padx=13, pady=(6, 9))

        bottom = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )
        bottom.pack(fill="x", padx=12, pady=(0, 12))

        output = ctk.CTkEntry(
            bottom,
            height=39,
            corner_radius=9,
            border_width=1,
            border_color=BORDER,
            fg_color=INPUT,
            text_color=BLUE,
            font=("Consolas", 14, "bold"),
            state="readonly"
        )
        output.pack(side="left", fill="x", expand=True)

        self.rounded_button(
            bottom,
            "COPY",
            lambda: self.copy_output(output),
            "#334155",
            BLUE_DARK,
            height=39,
            width=65
        ).pack(side="right", padx=(9, 0))

        return output

    def set_output(self, widget, value):

        widget.configure(state="normal")
        widget.delete(0, "end")
        widget.insert(0, value or "")
        widget.configure(state="readonly")

    def copy_output(self, widget):

        value = widget.get()

        if not value:
            messagebox.showwarning(
                "Copy",
                "There is no password to copy."
            )
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(value)
        self.root.update()

        messagebox.showinfo(
            "Copied",
            "Password copied to clipboard."
        )

    def generate(self):

        imei = self.imei_entry.get().strip()
        mac = self.mac_entry.get().strip()

        clean_imei = re.sub(r"\s+", "", imei)
        clean_mac = re.sub(r"[^0-9A-Fa-f]", "", mac)

        if not clean_imei and not clean_mac:
            messagebox.showwarning(
                "Input Required",
                "Enter an IMEI number or MAC address."
            )
            return

        if clean_imei and (
            len(clean_imei) != 15
            or not all("0" <= ch <= "9" for ch in clean_imei)
        ):
            messagebox.showerror(
                "Invalid IMEI",
                "IMEI must contain exactly 15 digits."
            )
            return

        if clean_mac and len(clean_mac) != 12:
            messagebox.showerror(
                "Invalid MAC",
                "MAC address must contain exactly 12 hexadecimal characters."
            )
            return

        test = test_password(clean_imei) if clean_imei else ""
        operator = operator_pass(clean_imei) if clean_imei else ""
        user = user_pass(mac) if clean_mac else ""

        _, formatted_mac = format_mac_bytes(mac)

        self.results = {
            "imei": clean_imei,
            "mac": formatted_mac if clean_mac else "",
            "test": test or "",
            "operator": operator or "",
            "user": user or ""
        }

        self.set_output(self.test_output, test)
        self.set_output(self.operator_output, operator)
        self.set_output(self.user_output, user)

    def build_text(self):

        r = self.results

        return (
            "################# Visal_ZLT_Password_Genarator ##################\n\n"
            f"IMEI - {r['imei'] or 'Not provided'}\n"
            f"MAC - {r['mac'] or 'Not provided'}\n\n"
            "#################################################################\n"
            f"Test password - {r['test'] or 'Not generated'}\n"
            f"Operator password is - {r['operator'] or 'Not generated'}\n"
            f"User password is - {r['user'] or 'Not generated'}\n\n"
            "#################################################################\n"
        )

    def download_results(self):

        if not any([
            self.results["test"],
            self.results["operator"],
            self.results["user"]
        ]):
            messagebox.showwarning(
                "No Results",
                "Generate passwords before downloading."
            )
            return

        selected_format = self.format_var.get()

        if selected_format == "TXT":
            extension = ".txt"
            filetypes = [("Text files", "*.txt")]
        else:
            extension = ".pdf"
            filetypes = [("PDF files", "*.pdf")]

        filepath = filedialog.asksaveasfilename(
            title="Save Password Results",
            initialfile="Visal_ZLT_Passwords" + extension,
            defaultextension=extension,
            filetypes=filetypes
        )

        if not filepath:
            return

        try:

            if selected_format == "TXT":
                with open(filepath, "w", encoding="utf-8") as file:
                    file.write(self.build_text())
            else:
                self.save_pdf(filepath)

            messagebox.showinfo(
                "Download Complete",
                f"Results saved successfully:\n{filepath}"
            )

        except ImportError:
            messagebox.showerror(
                "PDF Package Missing",
                "Install using:\n\npy -m pip install reportlab"
            )

        except Exception as error:
            messagebox.showerror(
                "Save Error",
                str(error)
            )

    def save_pdf(self, filepath):

        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib import colors
        from reportlab.lib.units import mm
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle
        )

        r = self.results

        document = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            rightMargin=22 * mm,
            leftMargin=22 * mm,
            topMargin=25 * mm,
            bottomMargin=25 * mm
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "GeneratorTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=19,
            textColor=colors.HexColor("#075985"),
            spaceAfter=8
        )

        normal_style = ParagraphStyle(
            "GeneratorNormal",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=17
        )

        story = [
            Paragraph("Visal ZLT Password Generator", title_style),
            Paragraph("Made by Visal", normal_style),
            Spacer(1, 22)
        ]

        details = [
            ["IMEI", r["imei"] or "Not provided"],
            ["MAC", r["mac"] or "Not provided"]
        ]

        details_table = Table(
            details,
            colWidths=[40 * mm, 110 * mm]
        )

        details_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#e0f2fe")),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1e293b")),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (1, 0), (1, -1), "Courier"),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("PADDING", (0, 0), (-1, -1), 10)
        ]))

        passwords = [
            ["Password Type", "Generated Password"],
            ["Test Password", r["test"] or "Not generated"],
            ["Operator Password", r["operator"] or "Not generated"],
            ["User Password", r["user"] or "Not generated"]
        ]

        password_table = Table(
            passwords,
            colWidths=[60 * mm, 90 * mm]
        )

        password_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#075985")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTNAME", (1, 1), (1, -1), "Courier-Bold"),
            ("TEXTCOLOR", (1, 1), (1, -1), colors.HexColor("#075985")),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("PADDING", (0, 0), (-1, -1), 12),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE")
        ]))

        story.extend([
            details_table,
            Spacer(1, 28),
            Paragraph("Generated Passwords", styles["Heading2"]),
            Spacer(1, 10),
            password_table,
            Spacer(1, 30),
            Paragraph("Visal_ZLT_Password_Genarator", normal_style)
        ])

        document.build(story)

    def clear_all(self):

        self.imei_entry.delete(0, "end")
        self.mac_entry.delete(0, "end")

        self.set_output(self.test_output, "")
        self.set_output(self.operator_output, "")
        self.set_output(self.user_output, "")

        self.results = {
            "imei": "",
            "mac": "",
            "test": "",
            "operator": "",
            "user": ""
        }


if __name__ == "__main__":

    root = ctk.CTk()
    app = VisalZLTPasswordGenerator(root)
    root.mainloop()
