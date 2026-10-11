import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('documentation_assets/screenshots', exist_ok=True)

placeholders = [
    ("login_screen.png", "FIGURE 8.1 — LOGIN AND AUTHENTICATION SCREEN", "LoginFrame GUI: Username & Password with Role-Based Routing", "login_screen.png"),
    ("register_screen.png", "FIGURE 8.2 — USER REGISTRATION SCREEN", "RegisterFrame GUI: Customer & Farmer Account Creation", "register_screen.png"),
    ("farmer_dashboard.png", "FIGURE 8.3 — FARMER DASHBOARD WORKSPACE", "FarmerDashboard GUI: Produce, Orders, Revenue & Profile Navigation", "farmer_dashboard.png"),
    ("crop_management.png", "FIGURE 8.4 — CROP INVENTORY MANAGEMENT PANEL", "CropManagementPanel GUI: Produce Listing Form & Interactive JTable", "crop_management.png"),
    ("incoming_orders.png", "FIGURE 8.5 — FARMER INCOMING ORDERS FULFILLMENT", "OrdersPanel (Farmer View): Order Details & Status Transition Controls", "incoming_orders.png"),
    ("revenue_dashboard.png", "FIGURE 8.6 — FARMER REVENUE & SALES LEDGER", "RevenuePanel GUI: Realized Revenue Calculation & Sales History", "revenue_dashboard.png"),
    ("customer_marketplace.png", "FIGURE 8.7 — CUSTOMER PRODUCE MARKETPLACE", "CropBrowsePanel GUI: Search, Live Filtering & Quantity Selection", "customer_marketplace.png"),
    ("shopping_cart.png", "FIGURE 8.8 — CUSTOMER SHOPPING CART PANEL", "CartPanel GUI: Cart Table, Dynamic Totals & Atomic Checkout", "shopping_cart.png"),
    ("customer_order_tracking.png", "FIGURE 8.9 — CUSTOMER ORDER HISTORY & TRACKING", "OrdersPanel (Customer View): Real-Time Status Tracking & Line Items", "customer_order_tracking.png"),
    ("profile_editing.png", "FIGURE 8.10 — USER PROFILE EDITING & PERSISTENCE", "ProfilePanel GUI: Edit Details & Password Modification Dialogs", "profile_editing.png"),
    ("admin_dashboard.png", "FIGURE 8.11 — ADMINISTRATOR PLATFORM OVERVIEW", "AdminDashboard GUI: Real-Time Platform Metrics & JMenuBar", "admin_dashboard.png"),
    ("admin_user_management.png", "FIGURE 8.12 — ADMIN USER & PRODUCE MANAGEMENT", "AdminDashboard GUI: Account Roster, Produce Oversight & JTree Hierarchy", "admin_user_management.png"),
]

def make_placeholder(filename, fig_title, subtitle, target_file):
    w, h = 900, 500
    img = Image.new('RGB', (w, h), color='#F8FAFC')
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([10, 10, w - 10, h - 10], outline='#1E3A8A', width=3)
    # Inner border
    draw.rectangle([16, 16, w - 16, h - 16], outline='#94A3B8', width=1)

    # Header bar
    draw.rectangle([18, 18, w - 18, 75], fill='#1E3A8A')
    
    # Text
    # Title
    draw.text((w // 2, 46), fig_title, fill='#FFFFFF', anchor='mm', font=None)
    
    # Box center message
    center_y = h // 2
    draw.rectangle([80, center_y - 80, w - 80, center_y + 80], fill='#EFF6FF', outline='#3B82F6', width=2)
    
    draw.text((w // 2, center_y - 45), f"[ INSERT ACTUAL YIELDGRID SCREENSHOT HERE ]", fill='#1E3A8A', anchor='mm', font=None)
    draw.text((w // 2, center_y - 15), subtitle, fill='#334155', anchor='mm', font=None)
    draw.text((w // 2, center_y + 15), f"Target Filename: documentation_assets/screenshots/{target_file}", fill='#0F766E', anchor='mm', font=None)
    draw.text((w // 2, center_y + 45), "Live capture unavailable in non-interactive agent session. See SCREENSHOT_INSERTION_GUIDE.md", fill='#64748B', anchor='mm', font=None)

    # Footer banner
    draw.rectangle([18, h - 55, w - 18, h - 18], fill='#F1F5F9')
    draw.text((w // 2, h - 36), "YieldGrid — Application for Farm-to-Retail Inventory (B.Tech Course-Based Project)", fill='#475569', anchor='mm', font=None)

    filepath = os.path.join('documentation_assets/screenshots', filename)
    img.save(filepath, format='PNG')
    print(f"Generated placeholder: {filepath}")

for p in placeholders:
    make_placeholder(p[0], p[1], p[2], p[3])

print("All 12 screenshot placeholders created successfully!")
