# YieldGrid — Application Screenshot Insertion Guide

This guide provides step-by-step instructions for capturing and replacing each application screenshot in the YieldGrid project report (`YieldGrid_CBP_Project_Report.docx` and `YieldGrid_CBP_Project_Report.pdf`).

## Reason for Placeholders in Automated Build
During autonomous report compilation, the agent operates in a non-interactive Windows service process environment (Session 0). In this headless context:
- Windows GDI API `CopyFromScreen` returns `Exception: The handle is invalid` because no active interactive desktop surface (`WinSta0\Default`) is bound to the process.
- Python `PIL.ImageGrab.grab()` raises `OSError: screen grab failed`.
- Per the user guidelines, clean, bordered placeholders are generated with exact figure numbering, aspect ratios, and reserved dimensions so the report formatting remains strictly submission-ready and stable.

To replace any placeholder with a genuine desktop capture, follow the detailed instructions below.

---

## Screenshot Inventory & Step-by-Step Capture Instructions

| Figure & Caption | Expected Filename | Report Section | Required Role | Screen to Open & Action Steps | Recommended Size / Aspect |
|---|---|---|---|---|---|
| **Figure 8.1:** Login and Authentication Screen | `login_screen.png` | Chapter 8: Testing & GUI | Any / Unauthenticated | Launch application via `run.bat` or `java -cp "bin;lib/*" yieldgrid.main.Main`. Capture initial `LoginFrame` window. | 900x500 (16:9) |
| **Figure 8.2:** User Registration Screen | `register_screen.png` | Chapter 8: Testing & GUI | New User | On `LoginFrame`, click **Register**. Capture the `RegisterFrame` form with role selector dropdown. | 900x500 (16:9) |
| **Figure 8.3:** Farmer Dashboard Workspace | `farmer_dashboard.png` | Chapter 8: Testing & GUI | Farmer (`farmer1` / `farmer123`) | Log in as `farmer1`. Capture the main `FarmerDashboard` landing window showing the welcome banner, navigation tabs, and header. | 900x500 (16:9) |
| **Figure 8.4:** Crop Inventory Management Panel | `crop_management.png` | Chapter 8: Testing & GUI | Farmer (`farmer1` / `farmer123`) | In `FarmerDashboard`, click the **Crops Management** tab. Capture the produce creation form, input fields, and the populated `JTable` of crops. | 900x500 (16:9) |
| **Figure 8.5:** Farmer Incoming Orders Fulfillment | `incoming_orders.png` | Chapter 8: Testing & GUI | Farmer (`farmer1` / `farmer123`) | In `FarmerDashboard`, click the **Orders** tab. Capture incoming purchase orders, line items breakdown, and order status buttons. | 900x500 (16:9) |
| **Figure 8.6:** Farmer Revenue & Sales Ledger | `revenue_dashboard.png` | Chapter 8: Testing & GUI | Farmer (`farmer1` / `farmer123`) | In `FarmerDashboard`, click the **Revenue** tab. Capture the realized revenue card, total sales amount, and order ledger table. | 900x500 (16:9) |
| **Figure 8.7:** Customer Produce Marketplace | `customer_marketplace.png` | Chapter 8: Testing & GUI | Customer (`customer1` / `customer123`) | Log in as `customer1`. Capture the **Browse Produce** tab with active search bar, farmer listings, unit prices, and quantity spinners. | 900x500 (16:9) |
| **Figure 8.8:** Customer Shopping Cart Panel | `shopping_cart.png` | Chapter 8: Testing & GUI | Customer (`customer1` / `customer123`) | Add items to cart and navigate to the **Cart** tab. Capture the itemized cart table, subtotal calculations, and the **Checkout** button. | 900x500 (16:9) |
| **Figure 8.9:** Customer Order History & Tracking | `customer_order_tracking.png` | Chapter 8: Testing & GUI | Customer (`customer1` / `customer123`) | In `CustomerDashboard`, click the **My Orders** tab. Capture placed orders showing real-time `OrderStatus` (PENDING, CONFIRMED, COMPLETED). | 900x500 (16:9) |
| **Figure 8.10:** User Profile Editing & Persistence | `profile_editing.png` | Chapter 8: Testing & GUI | Any logged-in user | Click the **Profile** tab on any dashboard, then click **Edit Details**. Capture the modal dialog showing name and contact modification. | 900x500 (16:9) |
| **Figure 8.11:** Administrator Platform Overview | `admin_dashboard.png` | Chapter 8: Testing & GUI | Admin (`admin` / `admin123`) | Log in as `admin`. Capture `AdminDashboard` showing the platform metric cards (Total Users, Farmers, Crops, GMV) and top `JMenuBar`. | 900x500 (16:9) |
| **Figure 8.12:** Admin User & Produce Management | `admin_user_management.png` | Chapter 8: Testing & GUI | Admin (`admin` / `admin123`) | In `AdminDashboard`, click the **Users** tab. Capture user roster `JTable`, active search field, role filters, and right-click context menu. | 900x500 (16:9) |

---

## Replacement Workflow
1. Launch the interactive application by running `run.bat` on your Windows desktop.
2. Navigate to the desired screen using the demo credentials listed above.
3. Use Windows Snipping Tool (`Win + Shift + S`) or Alt+PrtScn to capture the active window.
4. Save the screenshot with the exact filename into `documentation_assets/screenshots/<filename>.png`.
5. Re-run the documentation generator script `generate_report.py` to automatically embed your genuine screenshots and regenerate the final submission DOCX and PDF.
