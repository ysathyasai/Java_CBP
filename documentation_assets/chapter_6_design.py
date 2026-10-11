# -*- coding: utf-8 -*-
"""
Chapter 6 Builder for YieldGrid Academic Project Report
Contains System Design: Modules, Role Workflows, Transactions, Diagrams, ERD, Schema Tables, and Algorithms
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

def build_chapter_6(doc):
    # ----------------------------------------------------
    # CHAPTER 6: SYSTEM DESIGN
    # ----------------------------------------------------
    add_heading_1(doc, "CHAPTER 6\nSYSTEM DESIGN")

    add_heading_2(doc, "6.1 Modular System Decomposition and Responsibilities")
    add_body_p(
        doc,
        "The architecture of YieldGrid is partitioned into cohesive, loosely coupled functional modules, each addressing "
        "a distinct operational domain of the farm-to-retail ecosystem. This modular separation simplifies unit testing, "
        "improves fault isolation, and strictly enforces the Single Responsibility Principle across the application."
    )
    add_bullet_p(
        doc,
        "Handles user authentication, credential validation, session initialization, and role-based interface dispatching. "
        "Maintains active session state and disallows unauthorized cross-tenant operations.",
        bold_prefix="1. Authentication and Access Control Module: "
    )
    add_bullet_p(
        doc,
        "Empowers farmers to register new crop varieties, update unit pricing, replenish stock quantities, and remove obsolete "
        "listings. Enforces data validation to ensure prices and quantities remain strictly positive.",
        bold_prefix="2. Crop Inventory Management Module: "
    )
    add_bullet_p(
        doc,
        "Enables retail customers to discover produce through case-insensitive substring searching, view producer origins, "
        "add items to an in-memory shopping cart, modify purchase quantities, and calculate dynamic subtotals.",
        bold_prefix="3. Customer Marketplace and Cart Module: "
    )
    add_bullet_p(
        doc,
        "Executes multi-item order checkouts within atomic JDBC transaction boundaries, decrements physical inventory stock safely, "
        "generates unique order tracking numbers, and records individual line items.",
        bold_prefix="4. Order Processing and Transaction Module: "
    )
    add_bullet_p(
        doc,
        "Aggregates completed sales data for farmers, calculates cumulative revenues, evaluates inventory turnover, and provides "
        "structured RFC 4180 CSV export with formula injection sanitization.",
        bold_prefix="5. Revenue Analytics and Export Module: "
    )
    add_bullet_p(
        doc,
        "Provides system administrators with comprehensive oversight, including user account activation/deactivation, platform-wide "
        "metric card visualizations, produce listing moderation, and audit trail inspection.",
        bold_prefix="6. Platform Administration and Auditing Module: "
    )

    add_heading_2(doc, "6.2 Role-Based Workflows")
    add_body_p(
        doc,
        "YieldGrid defines distinct, isolated operational workflows tailored to each authenticated stakeholder role. "
        "The system enforces strict role authorization at both the presentation layer (by rendering role-specific dashboard views) "
        "and the service layer (by verifying user permissions before executing business operations)."
    )

    add_heading_3(doc, "6.2.1 Farmer Workflow")
    add_body_p(
        doc,
        "Upon successful authentication, a farmer enters the FarmerDashboard, which presents three primary operational panels: "
        "Crop Management, Incoming Orders, and Revenue Analytics. The farmer can create new crop listings by specifying crop name, "
        "category, quantity, and price. When orders are received from customers, the farmer reviews the requested quantities and "
        "transitions the order status from PENDING to CONFIRMED, and subsequently to SHIPPED or DELIVERED. The Revenue Analytics panel "
        "computes real-time gross earnings and permits one-click CSV financial export."
    )
    add_figure(doc, "documentation_assets/diagrams/farmer_workflow.png", "Figure 6.1: Farmer Operational Workflow Diagram", width=Inches(5.2))

    add_heading_3(doc, "6.2.2 Customer Workflow")
    add_body_p(
        doc,
        "Customers access the CustomerDashboard featuring the Marketplace Catalog, Shopping Cart, and My Orders panels. "
        "Customers browse available produce with live filtering across names, descriptions, and farmer details. Adding produce "
        "to the cart checks available stock in real time. During checkout, the customer confirms the order, triggering an atomic "
        "database transaction that generates order records and decrements stock units. Customers can monitor live fulfillment "
        "progress in the My Orders panel."
    )
    add_figure(doc, "documentation_assets/diagrams/customer_workflow.png", "Figure 6.2: Customer Marketplace and Checkout Workflow Diagram", width=Inches(5.2))

    add_heading_3(doc, "6.2.3 Platform Administrator Workflow")
    add_body_p(
        doc,
        "The AdminDashboard provides centralized governance for platform administrators. Administrators monitor real-time system "
        "metrics (total active users, listed crops, total orders placed, and gross marketplace sales volume). The user management panel "
        "allows administrators to review registered accounts, activate or deactivate users, and export user lists. Safety constraints "
        "prevent administrators from deactivating their own active admin account. Additionally, administrators can moderate inappropriate "
        "crop listings and inspect audit logs."
    )
    add_figure(doc, "documentation_assets/diagrams/admin_workflow.png", "Figure 6.3: Administrator Governance and Auditing Workflow Diagram", width=Inches(5.2))

    add_heading_2(doc, "6.3 Transactional Workflows: Order Placement & Inventory Consistency")
    add_body_p(
        doc,
        "Maintaining absolute inventory consistency across concurrent user sessions is critical in agricultural commerce. "
        "YieldGrid guarantees inventory integrity through an atomic, multi-stage checkout workflow managed by OrderDAO and OrderService."
    )
    add_body_p(
        doc,
        "When the customer confirms checkout, the database connection disables automatic commits (setAutoCommit(false)). "
        "The system first inserts the master order header and retrieves the generated order ID. Next, it iterates through each line item "
        "in the cart, inserting the order_item record and executing an atomic conditional stock deduction: "
        "UPDATE crops SET quantity = quantity - ? WHERE crop_id = ? AND quantity >= ?. If any line item fails due to stock exhaustion, "
        "the entire transaction is rolled back immediately, restoring all previous inventory states and preventing orphaned order entries."
    )
    add_figure(doc, "documentation_assets/diagrams/order_inventory_transaction_workflow.png", "Figure 6.4: Order Placement and Inventory Transaction Workflow", width=Inches(5.2))

    add_heading_2(doc, "6.4 Component & Class Hierarchy Design")
    add_body_p(
        doc,
        "YieldGrid strictly applies object-oriented design principles to organize domain entities, interfaces, and services. "
        "Figure 6.5 illustrates the complete component and class hierarchy, highlighting abstract inheritance, interface implementation, "
        "and service layer interactions."
    )
    add_figure(doc, "documentation_assets/diagrams/component_class_diagram.png", "Figure 6.5: YieldGrid Component and Class Hierarchy Diagram", width=Inches(5.3))

    add_heading_3(doc, "6.4.1 Object-Oriented Domain Entity Hierarchy")
    add_body_p(
        doc,
        "The domain model centers around an abstract base class User located in package yieldgrid.model. The User class defines "
        "common encapsulated attributes (userId, name, username, passwordHash, role, contactInfo, isActive) and declares the abstract method "
        "getRoleDescription(). Concrete subclasses Farmer, Customer, and AdminUser extend User, providing polymorphic implementations "
        "of role descriptions and specialized behavior. Entities override equals() and hashCode() based on persistent database identity, "
        "ensuring predictable behavior within Java Collections such as HashSet and HashMap."
    )

    add_heading_3(doc, "6.4.2 Interface Segregation and Extension")
    add_body_p(
        doc,
        "To decouple dashboard views from concrete implementations, YieldGrid defines behavioral contracts using Java interfaces. "
        "Interface DashboardActions specifies fundamental lifecycle contracts (refreshDashboard(), logout(), displayErrorMessage()). "
        "The specialized interface AdminActions extends DashboardActions, declaring administrative contracts (loadSystemMetrics(), "
        "toggleUserStatus(), exportAuditLogs()). This demonstrates clean interface inheritance and adhering to the Interface Segregation Principle."
    )

    add_heading_2(doc, "6.5 Database Design & Schema Architecture")
    add_body_p(
        doc,
        "The database schema is normalized to Third Normal Form (3NF) to eliminate redundant storage, update anomalies, and data inconsistency. "
        "Figure 6.6 shows the Entity-Relationship (ER) Diagram representing all entities, primary keys, foreign keys, and cardinalities."
    )
    add_figure(doc, "documentation_assets/diagrams/entity_relationship_diagram.png", "Figure 6.6: YieldGrid Relational Entity-Relationship (ER) Diagram", width=Inches(5.3))

    add_heading_3(doc, "6.5.1 Detailed Database Schema Tables")
    add_body_p(doc, "The physical schema comprises five relational tables as detailed below:")

    # Helper function for schema tables
    def render_schema_table(caption_text, col_headers, rows_data):
        tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(col_headers))
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        for c_idx, h_text in enumerate(col_headers):
            cell = tbl.cell(0, c_idx)
            set_cell_shading(cell, "1E3A8A")
            set_cell_margins(cell, 20, 20, 40, 40)
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            r = p.add_run(h_text)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9)
            r.bold = True
            r.font.color.rgb = RGBColor(255, 255, 255)
        for r_idx, row in enumerate(rows_data, start=1):
            for c_idx, val in enumerate(row):
                cell = tbl.cell(r_idx, c_idx)
                set_cell_shading(cell, "F8F9FA" if r_idx % 2 == 1 else "FFFFFF")
                set_cell_margins(cell, 15, 15, 35, 35)
                set_cell_border(cell, top={'val': 'single', 'sz': 4, 'color': 'E2E8F0'},
                                     bottom={'val': 'single', 'sz': 4, 'color': 'E2E8F0'},
                                     left={'val': 'single', 'sz': 4, 'color': 'E2E8F0'},
                                     right={'val': 'single', 'sz': 4, 'color': 'E2E8F0'})
                p = cell.paragraphs[0]
                p.paragraph_format.space_before = Pt(0)
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.0
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx in (0, 3) else WD_ALIGN_PARAGRAPH.CENTER
                r = p.add_run(val)
                r.font.name = "Times New Roman"
                r.font.size = Pt(8)
                if c_idx == 2 and "PRIMARY" in val:
                    r.bold = True
                    r.font.color.rgb = RGBColor(16, 75, 42)
        add_caption(doc, caption_text)

    # Table 6.1 users
    users_data = [
        ("user_id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "Unique identifier for each user account"),
        ("name", "VARCHAR(100)", "NOT NULL", "Full legal name or farm establishment name"),
        ("username", "VARCHAR(50)", "NOT NULL, UNIQUE", "Unique login credential identifier"),
        ("password", "VARCHAR(255)", "NOT NULL", "Salted PBKDF2 or legacy SHA-256 password hash"),
        ("role", "VARCHAR(20)", "NOT NULL", "User access role: FARMER, CUSTOMER, or ADMIN"),
        ("contact_info", "VARCHAR(150)", "NULLABLE", "Physical address, city, and telephone number"),
        ("is_active", "BOOLEAN", "DEFAULT TRUE", "Account authorization status flag"),
        ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Record creation timestamp")
    ]
    render_schema_table("Table 6.1: Relational Schema for 'users' Table", ["Column Name", "Data Type", "Constraints", "Description"], users_data)

    # Table 6.2 crops
    crops_data = [
        ("crop_id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "Unique crop listing identifier"),
        ("farmer_id", "INT", "FOREIGN KEY (users.user_id)", "ID of farmer who listed this crop (CASCADE)"),
        ("crop_name", "VARCHAR(100)", "NOT NULL", "Botanical or common market name of produce"),
        ("description", "TEXT", "NULLABLE", "Detailed crop description, grade, quality"),
        ("quantity", "INT", "NOT NULL, CHECK (>=0)", "Current available physical stock units (kg/bunches)"),
        ("price", "DECIMAL(10,2)", "NOT NULL, CHECK (>0)", "Unit price in INR set directly by farmer"),
        ("available", "BOOLEAN", "DEFAULT TRUE", "Catalog visibility and availability flag"),
        ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Produce listing registration timestamp")
    ]
    render_schema_table("Table 6.2: Relational Schema for 'crops' Table", ["Column Name", "Data Type", "Constraints", "Description"], crops_data)

    # Table 6.3 orders
    orders_data = [
        ("order_id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "Unique purchase order identifier"),
        ("customer_id", "INT", "FOREIGN KEY (users.user_id)", "ID of purchasing customer account"),
        ("farmer_id", "INT", "FOREIGN KEY (users.user_id)", "ID of fulfilling farmer account"),
        ("order_date", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Date and time of order checkout"),
        ("total_amount", "DECIMAL(10,2)", "NOT NULL", "Gross financial total in INR for this order"),
        ("status", "VARCHAR(20)", "DEFAULT 'PENDING'", "Lifecycle state: PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED")
    ]
    render_schema_table("Table 6.3: Relational Schema for 'orders' Table", ["Column Name", "Data Type", "Constraints", "Description"], orders_data)

    # Table 6.4 order_items
    items_data = [
        ("order_item_id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "Unique line item identifier"),
        ("order_id", "INT", "FOREIGN KEY (orders.order_id)", "Parent purchase order reference (CASCADE)"),
        ("crop_id", "INT", "FOREIGN KEY (crops.crop_id)", "Reference to ordered crop variety (CASCADE)"),
        ("quantity", "INT", "NOT NULL, CHECK (>0)", "Purchased quantity in kilograms or units"),
        ("unit_price", "DECIMAL(10,2)", "NOT NULL", "Price per unit captured at instant of purchase"),
        ("subtotal", "DECIMAL(10,2)", "NOT NULL", "Computed line total (quantity * unit_price)")
    ]
    render_schema_table("Table 6.4: Relational Schema for 'order_items' Table", ["Column Name", "Data Type", "Constraints", "Description"], items_data)

    # Table 6.5 activity_logs
    logs_data = [
        ("log_id", "INT", "PRIMARY KEY, AUTO_INCREMENT", "Unique administrative audit entry identifier"),
        ("user_id", "INT", "FOREIGN KEY (users.user_id)", "Actor who performed the logged action"),
        ("action", "VARCHAR(100)", "NOT NULL", "Descriptor: USER_DEACTIVATE, CROP_ADD, ORDER_PLACE, etc."),
        ("details", "TEXT", "NULLABLE", "Contextual metadata and action details"),
        ("timestamp", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "Exact timestamp of audited system event")
    ]
    render_schema_table("Table 6.5: Relational Schema for 'activity_logs' Table", ["Column Name", "Data Type", "Constraints", "Description"], logs_data)

    add_heading_2(doc, "6.6 Core Algorithmic Designs")
    add_body_p(
        doc,
        "YieldGrid implements robust algorithms across transactional checkout, cryptographic security, and inventory analytics. "
        "The following pseudo-algorithms describe these core mechanisms:"
    )

    add_heading_3(doc, "Algorithm 6.1: Atomic Multi-Item Order Checkout with Inventory Validation")
    add_body_p(
        doc,
        "Input: Customer ID (cid), Active Cart Items List (cart)\n"
        "Output: Boolean (True if transaction committed successfully, False otherwise)\n"
        "1. Obtain persistent database connection 'conn'.\n"
        "2. If cart is null or cart.isEmpty(), throw ValidationException('Cart is empty').\n"
        "3. In-memory pre-validation: For each item in cart, verify item.quantity > 0 and item.quantity <= item.crop.quantity.\n"
        "4. Group cart items by distinct farmerId to generate separate farmer orders.\n"
        "5. For each farmer group:\n"
        "     a. conn.setAutoCommit(false);\n"
        "     b. Execute INSERT INTO orders (customer_id, farmer_id, total_amount, status) VALUES (?, ?, ?, 'PENDING');\n"
        "     c. Retrieve generated orderId via pstmt.getGeneratedKeys();\n"
        "     d. For each item in farmer group:\n"
        "          i. Execute INSERT INTO order_items (order_id, crop_id, quantity, unit_price, subtotal) VALUES (?, ?, ?, ?, ?);\n"
        "          ii. Execute atomic conditional decrement: UPDATE crops SET quantity = quantity - ? WHERE crop_id = ? AND quantity >= ?;\n"
        "          iii. If affected rows == 0 (stock exhausted by concurrent order), conn.rollback() and throw InsufficientStockException;\n"
        "     e. conn.commit();\n"
        "6. conn.setAutoCommit(true);\n"
        "7. Clear active customer cart and return True."
    )

    add_heading_3(doc, "Algorithm 6.2: PBKDF2 Password Verification with Transparent Migration")
    add_body_p(
        doc,
        "Input: Plaintext Candidate Password (p), Stored Password Hash (stored)\n"
        "Output: Boolean (True if valid, False otherwise)\n"
        "1. If p is null or stored is null, return False.\n"
        "2. If stored starts with 'pbkdf2$':\n"
        "     a. Parse tokens: iterations = parts[1], salt = Base64Decode(parts[2]), expectedHash = Base64Decode(parts[3]).\n"
        "     b. candidateHash = PBKDF2WithHmacSHA256(p, salt, iterations, 256 bits).\n"
        "     c. Return MessageDigest.isEqual(candidateHash, expectedHash) [constant-time comparison].\n"
        "3. Else if stored starts with 'sha256$':\n"
        "     a. expectedHash = stored.substring(7).\n"
        "     b. candidateHash = HexEncode(SHA-256(UTF8(p))).\n"
        "     c. If candidateHash equals expectedHash:\n"
        "          i. Trigger background migration: newHash = hashPassword(p) [generates salted PBKDF2].\n"
        "          ii. UPDATE users SET password = newHash WHERE username = current_user;\n"
        "          iii. Return True.\n"
        "4. Return False."
    )

    add_heading_3(doc, "Algorithm 6.3: Recursive Total Inventory Accumulation")
    add_body_p(
        doc,
        "Input: List of Crop objects (crops), Current Index (index)\n"
        "Output: Total physical units across all crops (Integer)\n"
        "1. Base Case: If crops is null or index < 0 or index >= crops.size(), return 0.\n"
        "2. Recursive Step: currentQuantity = (crops.get(index) != null) ? crops.get(index).getQuantity() : 0.\n"
        "3. Return currentQuantity + calculateRecursiveStockUnits(crops, index + 1).\n"
        "Overloaded entry method: calculateRecursiveStockUnits(crops) returns calculateRecursiveStockUnits(crops, 0)."
    )

    doc.add_page_break()
    print("Chapter 6 (System Design) generated successfully.")
