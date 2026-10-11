# -*- coding: utf-8 -*-
"""
YieldGrid Academic Project Report — Diagram Generator
Generates all 8 high-resolution architecture, workflow, ER, and UML class diagrams.
Engineered with generous container padding, multi-line auto-spacing, distinct title headers,
and clean orthogonal connector paths to ensure zero overlapping or overflowing text.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs('documentation_assets/diagrams', exist_ok=True)

def setup_fig(w=11, h=7.5, dpi=300):
    fig, ax = plt.subplots(figsize=(w, h), dpi=dpi)
    ax.axis('off')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    return fig, ax

def draw_container(ax, x, y, w, h, header_text, bg='#F8FAFC', border='#334E68', header_bg='#1E3A8A', header_color='#FFFFFF', radius=1.5):
    """Draws a layer container box with a dedicated top header banner so child boxes never collide with title."""
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.2,rounding_size={radius}",
                                  ec=border, fc=bg, lw=1.5, zorder=1)
    ax.add_patch(rect)
    
    # Header bar
    header_h = 3.6
    header_rect = patches.Rectangle((x + 0.2, y + h - header_h - 0.2), w - 0.4, header_h,
                                    fc=header_bg, ec='none', zorder=2)
    ax.add_patch(header_rect)
    ax.text(x + w / 2, y + h - header_h / 2 - 0.2, header_text,
            ha='center', va='center', fontsize=9.5, fontweight='bold', color=header_color, zorder=3)

def draw_card(ax, x, y, w, h, title, lines=None, bg='#FFFFFF', border='#2B5B84', 
              title_color='#0B2545', body_color='#334E68', title_size=9, body_size=7.5, radius=1.2, zorder=4):
    """Draws a component card with evenly distributed multi-line body text."""
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0.2,rounding_size={radius}",
                                  ec=border, fc=bg, lw=1.2, zorder=zorder)
    ax.add_patch(rect)
    
    if not lines:
        ax.text(x + w / 2, y + h / 2, title, ha='center', va='center',
                fontsize=title_size, fontweight='bold', color=title_color, zorder=zorder + 1)
        return

    # Title at top of card
    title_y = y + h - 1.8
    ax.text(x + w / 2, title_y, title, ha='center', va='center',
            fontsize=title_size, fontweight='bold', color=title_color, zorder=zorder + 1)
    
    # Divider line under title
    ax.plot([x + 1, x + w - 1], [y + h - 3.2, y + h - 3.2], color=border, lw=0.6, alpha=0.5, zorder=zorder + 1)
    
    # Body lines distributed in remaining vertical space
    num_lines = len(lines)
    avail_h = h - 4.2
    if num_lines > 0 and avail_h > 0:
        line_spacing = avail_h / (num_lines + 0.5)
        for idx, line in enumerate(lines):
            line_y = (y + h - 4.2) - (idx + 0.5) * line_spacing
            ax.text(x + w / 2, line_y, line, ha='center', va='center',
                    fontsize=body_size, color=body_color, zorder=zorder + 1)

def draw_arrow(ax, x1, y1, x2, y2, label=None, color='#1E3A8A', lw=1.5, label_offset=(0, 0), label_color='#0F2942', label_bg='#FFFFFF'):
    """Draws an arrow with an optional badge-backed label so lines never strike through text."""
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=2, shrinkB=2), zorder=2)
    if label:
        mx = (x1 + x2) / 2 + label_offset[0]
        my = (y1 + y2) / 2 + label_offset[1]
        bbox_props = dict(boxstyle="round,pad=0.2", fc=label_bg, ec=color, lw=0.8, alpha=0.95)
        ax.text(mx, my, label, ha='center', va='center', fontsize=7.5,
                fontweight='bold', color=label_color, bbox=bbox_props, zorder=5)

def draw_elbow_arrow(ax, points, label=None, color='#1E3A8A', lw=1.5, label_pos=None, label_color='#0F2942', label_bg='#FFFFFF'):
    """Draws an orthogonal multi-segment arrow path."""
    for i in range(len(points) - 2):
        p1, p2 = points[i], points[i+1]
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw, zorder=2)
    # Final segment with arrow head
    p_penult, p_last = points[-2], points[-1]
    ax.annotate('', xy=p_last, xytext=p_penult,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=2), zorder=2)
    if label and label_pos:
        bbox_props = dict(boxstyle="round,pad=0.2", fc=label_bg, ec=color, lw=0.8, alpha=0.95)
        ax.text(label_pos[0], label_pos[1], label, ha='center', va='center', fontsize=7.5,
                fontweight='bold', color=label_color, bbox=bbox_props, zorder=5)


# ==============================================================================
# 1. OVERALL SYSTEM ARCHITECTURE
# ==============================================================================
def make_diag_1():
    fig, ax = setup_fig(11, 8.2)
    ax.text(50, 97.5, "YieldGrid — Three-Tier Layered System Architecture",
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0B2545')
    
    # Layer 1: Presentation Layer
    draw_container(ax, 4, 76.5, 92, 17.5,
                   "PRESENTATION LAYER — Java Swing GUI (Event Dispatch Thread & Nimbus Look-and-Feel)",
                   bg='#F0F9FF', border='#0284C7', header_bg='#0284C7')
    draw_card(ax, 5.5, 78, 16.5, 11.5, "Login & Register",
              ["LoginFrame", "RegisterFrame", "Role-Based Dispatch"], border='#38BDF8')
    draw_card(ax, 23.5, 78, 17, 11.5, "Farmer Operations",
              ["FarmerDashboard", "Manage Crops Tab", "Incoming Orders", "Revenue & Sales Ledger"], border='#38BDF8')
    draw_card(ax, 42, 78, 17, 11.5, "Customer Marketplace",
              ["CustomerDashboard", "Browse Produce Tab", "Active Shopping Cart", "Order Tracking Panel"], border='#38BDF8')
    draw_card(ax, 60.5, 78, 17, 11.5, "Admin Console",
              ["AdminDashboard", "KPI Overview Cards", "User Accounts JTable", "JTree Hierarchy"], border='#38BDF8')
    draw_card(ax, 79, 78, 15.5, 11.5, "Theme & Dialogs",
              ["UITheme Engine", "ProfilePanel Dialog", "StyledButtonUI", "JFileChooser CSV"], border='#38BDF8')

    # Layer 2: Model Layer
    draw_container(ax, 4, 57, 92, 16.5,
                   "DOMAIN MODEL LAYER — Encapsulated Entities & Object-Oriented Hierarchy",
                   bg='#F8FAFC', border='#475569', header_bg='#334155')
    draw_card(ax, 5.5, 58.5, 20.5, 11, "User Base Entity",
              ["User (Abstract Class)", "userId, name, username", "passwordHash, role, isActive", "getRoleDescription() [abstract]"], border='#94A3B8')
    draw_card(ax, 28, 58.5, 20.5, 11, "Role Subclasses",
              ["Farmer (Producer Entity)", "Customer (Retail Buyer)", "AdminUser (Governance)", "Polymorphic dispatch"], border='#94A3B8')
    draw_card(ax, 50.5, 58.5, 20.5, 11, "Produce & Cart",
              ["Crop Domain Model", "CartItem Component", "price, quantity, available", "In-memory subtotal math"], border='#94A3B8')
    draw_card(ax, 73, 58.5, 21.5, 11, "Orders & Enums",
              ["Order & OrderItem Models", "orderId, totalAmount", "OrderStatus (Java Enum)", "PENDING..COMPLETED"], border='#94A3B8')

    # Layer 3: Service Layer
    draw_container(ax, 4, 37.5, 92, 16.5,
                   "SERVICE LAYER — Business Logic, Security Validation & ACID Transaction Boundaries",
                   bg='#F0FDF4', border='#16A34A', header_bg='#16A34A')
    draw_card(ax, 5.5, 39, 16.5, 11, "AuthService",
              ["SessionManager", "PBKDF2 Hashing", "Salt Generation", "Migration Check"], border='#86EFAC')
    draw_card(ax, 23.5, 39, 17, 11, "CropService",
              ["Produce Validation", "Ownership Isolation", "Stock Verification", "Listing CRUD"], border='#86EFAC')
    draw_card(ax, 42, 39, 17, 11, "OrderService",
              ["Multi-Farmer Split", "Cart Verification", "Atomic Checkout", "Status Workflow"], border='#86EFAC')
    draw_card(ax, 60.5, 39, 17, 11, "RevenueService",
              ["Earnings Summary", "Financial Ledger", "Recursive Stock Sum", "Turnover Metric"], border='#86EFAC')
    draw_card(ax, 79, 39, 15.5, 11, "AdminService",
              ["Platform Metrics", "Account Activation", "Anti-Lockout Guard", "Catalog Moderation"], border='#86EFAC')

    # Layer 4: Data Access Layer
    draw_container(ax, 4, 18, 92, 16.5,
                   "DATA ACCESS LAYER (DAO) — JDBC PreparedStatements & Transaction Management",
                   bg='#FFFBEB', border='#D97706', header_bg='#D97706')
    draw_card(ax, 5.5, 19.5, 20.5, 11, "UserDAO",
              ["authenticateUser()", "findUserByUsername()", "updateProfile()", "migratePasswordToPBKDF2()"], border='#FDE68A')
    draw_card(ax, 28, 19.5, 20.5, 11, "CropDAO",
              ["insertCrop(), updateCrop()", "getCropsByFarmer()", "searchCrops()", "atomicDecrementStock()"], border='#FDE68A')
    draw_card(ax, 50.5, 19.5, 20.5, 11, "OrderDAO",
              ["placeOrder() (ACID)", "setAutoCommit(false)", "commit() / rollback()", "getOrdersByCustomer/Farmer()"], border='#FDE68A')
    draw_card(ax, 73, 19.5, 21.5, 11, "AdminDAO",
              ["getSystemMetrics()", "getAllUsers()", "toggleUserStatus()", "logActivity() Audit Trail"], border='#FDE68A')

    # Layer 5: Relational Database
    draw_container(ax, 16, 2.5, 68, 12.5,
                   "PERSISTENCE STORAGE — MySQL Server 8.0+ (Connector/J Type-4 Driver)",
                   bg='#FEF2F2', border='#DC2626', header_bg='#DC2626')
    draw_card(ax, 18, 3.8, 64, 7.2, "Relational Schema Tables (Third Normal Form — 3NF)",
              ["users   •   crops   •   orders   •   order_items   •   activity_logs",
               "Referential Integrity Enforced via Foreign Keys (CASCADE / RESTRICT)"],
              border='#FCA5A5', bg='#FFFFFF', title_size=9, body_size=8)

    # Inter-layer connecting arrows with clean labeled badges
    draw_arrow(ax, 50, 76.5, 50, 73.5, label="UI Dispatches Entity Actions", color='#0284C7')
    draw_arrow(ax, 50, 57, 50, 54, label="Domain Models Passed to Services", color='#334155')
    draw_arrow(ax, 50, 37.5, 50, 34.5, label="Business Logic Invokes DAOs", color='#16A34A')
    draw_arrow(ax, 50, 18, 50, 15, label="JDBC PreparedStatement Execution", color='#D97706')

    plt.tight_layout()
    fig.savefig('documentation_assets/diagrams/system_architecture.png', dpi=300)
    fig.savefig('documentation_assets/diagrams/system_architecture.svg')
    plt.close()


# ==============================================================================
# 2. OVERALL APPLICATION WORKFLOW
# ==============================================================================
def make_diag_2():
    fig, ax = setup_fig(10.5, 8.5)
    ax.text(50, 97.5, "Overall Application Workflow & Role-Based Navigation",
            ha='center', va='center', fontsize=13.5, fontweight='bold', color='#0B2545')

    # Top Startup Sequence
    draw_card(ax, 32, 88.5, 36, 6.5, "Application Launch (Main.main())",
              ["Swing EDT Bootstrap  •  UITheme Nimbus Look-and-Feel"],
              bg='#EFF6FF', border='#2563EB', title_color='#1E40AF', title_size=9, body_size=7.5)

    draw_card(ax, 32, 78, 36, 6.5, "Database Connectivity Check",
              ["DBConnection.testConnection()  •  MySQL Port 3306"],
              bg='#F0FDF4', border='#16A34A', title_color='#166534', title_size=9, body_size=7.5)
    draw_arrow(ax, 50, 88.5, 50, 84.5)

    # Login in center and Registration on the right
    draw_card(ax, 32, 66, 36, 7.5, "Authentication (LoginFrame)",
              ["Input Username & Password  •  Role Quick-Fill Buttons"],
              bg='#FEF3C7', border='#D97706', title_color='#92400E', title_size=9, body_size=7.5)
    draw_arrow(ax, 50, 78, 50, 73.5)

    draw_card(ax, 72, 66, 25, 7.5, "Registration (RegisterFrame)",
              ["Full Name, Role, Password, Contact"],
              bg='#F5F3FF', border='#7C3AED', title_color='#5B21B6', title_size=8.5, body_size=7.2)
    
    # Horizontal arrows between Login and Register
    draw_arrow(ax, 68, 70.5, 72, 70.5, label="New User", color='#7C3AED', label_offset=(0, 0))
    draw_arrow(ax, 72, 68, 68, 68, label="Registered", color='#16A34A', label_offset=(0, 0))

    # Role Resolution & Session Manager
    draw_card(ax, 24, 53, 52, 8, "Role Resolution & Session Initialization",
              ["AuthenticationService verifies PBKDF2 hash  •  Checks isActive",
               "SessionManager.setCurrentUser() sets active authenticated context"],
              bg='#FEF9C3', border='#CA8A04', title_color='#854D0E', title_size=9.5, body_size=7.8)
    draw_arrow(ax, 50, 66, 50, 61, color='#D97706')

    # Three Role Pathways
    # Farmer
    draw_card(ax, 4, 34, 28, 14, "FARMER WORKFLOW",
              ["FarmerDashboard (JFrame)",
               "• Manage Crops: Add, edit stock & price",
               "• Incoming Orders: Confirm & complete",
               "• Revenue & Sales: Ledger & totals",
               "• Export CSV: Orders and sales reports"],
              bg='#F0FDF4', border='#16A34A', title_color='#15803D', title_size=9, body_size=7.5)
    draw_arrow(ax, 32, 53, 18, 48, label="Role: FARMER", color='#16A34A', label_offset=(-2, 0))

    # Customer
    draw_card(ax, 36, 34, 28, 14, "CUSTOMER WORKFLOW",
              ["CustomerDashboard (JFrame)",
               "• Browse Produce: Live keyword filter",
               "• Shopping Cart: Subtotaling & quantity",
               "• Atomic Checkout: Instant stock debit",
               "• My Orders: Status tracking & items"],
              bg='#EFF6FF', border='#2563EB', title_color='#1D4ED8', title_size=9, body_size=7.5)
    draw_arrow(ax, 50, 53, 50, 48, label="Role: CUSTOMER", color='#2563EB', label_offset=(0, 0))

    # Admin
    draw_card(ax, 68, 34, 28, 14, "ADMINISTRATOR WORKFLOW",
              ["AdminDashboard (JFrame)",
               "• System Overview: 6 KPI live metrics",
               "• User Accounts: Moderation & status",
               "• Produce & Orders: Cross-tenant view",
               "• Platform Hierarchy: JTree navigation"],
              bg='#FEF2F2', border='#DC2626', title_color='#B91C1C', title_size=9, body_size=7.5)
    draw_arrow(ax, 68, 53, 82, 48, label="Role: ADMIN", color='#DC2626', label_offset=(2, 0))

    # Shared Account Panel
    draw_card(ax, 20, 16.5, 60, 11, "SHARED ACCOUNT ACTIONS (ProfilePanel Dialog)",
              ["View Account Profile Details  •  Update Contact Information & Delivery Address",
               "Secure Password Change (Salted PBKDF2 with HMAC-SHA256)",
               "Data Export (RFC 4180 CSV via DataExporter)"],
              bg='#F8FAFC', border='#475569', title_color='#1E293B', title_size=9, body_size=7.8)
    draw_arrow(ax, 18, 34, 30, 27.5, color='#16A34A')
    draw_arrow(ax, 50, 34, 50, 27.5, color='#2563EB')
    draw_arrow(ax, 82, 34, 70, 27.5, color='#DC2626')

    # Logout Action & Perimeter Loop
    draw_card(ax, 38, 4, 24, 7.5, "Session Logout",
              ["SessionManager.logout()", "Clear user & shopping cart"],
              bg='#FEE2E2', border='#EF4444', title_color='#B91C1C', title_size=8.5, body_size=7.2)
    draw_arrow(ax, 50, 16.5, 50, 11.5, color='#EF4444')

    # Perimeter return route from Logout back to LoginFrame (no crossings!)
    draw_elbow_arrow(ax, [(38, 7.5), (2, 7.5), (2, 69.5), (18, 69.5)],
                     label="Back to Login", color='#DC2626', label_pos=(2, 40))

    plt.tight_layout()
    fig.savefig('documentation_assets/diagrams/overall_application_workflow.png', dpi=300)
    fig.savefig('documentation_assets/diagrams/overall_application_workflow.svg')
    plt.close()


# ==============================================================================
# 3. FARMER OPERATIONAL WORKFLOW
# ==============================================================================
def make_diag_3():
    fig, ax = setup_fig(10.5, 7.5)
    ax.text(50, 97, "Farmer Role — Operational & Produce Inventory Workflow",
            ha='center', va='center', fontsize=13.5, fontweight='bold', color='#14532D')

    draw_card(ax, 32, 87.5, 36, 6.5, "Farmer Authenticated",
              ["FarmerDashboard Active  •  Session Context Initialized"],
              bg='#DCFCE7', border='#16A34A', title_color='#14532D', title_size=9.5, body_size=7.8)

    # 4 Main Functional Panels
    draw_card(ax, 4, 58, 21.5, 24, "1. Produce Inventory",
              ["Manage Crops Tab",
               "• Register new crop listing",
               "• Botanical/common name",
               "• Direct unit price (INR)",
               "• Physical stock quantity",
               "• Update stock & pricing",
               "• Delete crop (Owner check)",
               "• Toggle availability flag"],
              bg='#F0FDF4', border='#16A34A', title_color='#15803D', title_size=9, body_size=7.4)

    draw_card(ax, 28, 58, 21.5, 24, "2. Order Fulfillment",
              ["Incoming Orders Tab",
               "• Live incoming orders list",
               "• Customer details inspection",
               "• Line items breakdown",
               "• Unit price & subtotal audit",
               "• Transition to CONFIRMED",
               "• Transition to COMPLETED",
               "• Lifecycle state validation"],
              bg='#F0FDF4', border='#16A34A', title_color='#15803D', title_size=9, body_size=7.4)

    draw_card(ax, 52, 58, 21.5, 24, "3. Revenue Analytics",
              ["Revenue & Sales Tab",
               "• Gross revenue metrics card",
               "• Completed orders counter",
               "• Financial ledger JTable",
               "• Real-time sales summation",
               "• Recursive stock inventory",
               "• Average revenue per order",
               "• Sales performance trends"],
              bg='#F0FDF4', border='#16A34A', title_color='#15803D', title_size=9, body_size=7.4)

    draw_card(ax, 76, 58, 20, 24, "4. Profile & Account",
              ["ProfilePanel Dialog",
               "• Farm credentials view",
               "• Legal business name",
               "• Update telephone & address",
               "• Secure PBKDF2 password",
               "• Password match audit",
               "• Transparent DB update",
               "• Safe session logout"],
              bg='#F0FDF4', border='#16A34A', title_color='#15803D', title_size=9, body_size=7.4)

    draw_arrow(ax, 38, 87.5, 15, 82, color='#16A34A')
    draw_arrow(ax, 46, 87.5, 39, 82, color='#16A34A')
    draw_arrow(ax, 54, 87.5, 63, 82, color='#16A34A')
    draw_arrow(ax, 62, 87.5, 86, 82, color='#16A34A')

    # Persistence interactions
    draw_container(ax, 8, 26, 84, 18,
                   "SERVICE & DATA PERSISTENCE INTEGRATION",
                   bg='#F8FAFC', border='#334155', header_bg='#334155')
    draw_card(ax, 10, 27.5, 25.5, 12, "CropService Tier",
              ["CropService ↔ CropDAO", "Multi-tenant ownership check", "crops table in MySQL"],
              border='#94A3B8', title_size=8.5, body_size=7.2)
    draw_card(ax, 37.5, 27.5, 25.5, 12, "Order & Revenue Tier",
              ["OrderService / RevenueService", "OrderDAO SQL aggregates", "orders & order_items tables"],
              border='#94A3B8', title_size=8.5, body_size=7.2)
    draw_card(ax, 65, 27.5, 25, 12, "Auth & Profile Tier",
              ["AuthenticationService", "UserDAO credential update", "users table in MySQL"],
              border='#94A3B8', title_size=8.5, body_size=7.2)

    draw_arrow(ax, 15, 58, 22, 44, color='#16A34A')
    draw_arrow(ax, 39, 58, 48, 44, color='#16A34A')
    draw_arrow(ax, 63, 58, 52, 44, color='#16A34A')
    draw_arrow(ax, 86, 58, 77, 44, color='#16A34A')

    # Bottom File Export Engine
    draw_card(ax, 24, 4.5, 52, 14, "Local File Reporting Engine (DataExporter)",
              ["RFC 4180 Structured CSV Export  •  java.io File Streams",
               "CSV Formula Injection Defense: Prepends single quote (') to sanitize formulas",
               "Outputs: farmer_incoming_orders.csv  •  farmer_revenue_ledger.csv"],
              bg='#FFFFFF', border='#16A34A', title_color='#15803D', title_size=9, body_size=7.6)
    draw_arrow(ax, 50, 26, 50, 18.5, label="Export Action", color='#16A34A')

    plt.tight_layout()
    fig.savefig('documentation_assets/diagrams/farmer_workflow.png', dpi=300)
    fig.savefig('documentation_assets/diagrams/farmer_workflow.svg')
    plt.close()


# ==============================================================================
# 4. CUSTOMER OPERATIONAL WORKFLOW
# ==============================================================================
def make_diag_4():
    fig, ax = setup_fig(10.5, 7.5)
    ax.text(50, 97, "Customer Role — Marketplace, Shopping Cart & Tracking Workflow",
            ha='center', va='center', fontsize=13.5, fontweight='bold', color='#1E40AF')

    draw_card(ax, 32, 87.5, 36, 6.5, "Customer Authenticated",
              ["CustomerDashboard Active  •  Session Context Initialized"],
              bg='#DBEAFE', border='#2563EB', title_color='#1E40AF', title_size=9.5, body_size=7.8)

    # 3 Sequential Primary Steps
    draw_card(ax, 4, 56, 28, 25, "1. Produce Marketplace",
              ["Browse Produce Tab",
               "• Live produce catalog in JTable",
               "• Real-time search keyword filter",
               "• Inspect producer (farmer) details",
               "• Inspect unit price & available units",
               "• Quantity selector (JSpinner)",
               "• In-memory stock validation guard",
               "• 'Add to Cart' user action"],
              bg='#EFF6FF', border='#2563EB', title_color='#1D4ED8', title_size=9.5, body_size=7.6)

    draw_card(ax, 36, 56, 28, 25, "2. Active Shopping Cart",
              ["My Shopping Cart Tab",
               "• In-memory CartItem collection",
               "• Dynamic subtotal recalculation",
               "• Adjust purchase quantities",
               "• Remove unwanted produce items",
               "• Multi-farmer produce grouping",
               "• Total checkout amount preview",
               "• 'Proceed to Checkout' action"],
              bg='#EFF6FF', border='#2563EB', title_color='#1D4ED8', title_size=9.5, body_size=7.6)

    draw_card(ax, 68, 56, 28, 25, "3. Atomic Checkout",
              ["Order Placement Engine",
               "• Discrete order per distinct farmer",
               "• ACID JDBC transaction boundary",
               "• Atomic conditional stock update",
               "• InsufficientStockException guard",
               "• Order line items insertion",
               "• Empty cart upon success",
               "• Order tracking dispatch"],
              bg='#EFF6FF', border='#2563EB', title_color='#1D4ED8', title_size=9.5, body_size=7.6)

    draw_arrow(ax, 42, 87.5, 18, 81, color='#2563EB')
    draw_arrow(ax, 32, 68.5, 36, 68.5, label="Add to Cart", color='#2563EB')
    draw_arrow(ax, 64, 68.5, 68, 68.5, label="Checkout", color='#2563EB', label_offset=(0, 2.5))

    # Order History & Tracking below Checkout (clean straight downward flow)
    draw_card(ax, 52, 25, 44, 22, "4. Order History & Status Tracking",
              ["My Orders & Tracking Tab",
               "• Comprehensive order history table",
               "• Real-time status: PENDING → CONFIRMED → COMPLETED",
               "• Order details dialog (item quantities, unit price, totals)",
               "• Export order history to customer_orders.csv"],
              bg='#F8FAFC', border='#475569', title_color='#1E293B', title_size=9, body_size=7.6)

    # Customer Profile on left side
    draw_card(ax, 4, 25, 44, 22, "5. Profile & Security Management",
              ["ProfilePanel Dialog",
               "• View registered name, username, and account identity",
               "• Edit physical delivery address and telephone contact",
               "• Secure password reset via salted PBKDF2 with HMAC-SHA256",
               "• Immediate persistent update to MySQL users table"],
              bg='#F8FAFC', border='#475569', title_color='#1E293B', title_size=9, body_size=7.6)

    # Straight vertical arrow from Checkout down to Order Tracking!
    draw_arrow(ax, 82, 56, 82, 47, label="Order Placed", color='#16A34A')
    # Horizontal link between Order Tracking and Profile
    draw_arrow(ax, 52, 36, 48, 36, label="Account Settings", color='#475569')

    # Bottom ACID Banner
    draw_card(ax, 16, 4, 68, 14, "TRANSACTIONAL INTEGRITY GUARANTEE (OrderDAO.placeOrder)",
              ["conn.setAutoCommit(false) wraps order header, order items, and stock deductions",
               "UPDATE crops SET quantity = quantity - ? WHERE crop_id = ? AND quantity >= ?",
               "Automatic conn.rollback() on inventory exhaustion; atomic commit() on success"],
              bg='#FFFBEB', border='#D97706', title_color='#92400E', title_size=9, body_size=7.6)
    draw_arrow(ax, 74, 25, 65, 18, color='#D97706')

    plt.tight_layout()
    fig.savefig('documentation_assets/diagrams/customer_workflow.png', dpi=300)
    fig.savefig('documentation_assets/diagrams/customer_workflow.svg')
    plt.close()


# ==============================================================================
# 5. ADMINISTRATOR OPERATIONAL WORKFLOW
# ==============================================================================
def make_diag_5():
    fig, ax = setup_fig(10.5, 7.5)
    ax.text(50, 97, "Administrator Role — Platform Governance & Auditing Workflow",
            ha='center', va='center', fontsize=13.5, fontweight='bold', color='#991B1B')

    draw_card(ax, 28, 87.5, 44, 6.5, "Administrator Authenticated",
              ["AdminDashboard Active  •  AdminService.requireAdminAccess() Verified"],
              bg='#FEE2E2', border='#DC2626', title_color='#991B1B', title_size=9.5, body_size=7.8)

    # 4 Main Governance Domains
    draw_card(ax, 4, 57, 21.5, 25, "1. Platform Overview",
              ["System Overview Tab",
               "• 6 Real-time KPI summary cards",
               "• Total registered user count",
               "• Active registered farmers",
               "• Catalog produce varieties",
               "• Gross platform orders placed",
               "• Completed marketplace GMV",
               "• Auto-refresh metric listener"],
              bg='#FEF2F2', border='#DC2626', title_color='#B91C1C', title_size=9, body_size=7.4)

    draw_card(ax, 28, 57, 21.5, 25, "2. User Account Control",
              ["User Accounts Tab",
               "• Master user accounts in JTable",
               "• Real-time role filtering & search",
               "• Edit user contact details",
               "• Toggle active/deactivated flag",
               "• Anti-Lockout Defense Guard",
               "• Prevents disabling last admin",
               "• Export users to CSV report"],
              bg='#FEF2F2', border='#DC2626', title_color='#B91C1C', title_size=9, body_size=7.4)

    draw_card(ax, 52, 57, 21.5, 25, "3. Catalog & Orders",
              ["Produce & Orders Tabs",
               "• Global produce catalog moderation",
               "• Edit unit price & stock across crops",
               "• Toggle catalog availability flag",
               "• Platform-wide master orders view",
               "• Inspect customer & farmer details",
               "• Audit line items & order status",
               "• Update order lifecycle state"],
              bg='#FEF2F2', border='#DC2626', title_color='#B91C1C', title_size=9, body_size=7.4)

    draw_card(ax, 76, 57, 20, 25, "4. Hierarchy & Reports",
              ["Platform Hierarchy Tab",
               "• JTree Organizational Explorer",
               "• Platform Root Node",
               "  ├─ Administrators Branch",
               "  ├─ Registered Farmers & Crops",
               "  └─ Customers & Order History",
               "• Administrative activity logs audit",
               "• Export master orders CSV report"],
              bg='#FEF2F2', border='#DC2626', title_color='#B91C1C', title_size=9, body_size=7.4)

    draw_arrow(ax, 36, 87.5, 15, 82, color='#DC2626')
    draw_arrow(ax, 44, 87.5, 39, 82, color='#DC2626')
    draw_arrow(ax, 56, 87.5, 63, 82, color='#DC2626')
    draw_arrow(ax, 64, 87.5, 86, 82, color='#DC2626')

    # Security & Governance Controls Container
    draw_container(ax, 8, 24, 84, 25,
                   "PLATFORM GOVERNANCE, SAFETY & AUDIT INTEGRITY CONTROLS",
                   bg='#FFFBEB', border='#D97706', header_bg='#D97706')
    draw_card(ax, 10, 25.5, 39, 18, "Access & Lockout Safeguards",
              ["• Service-Layer Security: Role authorization enforced in",
               "  AdminService, never relying on UI visibility alone",
               "• Anti-Lockout Guard: System automatically rejects",
               "  deactivation of the final active administrator account",
               "• Immutable Session State: Re-authenticates critical tasks"],
              border='#FDE68A', title_size=8.5, body_size=7.3)

    draw_card(ax, 51, 25.5, 39, 18, "Auditing & Relational Persistence",
              ["• Activity Logs: Administrative actions recorded with",
               "  userId, action type, description, and timestamp",
               "• Immediate Persistence: Direct JDBC execution against",
               "  MySQL tables (users, crops, orders, activity_logs)",
               "• Safe Cryptography: PBKDF2 with transparent upgrade"],
              border='#FDE68A', title_size=8.5, body_size=7.3)

    draw_arrow(ax, 15, 57, 24, 49, color='#D97706')
    draw_arrow(ax, 39, 57, 36, 49, color='#D97706')
    draw_arrow(ax, 63, 57, 65, 49, color='#D97706')
    draw_arrow(ax, 86, 57, 76, 49, color='#D97706')

    # Bottom Relational Storage Box
    draw_card(ax, 22, 4, 56, 14, "Underlying Relational Persistence Engine",
              ["MySQL Server 8.0+ via Type-4 Connector/J Driver  •  Port 3306",
               "Synchronized JTable models with live SQL queries",
               "Guaranteed transaction consistency and immediate state visibility across roles"],
              bg='#FFFFFF', border='#DC2626', title_color='#991B1B', title_size=9, body_size=7.5)
    draw_arrow(ax, 50, 24, 50, 18, color='#DC2626')

    plt.tight_layout()
    fig.savefig('documentation_assets/diagrams/admin_workflow.png', dpi=300)
    fig.savefig('documentation_assets/diagrams/admin_workflow.svg')
    plt.close()


# ==============================================================================
# 6. ENTITY-RELATIONSHIP DIAGRAM (ERD)
# ==============================================================================
def make_diag_6():
    fig, ax = setup_fig(11, 8.2)
    ax.text(50, 97.5, "YieldGrid — Relational Entity-Relationship (E-R) Diagram",
            ha='center', va='center', fontsize=14, fontweight='bold', color='#0B2545')

    # Table 1: users (Top Left)
    draw_card(ax, 5, 52, 36, 40, "users (User Accounts)",
              ["user_id : INT  [PRIMARY KEY, AUTO_INCREMENT]",
               "name : VARCHAR(100)  [NOT NULL]",
               "username : VARCHAR(50)  [NOT NULL, UNIQUE]",
               "password : VARCHAR(255)  [NOT NULL, PBKDF2]",
               "role : VARCHAR(20)  [NOT NULL, (FARMER|CUSTOMER|ADMIN)]",
               "contact_info : VARCHAR(150)  [NULLABLE]",
               "is_active : BOOLEAN  [DEFAULT TRUE]",
               "created_at : TIMESTAMP  [DEFAULT CURRENT_TIMESTAMP]"],
              bg='#F0F9FF', border='#0284C7', title_color='#0369A1', title_size=9.5, body_size=7.5)

    # Table 2: crops (Top Right)
    draw_card(ax, 59, 52, 36, 40, "crops (Produce Inventory)",
              ["crop_id : INT  [PRIMARY KEY, AUTO_INCREMENT]",
               "farmer_id : INT  [FOREIGN KEY -> users.user_id]",
               "crop_name : VARCHAR(100)  [NOT NULL]",
               "description : TEXT  [NULLABLE]",
               "quantity : INT  [NOT NULL, CHECK (quantity >= 0)]",
               "price : DECIMAL(10,2)  [NOT NULL, CHECK (price > 0)]",
               "available : BOOLEAN  [DEFAULT TRUE]",
               "created_at : TIMESTAMP  [DEFAULT CURRENT_TIMESTAMP]"],
              bg='#F0FDF4', border='#16A34A', title_color='#15803D', title_size=9.5, body_size=7.5)

    # Table 3: orders (Bottom Left)
    draw_card(ax, 5, 4, 36, 40, "orders (Purchase Orders)",
              ["order_id : INT  [PRIMARY KEY, AUTO_INCREMENT]",
               "customer_id : INT  [FOREIGN KEY -> users.user_id]",
               "farmer_id : INT  [FOREIGN KEY -> users.user_id]",
               "order_date : TIMESTAMP  [DEFAULT CURRENT_TIMESTAMP]",
               "total_amount : DECIMAL(10,2)  [NOT NULL]",
               "status : VARCHAR(20)  [OrderStatus Lifecycle Enum]",
               "(PENDING, CONFIRMED, SHIPPED, DELIVERED, CANCELLED)"],
              bg='#FFFBEB', border='#D97706', title_color='#B45309', title_size=9.5, body_size=7.5)

    # Table 4: order_items (Bottom Right)
    draw_card(ax, 59, 4, 36, 40, "order_items (Order Line Items)",
              ["order_item_id : INT  [PRIMARY KEY, AUTO_INCREMENT]",
               "order_id : INT  [FOREIGN KEY -> orders.order_id]",
               "crop_id : INT  [FOREIGN KEY -> crops.crop_id]",
               "quantity : INT  [NOT NULL, CHECK (quantity > 0)]",
               "unit_price : DECIMAL(10,2)  [NOT NULL (at order time)]",
               "subtotal : DECIMAL(10,2)  [quantity * unit_price]"],
              bg='#FDF2F8', border='#DB2777', title_color='#BE185D', title_size=9.5, body_size=7.5)

    # Relationships with clean non-overlapping labels
    # users -> crops (1 : N, Farmer lists produce)
    draw_arrow(ax, 41, 72, 59, 72, label="1 : N  (Farmer Lists Produce)", color='#16A34A')

    # users -> orders (Customer places order, 1 : N)
    draw_arrow(ax, 14, 52, 14, 44, label="1 : N  (Places)", color='#2563EB', label_offset=(-4, 0))

    # users -> orders (Farmer fulfills order, 1 : N)
    draw_arrow(ax, 32, 52, 32, 44, label="1 : N  (Fulfills)", color='#16A34A', label_offset=(4, 0))

    # orders -> order_items (1 : N, Order contains items)
    draw_arrow(ax, 41, 24, 59, 24, label="1 : N  (Contains Line Items)", color='#D97706')

    # crops -> order_items (1 : N, Crop referenced in line items)
    draw_arrow(ax, 77, 52, 77, 44, label="1 : N  (Referenced In)", color='#DB2777')

    plt.tight_layout()
    fig.savefig('documentation_assets/diagrams/entity_relationship_diagram.png', dpi=300)
    fig.savefig('documentation_assets/diagrams/entity_relationship_diagram.svg')
    plt.close()


# ==============================================================================
# 7. ORDER PLACEMENT & INVENTORY CONSISTENCY WORKFLOW
# ==============================================================================
def make_diag_7():
    fig, ax = setup_fig(10.5, 9.2)
    ax.text(50, 97.5, "Order Placement & Inventory Transaction Workflow (ACID Lifecycle)",
            ha='center', va='center', fontsize=13.5, fontweight='bold', color='#C2410C')

    draw_card(ax, 26, 88.5, 48, 6.5, "Customer Confirms Cart Checkout",
              ["Shopping cart contains N items across M farmers  •  Session verified"],
              bg='#EFF6FF', border='#2563EB', title_color='#1E40AF', title_size=9, body_size=7.5)

    draw_card(ax, 24, 78, 52, 6.5, "OrderService.placeOrdersFromCart()",
              ["Pre-validates cart non-empty  •  Groups cart items by distinct farmerId"],
              bg='#EFF6FF', border='#2563EB', title_color='#1E40AF', title_size=9, body_size=7.5)
    draw_arrow(ax, 50, 88.5, 50, 84.5)

    draw_card(ax, 20, 67.5, 60, 6.5, "Begin Explicit JDBC Transaction Boundary (OrderDAO)",
              ["conn.setAutoCommit(false)  •  Disables automatic commits"],
              bg='#FFFBEB', border='#D97706', title_color='#B45309', title_size=9, body_size=7.5)
    draw_arrow(ax, 50, 78, 50, 74)

    draw_card(ax, 24, 57, 52, 6.5, "Insert Master Order Header into 'orders'",
              ["INSERT INTO orders (customer_id, farmer_id, total, status)  •  Retrieves order_id"],
              bg='#FFFBEB', border='#D97706', title_color='#B45309', title_size=9, body_size=7.5)
    draw_arrow(ax, 50, 67.5, 50, 63.5)

    draw_card(ax, 14, 44, 72, 8.5, "Process Line Items & Atomic Stock Decrement",
              ["1. INSERT INTO order_items (order_id, crop_id, quantity, unit_price, subtotal)",
               "2. Execute atomic conditional decrement SQL:",
               "UPDATE crops SET quantity = quantity - ? WHERE crop_id = ? AND quantity >= ?"],
              bg='#FEF2F2', border='#DC2626', title_color='#991B1B', title_size=9, body_size=7.5)
    draw_arrow(ax, 50, 57, 50, 52.5)

    # Decision Node
    draw_card(ax, 32, 31.5, 36, 7.5, "Stock Decrement Succeeded?\n(rowsAffected > 0)",
              None, bg='#FEF9C3', border='#CA8A04', title_color='#854D0E', title_size=9)
    draw_arrow(ax, 50, 44, 50, 39)

    # Branch Left: Rollback
    draw_card(ax, 4, 17, 40, 10, "INSUFFICIENT STOCK / CONFLICT",
              ["• rowsAffected == 0 (stock depleted concurrently)",
               "• conn.rollback() cancels all previous inserts",
               "• Throw InsufficientStockException",
               "• Zero partial or orphaned records remain in DB"],
              bg='#FEE2E2', border='#DC2626', title_color='#991B1B', title_size=8.5, body_size=7.2)
    draw_arrow(ax, 32, 35, 24, 27, label="NO (rows == 0)", color='#DC2626')

    # Branch Right: Success / Next Item
    draw_card(ax, 56, 17, 40, 10, "ITEM STOCK RESERVED",
              ["• rowsAffected == 1 (inventory decremented safely)",
               "• Line item committed to current transaction",
               "• Advance to next item in active order group",
               "• Repeat for all remaining items in cart"],
              bg='#DCFCE7', border='#16A34A', title_color='#15803D', title_size=8.5, body_size=7.2)
    draw_arrow(ax, 68, 35, 76, 27, label="YES (rows > 0)", color='#16A34A')

    # Final Atomic Commit
    draw_card(ax, 22, 5, 56, 7.5, "All Items Processed Successfully -> conn.commit()",
              ["Transaction committed atomically to MySQL  •  conn.setAutoCommit(true)",
               "SessionManager.clearCart()  •  Customer redirected to My Orders view"],
              bg='#DCFCE7', border='#16A34A', title_color='#14532D', title_size=9, body_size=7.5)
    draw_arrow(ax, 76, 17, 60, 12.5, color='#16A34A')

    plt.tight_layout()
    fig.savefig('documentation_assets/diagrams/order_inventory_transaction_workflow.png', dpi=300)
    fig.savefig('documentation_assets/diagrams/order_inventory_transaction_workflow.svg')
    plt.close()


# ==============================================================================
# 8. COMPONENT & CLASS DIAGRAM (UML)
# ==============================================================================
def make_diag_8():
    fig, ax = setup_fig(11, 8.5)
    ax.text(50, 97.5, "YieldGrid — Component & UML Class Hierarchy Diagram",
            ha='center', va='center', fontsize=14, fontweight='bold', color='#1E1B4B')

    # Interfaces (Top Left)
    draw_card(ax, 3, 73, 22, 20, "<<interface>>\nDashboardActions",
              ["+ APPLICATION_NAME : String",
               "+ refreshData() : void",
               "+ showProfile() : void",
               "+ logout() : void"],
              bg='#F5F3FF', border='#7C3AED', title_color='#5B21B6', title_size=9, body_size=7.2)

    draw_card(ax, 28, 73, 21, 20, "<<interface>>\nAdminActions",
              ["extends DashboardActions",
               "+ auditUserAccounts() : void",
               "+ viewSystemMetrics() : void",
               "+ exportAuditReport() : void"],
              bg='#F5F3FF', border='#7C3AED', title_color='#5B21B6', title_size=9, body_size=7.2)
    draw_arrow(ax, 28, 83, 25, 83, label="extends", color='#7C3AED')

    # Abstract Class User (Top Right)
    draw_card(ax, 56, 70, 41, 23, "<<abstract>>\nUser",
              ["- userId : int  |  username, name, role : String",
               "- passwordHash : String  |  contactInfo : String",
               "- isActive : boolean  |  createdAt : Timestamp",
               "+ getRoleDescription() : String {abstract}",
               "+ getDashboardTitle() : String {abstract}",
               "+ equals(), hashCode(), toString() : Object overrides"],
              bg='#EFF6FF', border='#2563EB', title_color='#1E40AF', title_size=9.5, body_size=7.2)

    # GUI Implementation Classes (Middle Left)
    draw_card(ax, 3, 46, 14, 18, "FarmerDashboard",
              ["extends JFrame", "implements DashboardActions", "Manage Crops, Incoming", "Orders, Revenue Analytics"],
              bg='#FFFFFF', border='#059669', title_color='#065F46', title_size=8, body_size=6.7)
    draw_arrow(ax, 10, 64, 10, 73, label="implements", color='#059669', label_offset=(-3.5, 0))

    draw_card(ax, 18.5, 46, 14, 18, "CustomerDashboard",
              ["extends JFrame", "implements DashboardActions", "Browse Produce, Shopping", "Cart, My Orders Tracking"],
              bg='#FFFFFF', border='#059669', title_color='#065F46', title_size=8, body_size=6.7)
    draw_arrow(ax, 21, 64, 18, 73, color='#059669')

    draw_card(ax, 34, 46, 15, 18, "AdminDashboard",
              ["extends JFrame", "implements AdminActions", "System KPI Cards, Users,", "Catalog, Platform JTree"],
              bg='#FFFFFF', border='#059669', title_color='#065F46', title_size=8, body_size=6.7)
    draw_arrow(ax, 40, 64, 40, 73, label="implements", color='#059669', label_offset=(3.5, 0))

    # Subclasses of User (Middle Right, side by side, clean upward generalization)
    draw_card(ax, 54, 46, 13, 18, "Farmer\n(Producer)",
              ["extends User", "+ getRoleDescription():", "  'Farmer / Producer'", "+ getDashboardTitle():", "  'Farmer Dashboard'"],
              bg='#FFFFFF', border='#2563EB', title_color='#1E40AF', title_size=8, body_size=6.6)
    draw_arrow(ax, 60.5, 64, 63, 70, label="extends", color='#2563EB', label_offset=(-2.5, 0))

    draw_card(ax, 68.5, 46, 13, 18, "Customer\n(Consumer)",
              ["extends User", "+ getRoleDescription():", "  'Retail Customer'", "+ getDashboardTitle():", "  'Customer Dashboard'"],
              bg='#FFFFFF', border='#2563EB', title_color='#1E40AF', title_size=8, body_size=6.6)
    draw_arrow(ax, 75, 64, 76.5, 70, color='#2563EB')

    draw_card(ax, 83, 46, 14, 18, "AdminUser\n(Governance)",
              ["extends User", "- privilegeLevel : String", "+ getRoleDescription():", "  'Administrator'", "+ getDashboardTitle():", "  'Admin Console'"],
              bg='#FFFFFF', border='#2563EB', title_color='#1E40AF', title_size=8, body_size=6.6)
    draw_arrow(ax, 89.5, 64, 87, 70, color='#2563EB')

    # Architecture, Service & Utility Engines (Bottom Row)
    draw_card(ax, 3, 10, 21.5, 28, "OrderDAO (ACID Engine)",
              ["Transactional DAO Layer",
               "+ placeOrdersFromCart(conn, ...)",
               "+ updateOrderStatus(orderId, ...)",
               "+ getOrdersByCustomerId(id)",
               "Atomic Decrement SQL:",
               "UPDATE crops SET qty = qty - ?",
               "WHERE crop_id = ? AND qty >= ?",
               "Explicit conn.rollback() on fault"],
              bg='#FFFBEB', border='#D97706', title_color='#B45309', title_size=8.5, body_size=6.8)

    draw_card(ax, 27, 10, 21.5, 28, "PasswordUtil",
              ["Cryptographic Security Engine",
               "+ hashPassword(plain) : String",
               "+ verifyPassword(cand, hash)",
               "+ needsMigration(hash) : bool",
               "- slowEquals(a, b) : boolean",
               "Algorithm: PBKDF2WithHmacSHA256",
               "10,000 Iterations  •  64-char Hex",
               "Timing-attack safe verification"],
              bg='#FFFBEB', border='#D97706', title_color='#B45309', title_size=8.5, body_size=6.8)

    draw_card(ax, 51, 10, 22, 28, "DataExporter",
              ["CSV File I/O Engine",
               "+ exportUsersToCSV(file, list)",
               "+ exportOrdersToCSV(file, list)",
               "+ sanitizeCsvValue(val) : String",
               "RFC 4180 Escaping Standards",
               "Spreadsheet Formula Injection Defense",
               "(Prepends single quote if prefixed",
               "with =, +, -, or @)"],
              bg='#FFFBEB', border='#D97706', title_color='#B45309', title_size=8.5, body_size=6.8)

    draw_card(ax, 75.5, 10, 21.5, 28, "MultithreadingDemo",
              ["Producer-Consumer Concurrency",
               "+ Producer implements Runnable",
               "+ ConsumerThread extends Thread",
               "+ synchronized shared queue",
               "+ wait() on buffer full / empty",
               "+ notifyAll() on state change",
               "Thread-safe inter-thread coordination",
               "Zero race conditions"],
              bg='#FFFBEB', border='#D97706', title_color='#B45309', title_size=8.5, body_size=6.8)

    plt.tight_layout()
    fig.savefig('documentation_assets/diagrams/component_class_diagram.png', dpi=300)
    fig.savefig('documentation_assets/diagrams/component_class_diagram.svg')
    plt.close()


if __name__ == '__main__':
    print("Generating diagrams...")
    make_diag_1()
    print("1/8 System Architecture generated.")
    make_diag_2()
    print("2/8 Overall Workflow generated.")
    make_diag_3()
    print("3/8 Farmer Workflow generated.")
    make_diag_4()
    print("4/8 Customer Workflow generated.")
    make_diag_5()
    print("5/8 Admin Workflow generated.")
    make_diag_6()
    print("6/8 E-R Diagram generated.")
    make_diag_7()
    print("7/8 Order Transaction Workflow generated.")
    make_diag_8()
    print("8/8 Component/Class Diagram generated.")
    print("All 8 diagrams generated successfully in PNG and SVG!")
