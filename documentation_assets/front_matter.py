# -*- coding: utf-8 -*-
"""
Front Matter Builder for YieldGrid Academic Project Report
Contains Cover, Certificate, Declaration, Acknowledgement, Abstract, Table of Contents
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from documentation_assets.report_parts import (
    set_cell_margins, set_cell_shading, set_cell_border,
    add_heading_1, add_body_p
)

def build_front_matter(doc):
    # ----------------------------------------------------
    # PAGE 1: COVER PAGE
    # ----------------------------------------------------
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(10)
    p_logo.paragraph_format.space_after = Pt(8)
    r_logo = p_logo.add_run()
    if os.path.exists("documentation_assets/vnr_logo.jpg"):
        r_logo.add_picture("documentation_assets/vnr_logo.jpg", width=Inches(1.2))

    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(0)
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("VNR Vignana Jyothi Institute of Engineering and Technology\n(Affiliated to JNTU, Hyderabad)\nBachupally(v), Hyderabad, Telangana, India.")
    r_inst.bold = True
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(12)
    r_inst.font.color.rgb = RGBColor(11, 37, 69)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(36)
    p_title.paragraph_format.space_after = Pt(14)
    r_title = p_title.add_run("YIELDGRID — APPLICATION FOR FARM-TO-RETAIL INVENTORY")
    r_title.bold = True
    r_title.font.name = "Times New Roman"
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = RGBColor(11, 37, 69)

    p_stmt = doc.add_paragraph()
    p_stmt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_stmt.paragraph_format.space_before = Pt(0)
    p_stmt.paragraph_format.space_after = Pt(4)
    p_stmt.paragraph_format.line_spacing = 1.2
    r_stmt = p_stmt.add_run("A COURSE BASED PROJECT REPORT SUBMITTED IN PARTIAL FULFILLMENT OF\nTHE REQUIREMENTS FOR THE COMPLETION OF COURSE\n\"Object Oriented Programming Through Java Laboratory\"")
    r_stmt.font.name = "Times New Roman"
    r_stmt.font.size = Pt(11)
    r_stmt.font.color.rgb = RGBColor(30, 41, 59)

    p_deg = doc.add_paragraph()
    p_deg.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_deg.paragraph_format.space_before = Pt(24)
    p_deg.paragraph_format.space_after = Pt(18)
    r_deg = p_deg.add_run("BACHELOR OF TECHNOLOGY\nIN\nCSE - AIML")
    r_deg.bold = True
    r_deg.font.name = "Times New Roman"
    r_deg.font.size = Pt(13)
    r_deg.font.color.rgb = RGBColor(11, 37, 69)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(18)
    p_sub.paragraph_format.space_after = Pt(8)
    r_sub = p_sub.add_run("Submitted by")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(11.5)
    r_sub.italic = True

    # Team Members Table
    t_team = doc.add_table(rows=3, cols=2)
    t_team.alignment = WD_TABLE_ALIGNMENT.CENTER
    students = [
        ("Pervala Yashwanth", "26075A6610"),
        ("Yejju Sathyasai", "26075A6613"),
        ("Shaik Abdul Rasheed", "26075A6612")
    ]
    for idx, (name, roll) in enumerate(students):
        cell_name = t_team.cell(idx, 0)
        cell_roll = t_team.cell(idx, 1)
        cell_name.width = Inches(3.2)
        cell_roll.width = Inches(2.2)
        set_cell_margins(cell_name, 30, 30, 60, 60)
        set_cell_margins(cell_roll, 30, 30, 60, 60)
        
        p_n = cell_name.paragraphs[0]
        p_n.alignment = WD_ALIGN_PARAGRAPH.LEFT
        rn = p_n.add_run(name)
        rn.font.name = "Times New Roman"
        rn.font.size = Pt(11.5)
        rn.bold = True

        p_r = cell_roll.paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        rr = p_r.add_run(roll)
        rr.font.name = "Times New Roman"
        rr.font.size = Pt(11.5)
        rr.bold = True

    p_guide_lbl = doc.add_paragraph()
    p_guide_lbl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide_lbl.paragraph_format.space_before = Pt(28)
    p_guide_lbl.paragraph_format.space_after = Pt(2)
    rg_lbl = p_guide_lbl.add_run("Under the guidance of")
    rg_lbl.font.name = "Times New Roman"
    rg_lbl.font.size = Pt(11.5)
    rg_lbl.italic = True

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_before = Pt(0)
    p_guide.paragraph_format.space_after = Pt(0)
    rg = p_guide.add_run("Ms. K. Anitha\nAssistant Professor\nDepartment of Computer Science & Engineering (AI & ML) & IoT\nand R&AI")
    rg.bold = True
    rg.font.name = "Times New Roman"
    rg.font.size = Pt(11.5)
    rg.font.color.rgb = RGBColor(11, 37, 69)

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 2: CERTIFICATE
    # ----------------------------------------------------
    p_cert_logo = doc.add_paragraph()
    p_cert_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_logo.paragraph_format.space_before = Pt(8)
    p_cert_logo.paragraph_format.space_after = Pt(6)
    if os.path.exists("documentation_assets/vnr_logo.jpg"):
        p_cert_logo.add_run().add_picture("documentation_assets/vnr_logo.jpg", width=Inches(1.1))

    p_cert_inst = doc.add_paragraph()
    p_cert_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_inst.paragraph_format.space_before = Pt(0)
    p_cert_inst.paragraph_format.space_after = Pt(2)
    rc_inst = p_cert_inst.add_run("VNR Vignana Jyothi Institute of Engineering and Technology\n(Affiliated to JNTU, Hyderabad)\nBachupally(v), Hyderabad, Telangana, India.")
    rc_inst.bold = True
    rc_inst.font.name = "Times New Roman"
    rc_inst.font.size = Pt(11.5)
    rc_inst.font.color.rgb = RGBColor(11, 37, 69)

    p_cert_hd = doc.add_paragraph()
    p_cert_hd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cert_hd.paragraph_format.space_before = Pt(32)
    p_cert_hd.paragraph_format.space_after = Pt(20)
    rc_hd = p_cert_hd.add_run("CERTIFICATE")
    rc_hd.bold = True
    rc_hd.font.name = "Times New Roman"
    rc_hd.font.size = Pt(16)
    rc_hd.font.color.rgb = RGBColor(11, 37, 69)

    p_cert_body = doc.add_paragraph()
    p_cert_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert_body.paragraph_format.space_before = Pt(10)
    p_cert_body.paragraph_format.space_after = Pt(16)
    p_cert_body.paragraph_format.line_spacing = 1.3
    cert_text = (
        "This is to certify that they completed their course project work at Department of "
        "Computer Science & Engineering (AI & ML) & IoT and R&AI of VNR VJIET, Hyderabad entitled "
        "“YieldGrid — Application for Farm-to-Retail Inventory” in complete fulfilment of the requirements "
        "for the award of B. Tech degree during the academic year 2026-2027. This work is carried out under "
        "my supervision and has not been submitted to any other University/Institute for award of any degree/diploma."
    )
    r_cb = p_cert_body.add_run(cert_text)
    r_cb.font.name = "Times New Roman"
    r_cb.font.size = Pt(12)

    p_spc = doc.add_paragraph()
    p_spc.paragraph_format.space_before = Pt(90)
    p_spc.paragraph_format.space_after = Pt(0)

    # Signatures Table
    t_sig = doc.add_table(rows=1, cols=2)
    t_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_sup = t_sig.cell(0, 0)
    c_hod = t_sig.cell(0, 1)
    c_sup.width = Inches(3.2)
    c_hod.width = Inches(3.2)
    set_cell_margins(c_sup, 20, 20, 40, 40)
    set_cell_margins(c_hod, 20, 20, 40, 40)

    p_sup = c_sup.paragraphs[0]
    p_sup.alignment = WD_ALIGN_PARAGRAPH.LEFT
    rs_sup = p_sup.add_run(
        "Signature of Supervisor\n\n\n\n"
        "Ms. K. Anitha\n"
        "Assistant Professor\n"
        "Dept. of CSE - (AI & ML) & IoT\n"
        "and R&AI\n"
        "VNRVJIET, Hyderabad"
    )
    rs_sup.font.name = "Times New Roman"
    rs_sup.font.size = Pt(11)

    p_hod = c_hod.paragraphs[0]
    p_hod.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    rs_hod = p_hod.add_run(
        "Signature of HOD\n\n\n\n"
        "Dr. Sagar Yeruva\n"
        "Assoc. Professor & HOD\n"
        "Dept. of CSE - (AI & ML) & IoT\n"
        "and R&AI\n"
        "VNRVJIET, Hyderabad"
    )
    rs_hod.font.name = "Times New Roman"
    rs_hod.font.size = Pt(11)

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 3: DECLARATION
    # ----------------------------------------------------
    p_decl_hd = doc.add_paragraph()
    p_decl_hd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_decl_hd.paragraph_format.space_before = Pt(20)
    p_decl_hd.paragraph_format.space_after = Pt(24)
    rd_hd = p_decl_hd.add_run("DECLARATION")
    rd_hd.bold = True
    rd_hd.font.name = "Times New Roman"
    rd_hd.font.size = Pt(16)
    rd_hd.font.color.rgb = RGBColor(16, 75, 42)

    p_decl_body = doc.add_paragraph()
    p_decl_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_decl_body.paragraph_format.space_before = Pt(12)
    p_decl_body.paragraph_format.space_after = Pt(18)
    p_decl_body.paragraph_format.line_spacing = 1.3
    decl_text = (
        "This is to certify that our project report titled “YieldGrid — Application for Farm-to-Retail Inventory” "
        "submitted to Vallurupalli Nageswara Rao Institute of Engineering and Technology in complete fulfilment of "
        "requirement for the award of Bachelor of Technology in Computer Science and Engineering (AI & ML) & IoT "
        "and R&AI is a Bonafide report to the work carried out by us under the guidance and supervision of Ms. K. Anitha, "
        "Assistant Professor, Department of CSE (AI & ML) & IoT and R&AI, Vallurupalli Nageswara Rao Institute of "
        "Engineering and Technology. To the best of our knowledge, this has not been submitted in any form to other "
        "universities or institutions for the award of any degree or diploma."
    )
    r_db = p_decl_body.add_run(decl_text)
    r_db.font.name = "Times New Roman"
    r_db.font.size = Pt(12)

    p_dspc = doc.add_paragraph()
    p_dspc.paragraph_format.space_before = Pt(160)
    p_dspc.paragraph_format.space_after = Pt(0)

    # Student Declaration Table
    t_decl_students = doc.add_table(rows=2, cols=2)
    t_decl_students.alignment = WD_TABLE_ALIGNMENT.CENTER
    
    # Left: Yashwanth
    c00 = t_decl_students.cell(0, 0)
    c00.width = Inches(3.2)
    p00 = c00.paragraphs[0]
    p00.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r00 = p00.add_run("Pervala Yashwanth\n26075A6610\nCSE – AIML")
    r00.font.name = "Times New Roman"
    r00.font.size = Pt(11.5)

    # Right: Sathyasai
    c01 = t_decl_students.cell(0, 1)
    c01.width = Inches(3.2)
    p01 = c01.paragraphs[0]
    p01.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r01 = p01.add_run("Yejju Sathyasai\n26075A6613\nCSE – AIML")
    r01.font.name = "Times New Roman"
    r01.font.size = Pt(11.5)

    # Bottom Left: Abdul Rasheed
    c10 = t_decl_students.cell(1, 0)
    c10.width = Inches(3.2)
    p10 = c10.paragraphs[0]
    p10.paragraph_format.space_before = Pt(20)
    p10.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r10 = p10.add_run("Shaik Abdul Rasheed\n26075A6612\nCSE – AIML")
    r10.font.name = "Times New Roman"
    r10.font.size = Pt(11.5)

    c11 = t_decl_students.cell(1, 1)
    c11.width = Inches(3.2)

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 4: ACKNOWLEDGEMENT
    # ----------------------------------------------------
    p_ack_hd = doc.add_paragraph()
    p_ack_hd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_ack_hd.paragraph_format.space_before = Pt(20)
    p_ack_hd.paragraph_format.space_after = Pt(24)
    ra_hd = p_ack_hd.add_run("ACKNOWLEDGEMENT")
    ra_hd.bold = True
    ra_hd.font.name = "Times New Roman"
    ra_hd.font.size = Pt(16)
    ra_hd.font.color.rgb = RGBColor(16, 75, 42)

    p_ack_body = doc.add_paragraph()
    p_ack_body.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_ack_body.paragraph_format.space_before = Pt(12)
    p_ack_body.paragraph_format.space_after = Pt(18)
    p_ack_body.paragraph_format.line_spacing = 1.3
    ack_text = (
        "Over the last one year, VNRVJIET has helped us transform ourselves from mere amateurs in the field "
        "of Computer Science into skilled engineers capable of handling given situations in real time. We are "
        "highly indebted to the institute for everything that it has given us. We would like to express our "
        "gratitude towards the principal of our institute, Dr. B. Chennakesava Rao and the Head of the Department, "
        "Computer Science & Engineering (AI & ML) & IoT and R&AI, Dr. Y. Sagar, for their kind co-operation and "
        "encouragement which helped us complete the project in the stipulated time. Although we have spent a lot of "
        "time and put in a lot of effort into this project, it would not have been possible without the motivating "
        "support and help of our course coordinator of Object Oriented Programming Through Java, Assistant Professor, "
        "Ms. K. Anitha CSE - (AI & ML) & IoT and R&AI. We thank her for the guidance, constant supervision and for "
        "providing necessary information to complete this project. Our thanks and appreciations also go to all the "
        "faculty members, staff members of VNRVJIET, and all our friends who have helped us put this project together."
    )
    r_ab = p_ack_body.add_run(ack_text)
    r_ab.font.name = "Times New Roman"
    r_ab.font.size = Pt(12)

    p_aspc = doc.add_paragraph()
    p_aspc.paragraph_format.space_before = Pt(120)
    p_aspc.paragraph_format.space_after = Pt(0)

    # Student Names in Acknowledgement
    p_ack_names = doc.add_paragraph()
    p_ack_names.paragraph_format.space_before = Pt(10)
    p_ack_names.paragraph_format.line_spacing = 1.4
    r_an = p_ack_names.add_run(
        "PERVALA YASHWANTH\t\t\t\t(26075A6610)\n"
        "YEJJU SATHYASAI\t\t\t\t(26075A6613)\n"
        "SHAIK ABDUL RASHEED\t\t\t\t(26075A6612)"
    )
    r_an.font.name = "Times New Roman"
    r_an.font.size = Pt(11.5)
    r_an.bold = True

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 5: ABSTRACT
    # ----------------------------------------------------
    p_abs_hd = doc.add_paragraph()
    p_abs_hd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_abs_hd.paragraph_format.space_before = Pt(20)
    p_abs_hd.paragraph_format.space_after = Pt(20)
    rab_hd = p_abs_hd.add_run("ABSTRACT")
    rab_hd.bold = True
    rab_hd.font.name = "Times New Roman"
    rab_hd.font.size = Pt(16)
    rab_hd.font.color.rgb = RGBColor(11, 37, 69)

    p_abs1 = doc.add_paragraph()
    p_abs1.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs1.paragraph_format.space_before = Pt(10)
    p_abs1.paragraph_format.space_after = Pt(10)
    p_abs1.paragraph_format.line_spacing = 1.25
    abs_text1 = (
        "YieldGrid — Application for Farm-to-Retail Inventory is a comprehensive desktop software system "
        "designed to address structural inefficiencies, financial opacity, and supply chain delays inherent in "
        "traditional agricultural trading networks. In the existing multi-tier mandi framework, smallholder farmers "
        "are subjected to unpredictable intermediary commissions, lack direct market visibility, and experience "
        "frequent post-harvest inventory spoilage due to mismatched consumer demand. Retail consumers and urban buyers, "
        "conversely, encounter inflated produce prices and prolonged transit intervals that compromise nutritional freshness. "
        "YieldGrid resolves these systemic challenges by establishing a direct, transparent digital bridge connecting agricultural "
        "producers directly with retail consumers through an interactive, multi-role inventory and order management platform."
    )
    r_abs1 = p_abs1.add_run(abs_text1)
    r_abs1.font.name = "Times New Roman"
    r_abs1.font.size = Pt(12)

    p_abs2 = doc.add_paragraph()
    p_abs2.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_abs2.paragraph_format.space_before = Pt(0)
    p_abs2.paragraph_format.space_after = Pt(14)
    p_abs2.paragraph_format.line_spacing = 1.25
    abs_text2 = (
        "The application is engineered strictly in Java following a modular three-tier architecture encompassing "
        "the Presentation Layer (Java Swing with Nimbus GUI styling), Business Service Layer (role-based business rules, "
        "session authorization, validation), and Data Access Layer (JDBC connected to a relational MySQL database). "
        "YieldGrid provides dedicated, secure operational environments for three distinct stakeholders: Farmers, who list "
        "produce, modify stock units, manage incoming orders, track live revenues, and export audit files; Customers, who "
        "browse verified regional catalogs, search produce in real time, manage shopping carts, execute multi-item purchases, "
        "and track order statuses; and Platform Administrators, who supervise user accounts, moderate listings, and monitor "
        "platform analytics. The software implements essential core and advanced Java concepts including object-oriented encapsulation, "
        "inheritance hierarchies, polymorphic role dispatch, interfaces, Java Collections (ArrayList, HashSet, TreeSet, LinkedHashMap), "
        "custom exception handling, secure cryptographic password hashing with salted PBKDF2 (HMAC-SHA256) and transparent legacy SHA-256 "
        "migration, robust java.io CSV export with formula injection mitigation, and a standalone multithreading demonstration implementing "
        "a monitor-synchronized bounded buffer producer-consumer model with wait() and notifyAll(). Rigorous database transactions "
        "enforce strict ACID semantics, guaranteeing that multi-item order placement and stock unit decrements succeed atomically or "
        "roll back completely upon inventory contention."
    )
    r_abs2 = p_abs2.add_run(abs_text2)
    r_abs2.font.name = "Times New Roman"
    r_abs2.font.size = Pt(12)

    p_kw = doc.add_paragraph()
    p_kw.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_kw.paragraph_format.space_before = Pt(14)
    p_kw.paragraph_format.space_after = Pt(0)
    r_kw_pre = p_kw.add_run("Keywords: ")
    r_kw_pre.bold = True
    r_kw_pre.font.name = "Times New Roman"
    r_kw_pre.font.size = Pt(11.5)
    r_kw = p_kw.add_run("Farm-to-Retail Supply Chain, Java Swing, JDBC, MySQL, ACID Transactions, PBKDF2 Cryptography, Multithreading, Object-Oriented Programming")
    r_kw.font.name = "Times New Roman"
    r_kw.font.size = Pt(11.5)

    doc.add_page_break()

    # ----------------------------------------------------
    # PAGE 6: TABLE OF CONTENTS
    # ----------------------------------------------------
    p_toc_hd = doc.add_paragraph()
    p_toc_hd.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_toc_hd.paragraph_format.space_before = Pt(20)
    p_toc_hd.paragraph_format.space_after = Pt(24)
    rtoc_hd = p_toc_hd.add_run("TABLE OF CONTENTS")
    rtoc_hd.bold = True
    rtoc_hd.font.name = "Times New Roman"
    rtoc_hd.font.size = Pt(16)
    rtoc_hd.font.color.rgb = RGBColor(11, 37, 69)

    # TOC Table formatted cleanly like reference
    t_toc = doc.add_table(rows=10, cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_items = [
        ("1. Problem Statement", "1"),
        ("2. Literature Survey / Existing System", "3"),
        ("3. Objectives", "5"),
        ("4. System Architecture / Workflow", "6"),
        ("5. Proposed Solution", "8"),
        ("6. System Design", "9"),
        ("7. Implementation", "17"),
        ("8. Testing and Debugging", "32"),
        ("9. Analysis of Results", "35"),
        ("References", "36")
    ]
    for idx, (title, page) in enumerate(toc_items):
        c_title = t_toc.cell(idx, 0)
        c_page = t_toc.cell(idx, 1)
        c_title.width = Inches(5.4)
        c_page.width = Inches(1.0)
        set_cell_margins(c_title, 40, 40, 80, 80)
        set_cell_margins(c_page, 40, 40, 80, 80)

        pt = c_title.paragraphs[0]
        pt.alignment = WD_ALIGN_PARAGRAPH.LEFT
        rt = pt.add_run(title)
        rt.font.name = "Times New Roman"
        rt.font.size = Pt(11.5)
        rt.bold = True if idx in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9) else False

        pp = c_page.paragraphs[0]
        pp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        rp = pp.add_run(page)
        rp.font.name = "Times New Roman"
        rp.font.size = Pt(11.5)
        rp.bold = True if idx in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9) else False

    print("Front matter generated successfully (Pages 1 to 6).")
