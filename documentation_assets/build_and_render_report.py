# -*- coding: utf-8 -*-
"""
YieldGrid CBP Master Report Assembly & PDF Rendering Script
Builds YieldGrid_CBP_Project_Report.docx and converts to YieldGrid_CBP_Project_Report.pdf.
Applies native page borders, footer page numbering, updates TOC, and calculates final page count.
"""

import os
import sys

# Ensure current directory is on python path
sys.path.insert(0, os.path.abspath('.'))

import docx
from docx.shared import Inches, Pt, RGBColor
import win32com.client

from documentation_assets.front_matter import build_front_matter
from documentation_assets.chapters_1_to_5 import build_chapters_1_to_5
from documentation_assets.chapter_6_design import build_chapter_6
from documentation_assets.chapter_7_implementation import build_chapter_7
from documentation_assets.chapters_8_to_10 import build_chapters_8_to_10

def generate_report():
    print("==================================================")
    print("Generating YieldGrid Academic Project Report...")
    print("==================================================")

    doc = docx.Document()

    # Configure Section 1 (Front Matter) margins
    sec1 = doc.sections[0]
    sec1.top_margin = Inches(0.5)
    sec1.bottom_margin = Inches(0.5)
    sec1.left_margin = Inches(1.0)
    sec1.right_margin = Inches(0.75)
    sec1.page_width = Inches(8.5)
    sec1.page_height = Inches(11.0)

    # Base Normal Style setup
    style_normal = doc.styles['Normal']
    style_normal.font.name = 'Times New Roman'
    style_normal.font.size = Pt(11.5)
    style_normal.font.color.rgb = RGBColor(15, 23, 42)

    # 1. Front Matter (Pages 1 to 6)
    print("Building Front Matter (Cover, Certificate, Declaration, Acknowledgement, Abstract, TOC)...")
    build_front_matter(doc)

    # 2. Add Section Break for Body Chapters
    print("Adding Section Break between Front Matter and Body Chapters...")
    sec2 = doc.add_section()
    sec2.top_margin = Inches(0.5)
    sec2.bottom_margin = Inches(0.5)
    sec2.left_margin = Inches(1.0)
    sec2.right_margin = Inches(0.75)
    sec2.page_width = Inches(8.5)
    sec2.page_height = Inches(11.0)

    # 3. Chapters 1 to 5
    print("Building Chapters 1 to 5...")
    build_chapters_1_to_5(doc)

    # 4. Chapter 6 (System Design)
    print("Building Chapter 6 (System Design)...")
    build_chapter_6(doc)

    # 5. Chapter 7 (Implementation)
    print("Building Chapter 7 (Implementation)...")
    build_chapter_7(doc)

    # 6. Chapters 8 to 10 (Testing, Results, References)
    print("Building Chapters 8 to 10 (Testing, Analysis of Results, References)...")
    build_chapters_8_to_10(doc)

    # Save initial DOCX
    docx_path = os.path.abspath("YieldGrid_CBP_Project_Report.docx")
    pdf_path = os.path.abspath("YieldGrid_CBP_Project_Report.pdf")
    doc.save(docx_path)
    print(f"Base DOCX successfully written to: {docx_path}")

    # 7. Word COM Post-Processing: Page Borders, Numbering & PDF Conversion
    print("Initiating Microsoft Word COM automation...")
    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False

    try:
        w_doc = word.Documents.Open(docx_path)
        print(f"Document opened in Word. Sections count: {w_doc.Sections.Count}")

        # Configure Page Borders for all sections (1 pt single line)
        for sec in w_doc.Sections:
            for b_idx in [1, 2, 3, 4]: # Top, Left, Bottom, Right
                sec.Borders(b_idx).LineStyle = 1 # wdLineStyleSingle
                sec.Borders(b_idx).LineWidth = 8 # 1 pt width
            sec.Borders.DistanceFrom = 1 # wdBorderDistanceFromPage

        # Configure Footers and Page Numbers
        # Section 1 (Front Matter): No page number
        # Section 2 (Body): Starts numbering at 1 (Arabic numerals, centered)
        if w_doc.Sections.Count >= 2:
            s2 = w_doc.Sections(2)
            s2.Footers(1).LinkToPrevious = False
            p_nums = s2.Footers(1).PageNumbers
            p_nums.Add(1, True) # 1 = wdAlignPageNumberCenter, FirstPage = True
            p_nums.RestartNumberingAtSection = True
            p_nums.StartingNumber = 1

        # Update all fields
        w_doc.Fields.Update()

        # Compute page statistics
        page_count = w_doc.ComputeStatistics(2) # 2 = wdStatisticPages
        print(f"==================================================")
        print(f"RENDERED PAGE COUNT IN WORD: {page_count} pages")
        print(f"==================================================")

        # Print chapter page mapping
        print("Chapter Page Mapping:")
        for p in w_doc.Paragraphs:
            txt = p.Range.Text.strip()
            if txt.startswith('CHAPTER') or txt.startswith('REFERENCES') or txt.startswith('CERTIFICATE'):
                phys_page = p.Range.Information(3) # wdActiveEndPageNumber
                sec_page = p.Range.Information(1) # wdActiveEndAdjustedPageNumber
                print(f"  {txt[:35]:35s} -> Phys: {phys_page:2d}, Sec: {sec_page:2d}")

        # Save finalized DOCX
        w_doc.Save()
        print("Finalized DOCX saved.")

        # Export to PDF (17 is wdExportFormatPDF)
        w_doc.SaveAs(pdf_path, 17)
        print(f"Finalized PDF successfully exported to: {pdf_path}")

        w_doc.Close(False)
    finally:
        word.Quit()

    print("Master build complete!")
    return page_count

if __name__ == '__main__':
    generate_report()
