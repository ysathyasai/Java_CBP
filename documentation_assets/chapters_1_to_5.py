# -*- coding: utf-8 -*-
"""
Chapters 1 to 5 Builder for YieldGrid Academic Project Report
Contains Problem Statement, Literature Survey, Objectives, System Architecture/Workflow, Proposed Solution
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from documentation_assets.report_parts import (
    set_cell_margins, set_cell_shading, set_cell_border,
    add_heading_1, add_heading_2, add_heading_3,
    add_body_p, add_bullet_p, add_figure, add_caption
)

def build_chapters_1_to_5(doc):
    # ----------------------------------------------------
    # CHAPTER 1: PROBLEM STATEMENT
    # ----------------------------------------------------
    add_heading_1(doc, "CHAPTER 1\nPROBLEM STATEMENT")

    add_heading_2(doc, "1.1 Context and Background")
    add_body_p(
        doc,
        "Agriculture forms the foundational economic backbone of India, providing livelihoods for over 50 percent "
        "of the national workforce and contributing substantially to food security and industrial raw materials. "
        "Despite rapid technological advancements across manufacturing, finance, and consumer commerce, the agricultural "
        "distribution ecosystem continues to be governed by antiquated physical market systems characterized by extensive "
        "intermediation, information asymmetry, and manual operational workflows. In traditional mandi markets regulated "
        "under Agricultural Produce Market Committee (APMC) acts, fresh produce moves through an average of four to six "
        "intermediaries—including local village aggregators, commission agents (arhtiyas), primary wholesalers, secondary "
        "wholesalers, and retail street vendors—before ultimately reaching urban household consumers."
    )
    add_body_p(
        doc,
        "Each intermediary layer introduces compounded transaction commissions, handling markups, loading-unloading fees, "
        "and unavoidable transport delays. Research conducted across national agricultural corridors reveals that primary "
        "producers frequently capture as little as 25 to 35 percent of the terminal consumer rupee for perishable crops "
        "such as tomatoes, onions, leafy vegetables, and seasonal fruits. Conversely, retail consumers pay substantially "
        "elevated prices for produce whose organoleptic quality, nutritional density, and freshness have deteriorated "
        "significantly during prolonged physical transit through unorganized wholesale channels."
    )

    add_heading_2(doc, "1.2 Structural Inefficiencies in the Traditional Farm-to-Retail Chain")
    add_body_p(
        doc,
        "The traditional agricultural value chain suffers from several interrelated systemic bottlenecks that limit productivity "
        "and impose severe financial strain on primary agricultural stakeholders:",
        bold_prefix="Systemic Chain Vulnerabilities: "
    )
    add_bullet_p(
        doc,
        "Smallholder farmers arrive at regional market yards without verifiable advance knowledge of prevailing daily rates, "
        "leaving them entirely vulnerable to localized cartelization, discretionary discounting, and distress selling.",
        bold_prefix="Price Opacity and Information Asymmetry: "
    )
    add_bullet_p(
        doc,
        "Physical agricultural handling lacks real-time digital inventory synchronization. Without automated stock tracking, "
        "farmers frequently oversell or experience post-harvest storage losses exceeding 20 to 30 percent for perishable items.",
        bold_prefix="Inventory Spoilage and Stock Mismanagement: "
    )
    add_bullet_p(
        doc,
        "Traditional wholesale transactions rely heavily on paper registers, informal credit slips, and unrecorded cash exchanges, "
        "depriving farmers of verifiable revenue documentation necessary for institutional credit access.",
        bold_prefix="Absence of Auditable Transaction Trails: "
    )
    add_bullet_p(
        doc,
        "Urban retailers and retail consumers possess zero traceability regarding produce harvest dates, cultivation origins, "
        "or farming practices, leading to inconsistent quality and uncertain supply continuity.",
        bold_prefix="Lack of Provenance and Quality Assurance: "
    )

    add_heading_2(doc, "1.3 Target Users and Stakeholder Personas")
    add_body_p(
        doc,
        "To effectively replace intermediary dependency with software-driven coordination, YieldGrid targets three primary "
        "user classes within a cohesive multi-tenant desktop architecture:"
    )
    add_bullet_p(
        doc,
        "Agricultural producers seeking direct digital market access, transparent unit pricing control, instant stock listing, "
        "real-time order notification, and clear visibility into cumulative financial earnings.",
        bold_prefix="1. Farmers (Agricultural Producers): "
    )
    add_bullet_p(
        doc,
        "Urban consumers, retail cooperative buyers, and culinary businesses seeking farm-fresh produce, verifiable provenance, "
        "transparent weight-based catalog pricing, shopping cart convenience, and live order tracking.",
        bold_prefix="2. Customers (Retail Consumers & Buyers): "
    )
    add_bullet_p(
        doc,
        "System supervisors responsible for platform governance, user credential verification, catalog moderation, system health "
        "monitoring, audit record inspection, and operational conflict resolution.",
        bold_prefix="3. Platform Administrators: "
    )

    add_heading_2(doc, "1.4 Problem Statement Formulation")
    add_body_p(
        doc,
        "To design and engineer a robust, standalone, multi-role desktop application in Java—entitled YieldGrid—that enables "
        "smallholder farmers to publish real-time produce inventories, empowers retail consumers to discover farm-fresh crops "
        "and execute atomic, multi-item purchasing transactions, and provides platform administrators with governance and audit "
        "capabilities. The system must eliminate intermediary rent-seeking by enabling direct producer-to-consumer order fulfillment, "
        "guarantee inventory consistency under concurrent operations through database-enforced ACID transactions, safeguard user "
        "credentials with industry-standard salted PBKDF2 cryptography, and demonstrate rigorous mastery of core and advanced "
        "object-oriented Java software engineering principles.",
        bold_prefix="FORMAL PROBLEM STATEMENT: "
    )

    add_heading_2(doc, "1.5 Scope and Project Boundaries")
    add_body_p(
        doc,
        "YieldGrid is developed as an academic Course-Based Project (CBP) for the B.Tech curriculum in Computer Science and Engineering. "
        "The project scope encompasses a complete, production-quality desktop application featuring a Java Swing graphical user interface, "
        "JDBC database connectivity, MySQL relational persistence, role-based authentication, interactive shopping cart management, "
        "atomic multi-item order placement, farmer revenue calculations, CSV data export, and an academic bounded-buffer multithreading "
        "demonstration. The operational boundaries deliberately focus on standalone enterprise-style software execution; external third-party "
        "payment gateways, GPS-based telematics tracking, and cloud messaging services are identified as future enhancements beyond the current "
        "curricular syllabus."
    )

    doc.add_page_break()

    # ----------------------------------------------------
    # CHAPTER 2: LITERATURE SURVEY / EXISTING SYSTEM
    # ----------------------------------------------------
    add_heading_1(doc, "CHAPTER 2\nLITERATURE SURVEY / EXISTING SYSTEM")

    add_heading_2(doc, "2.1 Survey of Existing Agricultural Supply Systems")
    add_body_p(
        doc,
        "A comprehensive investigation of existing agricultural trading, distribution, and inventory management systems "
        "was conducted to identify their structural features, technological foundations, and practical limitations. "
        "Contemporary solutions in this domain fall into three broad categories: Physical APMC Mandis, Large Corporate Aggregation "
        "Platforms, and Emerging Direct-to-Consumer Marketplaces."
    )
    add_body_p(
        doc,
        "Physical Mandis represent the conventional trading mechanism across rural India. While they concentrate physical produce "
        "in centralized trading yards, they exhibit severe operational deficiencies including monopolistic bidding rings, non-transparent "
        "deductions, delayed farmer disbursements, and significant post-harvest crop degradation resulting from repeated loading, unloading, "
        "and unrefrigerated storage intervals."
    )
    add_body_p(
        doc,
        "Corporate Aggregator Platforms (e.g., Ninjacart, DeHaat, BigBasket) leverage technology to streamline wholesale procurement. "
        "However, these platforms primarily function as closed, centralized distribution monopolies. They negotiate bulk farmgate "
        "contracts on unilateral pricing terms, require extensive corporate collection center infrastructure, and exclude smallholder "
        "farmers who lack commercial transportation or harvest volumes exceeding minimum fulfillment thresholds."
    )
    add_body_p(
        doc,
        "Consumer-facing E-Grocery Apps (e.g., Blinkit, Zepto, Swiggy Instamart) prioritize rapid urban delivery from urban dark stores. "
        "These applications are completely disconnected from farmgate economics, operating with heavy retail markups, opaque sourcing, "
        "and zero direct communication or revenue visibility between consumers and agricultural producers."
    )

    add_heading_2(doc, "2.2 Comparative Study Matrix")
    add_body_p(
        doc,
        "Table 2.1 provides an in-depth comparative analysis evaluating existing agricultural trading paradigms against "
        "the architectural parameters of YieldGrid."
    )

    # Table 2.1
    t_comp = doc.add_table(rows=6, cols=5)
    t_comp.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Feature / Dimension", "Physical Mandis", "Corporate Aggregators", "Quick-Commerce Apps", "YieldGrid (Proposed)"]
    for j, h in enumerate(headers):
        c = t_comp.cell(0, j)
        set_cell_shading(c, "1E3A8A")
        set_cell_margins(c, 80, 80, 100, 100)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(h)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    matrix_data = [
        ("Intermediary Layers", "4 to 6 Intermediary Tiers", "Centralized Corporate Tier", "Wholesale & Dark Store Tiers", "Zero Intermediaries (Direct)"),
        ("Farmer Price Control", "None (Dictated by Brokers)", "Marginal (Corporate Tariffs)", "None (Wholesale Sourced)", "Full Control (Farmer Sets Price)"),
        ("Real-Time Inventory", "Manual Physical Registers", "Proprietary Cloud ERP", "Dark Store Warehouse Sync", "Relational Database Tracking"),
        ("Order Atomicity", "Not Applicable (Cash/Credit)", "Corporate Batch ERP", "High-Volume Web Cloud", "ACID JDBC Transactions"),
        ("Accessibility / Cost", "Physical Travel Required", "Requires Bulk Volume", "Urban Consumers Only", "Open Lightweight Desktop Java")
    ]
    for row_idx, data in enumerate(matrix_data, start=1):
        for col_idx, text in enumerate(data):
            c = t_comp.cell(row_idx, col_idx)
            set_cell_shading(c, "F8F9FA" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(c, 60, 60, 80, 80)
            set_cell_border(c, top={'val': 'single', 'sz': 4, 'color': 'E2E8F0'},
                               bottom={'val': 'single', 'sz': 4, 'color': 'E2E8F0'},
                               left={'val': 'single', 'sz': 4, 'color': 'E2E8F0'},
                               right={'val': 'single', 'sz': 4, 'color': 'E2E8F0'})
            p = c.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT if col_idx == 0 else WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9.5)
            if col_idx == 4:
                r.bold = True
                r.font.color.rgb = RGBColor(16, 75, 42)

    add_caption(doc, "Table 2.1: Comparative Feature Analysis of Agricultural Supply and Inventory Systems")

    add_heading_2(doc, "2.3 Identified Engineering and Research Gaps")
    add_body_p(
        doc,
        "The literature survey reveals three critical technological gaps that YieldGrid specifically resolves:"
    )
    add_bullet_p(
        doc,
        "Existing software platforms either target massive industrial agri-businesses or consumer grocery delivery, "
        "leaving individual farmers without an accessible, low-friction tool to manage their own direct inventory and order records.",
        bold_prefix="1. Absence of Decentralized Producer Inventory Tools: "
    )
    add_bullet_p(
        doc,
        "Commercial systems conceal margin distributions, leaving farmers unaware of final retail realization and consumers "
        "unaware of actual producer compensation. YieldGrid establishes 100% price transparency where the listed price represents the exact farmgate price.",
        bold_prefix="2. Lack of Two-Sided Financial Transparency: "
    )
    add_bullet_p(
        doc,
        "Many desktop educational systems rely on simplistic flat-file storage or lack transactional atomicity, leading to race conditions "
        "and negative inventory during concurrent orders. YieldGrid implements strict JDBC transaction rollback to guarantee mathematical consistency.",
        bold_prefix="3. Inadequate Transactional Integrity in Educational Software: "
    )

    doc.add_page_break()

    # ----------------------------------------------------
    # CHAPTER 3: OBJECTIVES
    # ----------------------------------------------------
    add_heading_1(doc, "CHAPTER 3\nOBJECTIVES")

    add_heading_2(doc, "3.1 Primary Technical Objectives")
    add_body_p(
        doc,
        "The primary technical objective of YieldGrid is to engineer a dependable, modular, and secure Java desktop application "
        "that connects agricultural producers directly with retail customers while demonstrating comprehensive mastery of the Object-Oriented "
        "Programming Through Java curriculum."
    )

    add_heading_2(doc, "3.2 Specific Functional Objectives")
    add_bullet_p(
        doc,
        "Provide an interactive Java Swing dashboard for farmers to list produce, update stock units, adjust unit prices, and monitor sales.",
        bold_prefix="Farmer Inventory Management: "
    )
    add_bullet_p(
        doc,
        "Deliver a customer marketplace with real-time produce filtering, keyword search, shopping cart management, and order tracking.",
        bold_prefix="Customer Marketplace & Cart: "
    )
    add_bullet_p(
        doc,
        "Implement administrative oversight enabling user account activation/deactivation, catalog moderation, and system audit logging.",
        bold_prefix="Administrative Governance: "
    )
    add_bullet_p(
        doc,
        "Enforce database-level ACID transactions via JDBC connection boundaries (commit, rollback) to guarantee atomic stock deduction.",
        bold_prefix="ACID Transactional Integrity: "
    )
    add_bullet_p(
        doc,
        "Safeguard user credentials with salted PBKDF2 (HMAC-SHA256, 10,000 iterations) with transparent migration for legacy SHA-256 hashes.",
        bold_prefix="Cryptographic Password Security: "
    )
    add_bullet_p(
        doc,
        "Provide RFC 4180 compliant CSV export using java.io streams with formula injection defense to protect financial records.",
        bold_prefix="Secure CSV Data Export: "
    )

    add_heading_2(doc, "3.3 Syllabus and Pedagogical Alignment Objectives")
    add_bullet_p(
        doc,
        "Unit I: Domain entities (User, Crop, Order), encapsulation, method overloading, and recursive inventory accumulation.",
        bold_prefix="Java Basics & OOP: "
    )
    add_bullet_p(
        doc,
        "Unit II: Abstract User class, polymorphic role specialization (Farmer, Customer, AdminUser), and interface inheritance.",
        bold_prefix="Inheritance & Interfaces: "
    )
    add_bullet_p(
        doc,
        "Unit III: Custom domain exceptions and a bounded-buffer producer-consumer multithreading model with wait() and notifyAll().",
        bold_prefix="Exceptions & Concurrency: "
    )
    add_bullet_p(
        doc,
        "Unit IV: Application of List, ArrayList, HashSet, TreeSet, and LinkedHashMap across domain models and cart calculations.",
        bold_prefix="Collections Framework: "
    )
    add_bullet_p(
        doc,
        "Unit V: Nimbus-themed Swing GUI components (JFrame, JTable, JTabbedPane) and JDBC connectivity with PreparedStatement.",
        bold_prefix="Swing GUI & JDBC: "
    )

    doc.add_page_break()

    # ----------------------------------------------------
    # CHAPTER 4: SYSTEM ARCHITECTURE / WORKFLOW
    # ----------------------------------------------------
    add_heading_1(doc, "CHAPTER 4\nSYSTEM ARCHITECTURE / WORKFLOW")

    add_heading_2(doc, "4.1 High-Level Architectural Overview")
    add_body_p(
        doc,
        "YieldGrid is engineered following a clean, loosely coupled Three-Tier Layered Architecture that guarantees separation "
        "of concerns, maintainability, and modular testability. The application is segregated into four distinct structural layers: "
        "the Presentation Layer, the Service (Business Logic) Layer, the Data Access Object (DAO) Layer, and the Relational Database Layer."
    )
    add_bullet_p(
        doc,
        "Built entirely using Java Swing with the Nimbus Look-and-Feel. Encapsulates all graphical frames, dashboard panels, tables, "
        "dialogs, and asynchronous event listeners. Interacts exclusively with the Service Layer without issuing direct database calls.",
        bold_prefix="1. Presentation Layer (Swing UI): "
    )
    add_bullet_p(
        doc,
        "Coordinates business domain logic, session management, input validation, cryptographic hashing, and transaction workflows. "
        "Enforces business rules such as verifying sufficient crop inventory prior to purchase and preventing unauthorized role actions.",
        bold_prefix="2. Service Layer (Business Logic): "
    )
    add_bullet_p(
        doc,
        "Encapsulates all SQL execution, PreparedStatement lifecycle management, and ResultSet-to-entity mapping. "
        "Isolates JDBC persistence mechanisms from application business logic.",
        bold_prefix="3. Data Access Layer (DAOs): "
    )
    add_bullet_p(
        doc,
        "Relational MySQL engine that persistently maintains users, produce inventories, orders, line items, and audit logs. "
        "Guarantees referential integrity through foreign key constraints and transactional consistency.",
        bold_prefix="4. Persistence Layer (MySQL Database): "
    )

    # Insert Figure 4.1 System Architecture Diagram
    add_figure(doc, "documentation_assets/diagrams/system_architecture.png", "Figure 4.1: YieldGrid Layered System Architecture", width=Inches(6.2))

    add_heading_2(doc, "4.2 Overall Application Execution Workflow")
    add_body_p(
        doc,
        "The runtime lifecycle of YieldGrid initiates at application launch when the Main bootstrap class sets up the global UI theme, "
        "verifies database driver availability, and presents the LoginFrame. Users authenticate using their credentials, triggering "
        "PBKDF2 cryptographic verification in the AuthenticationService. Upon successful verification, the SessionManager instantiates "
        "the active session and dispatches the user to their designated dashboard based on their polymorphic role."
    )

    # Insert Figure 4.2 Overall Workflow Diagram
    add_figure(doc, "documentation_assets/diagrams/overall_application_workflow.png", "Figure 4.2: YieldGrid Application Execution Lifecycle and Authentication Workflow", width=Inches(6.2))

    add_heading_2(doc, "4.3 Architectural Patterns and Design Principles")
    add_body_p(
        doc,
        "The software architecture incorporates established design patterns that promote code reuse and academic clarity:"
    )
    add_bullet_p(
        doc,
        "Abstracts low-level database operations behind clean interface methods (e.g., CropDAO, OrderDAO, UserDAO, AdminDAO), "
        "shielding business components from database syntax details.",
        bold_prefix="Data Access Object (DAO) Pattern: "
    )
    add_bullet_p(
        doc,
        "Ensures unified, thread-safe connection pooling and centralizes credential extraction from external configuration files.",
        bold_prefix="Singleton Connection Manager: "
    )
    add_bullet_p(
        doc,
        "Separates user interface rendering from domain state, ensuring that data modifications automatically reflect across "
        "active Swing tables through structured model events.",
        bold_prefix="Model-View Separation: "
    )

    doc.add_page_break()

    # ----------------------------------------------------
    # CHAPTER 5: PROPOSED SOLUTION
    # ----------------------------------------------------
    add_heading_1(doc, "CHAPTER 5\nPROPOSED SOLUTION")

    add_heading_2(doc, "5.1 System Overview and Key Value Propositions")
    add_body_p(
        doc,
        "YieldGrid delivers a comprehensive, software-driven alternative to intermediary-heavy agricultural supply chains. "
        "By replacing multi-tiered middlemen with a direct digital clearinghouse, the platform ensures that smallholder farmers "
        "retain direct control over crop pricing, receive 100 percent of customer payments, and gain clear visibility into real-time demand. "
        "Simultaneously, retail consumers gain access to fresher produce at fair prices, complete with transparent farmer origin details."
    )

    add_heading_2(doc, "5.2 Direct Farm-to-Retail Model")
    add_body_p(
        doc,
        "Under the YieldGrid paradigm, farmers list their harvested or growing crops directly onto the central digital catalog, "
        "specifying crop variety, detailed description, available quantity in kilograms or units, and their desired farmgate unit price. "
        "Customers browsing the catalog view real-time available stock and producer contact information. When an order is placed, "
        "an atomic transaction immediately reserves the required inventory units, generates an order record, and notifies the farmer's "
        "dashboard without requiring any broker intervention."
    )

    add_heading_2(doc, "5.3 Automated Inventory Management and Stock Consistency")
    add_body_p(
        doc,
        "To eliminate the risks of overselling and inventory race conditions, YieldGrid implements automated stock validation at two "
        "independent stages of the purchase workflow: first in-memory during shopping cart assembly, and second within the database "
        "using conditional SQL updates during transaction execution. If a customer attempts to purchase more units than currently available, "
        "the application raises an InsufficientStockException and halts execution before any invalid state changes occur."
    )

    add_heading_2(doc, "5.4 Cryptographic Security and Credential Safeguards")
    add_body_p(
        doc,
        "Security is central to the YieldGrid architecture. Unlike basic educational systems that store plaintext credentials or use "
        "obsolete unsalted MD5/SHA-1 algorithms, YieldGrid implements Password-Based Key Derivation Function 2 (PBKDF2) utilizing "
        "HMAC-SHA256 with 10,000 hash iterations and unique 16-byte cryptographically secure random salts. Furthermore, the system includes "
        "an intelligent migration mechanism that transparently re-hashes legacy SHA-256 credentials to PBKDF2 upon the user's next successful login, "
        "ensuring backward compatibility without compromising cryptographic strength."
    )

    add_heading_2(doc, "5.5 Relational Persistence and Transactional Atomicity")
    add_body_p(
        doc,
        "The underlying database schema is organized in Third Normal Form (3NF) across relational MySQL tables linked by cascading foreign "
        "keys. All critical order placement operations are executed within explicit JDBC transaction boundaries. In the event of network disruption, "
        "stock exhaustion, or database error during line item processing, the transaction immediately rolls back all partial modifications, "
        "guaranteeing total ledger consistency and zero orphaned records."
    )

    doc.add_page_break()
    print("Chapters 1 to 5 generated successfully.")
