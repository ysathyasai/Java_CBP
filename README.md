---

<h1 align="center"> 🌱 YieldGrid </h1>
<h3 align="center">Application for Farm-to-Retail Inventory</h3>

<div align="center">

[![Java](https://img.shields.io/badge/Java-17+-orange?style=flat-square&logo=openjdk)](https://www.oracle.com/java/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-blue?style=flat-square&logo=mysql)](https://www.mysql.com/)
[![Swing](https://img.shields.io/badge/GUI-Java%20Swing%20%26%20AWT-green?style=flat-square)](https://docs.oracle.com/javase/tutorial/uiswing/)
[![JDBC](https://img.shields.io/badge/Connectivity-JDBC%20Type--4-informational?style=flat-square)](https://docs.oracle.com/javase/tutorial/jdbc/)
[![Tests](https://img.shields.io/badge/Tests-53%2F53%20Passed-success?style=flat-square)](src/yieldgrid/test/WorkflowVerificationTest.java)
[![Security](https://img.shields.io/badge/Security-PBKDF2%20(HMAC--SHA256)-red?style=flat-square)](src/yieldgrid/util/PasswordUtil.java)
[![Academic Level](https://img.shields.io/badge/Academic%20Level-B.Tech%20CBP%20(OOP%20Java)-purple?style=flat-square)](COURSE_CONCEPT_MAP.md)

[🎯 Overview](#-overview) • [✨ Core Features](#-core-features) • [🛠️ Tech Stack](#️-tech-stack) • [🏗️ Architecture](#️-architecture) • [📁 Project Structure](#-project-structure) • [📦 Setup & Run](#-installation--configuration) • [🚀 Usage Guide](#-usage-guide--role-workflows) • [📚 Syllabus Map](#-course-concept-mapping-syllabus) • [👥 Team](#-project-team)

</div>

---

## 🎯 Overview

**YieldGrid** is a desktop Direct-to-Consumer (D2C) farm-to-retail inventory management application engineered in pure **Java Swing** and backed by a relational **MySQL** database via Type-4 **JDBC**. 

The application establishes a direct, transparent digital bridge between local agricultural producers (**Farmers**) and retail consumers (**Customers**), eliminating exploitative intermediary commissions. Farmers list crop batches, manage inventory levels, process customer orders, and track revenue. Customers browse fresh regional harvests, maintain interactive shopping carts, execute multi-item checkouts, and track live order fulfillment. Platform administrators (**Admins**) supervise user accounts, moderate listings, and monitor platform health.

Developed as an academic Course-Based Project (CBP) for **Object-Oriented Programming through Java (25PC1CS201)**, YieldGrid is structured to be clean, modular, and easy for students to explain during a project review or viva.

> *A transparent, reliable, middleman-free digital marketplace connecting rural producers directly with retail buyers.*

### Key Architecture Guarantees
- 🔒 **Zero Middleman Markups:** Direct transactional link between rural farmers and urban retail buyers.
- ⚡ **Atomic Inventory Integrity:** Database transactions enforce strict ACID consistency (`setAutoCommit(false)`, rollback on shortage).
- 🛡️ **Cryptographic Credential Security:** Salted PBKDF2 password hashing (10,000 iterations, 16-byte random salt) with transparent legacy migration.
- 🎨 **Restrained Desktop GUI:** Custom `UITheme` with Nimbus Look-and-Feel and high-contrast button styling.
- 📚 **Comprehensive Syllabus Grounding:** Full coverage of Units I through V mapped in [COURSE_CONCEPT_MAP.md](COURSE_CONCEPT_MAP.md).

---

## ✨ Core Features

### 🌾 **Farmer Module**
- **Inventory Management (CRUD):**
  - Add crops with botanical name, descriptions, available stock (kg/bunches), and unit price (INR).
  - Modify stock quantities and unit pricing dynamically.
  - Delete listings with multi-tenant ownership verification (farmers cannot modify another farmer's crops).
- **Order Fulfillment:**
  - Review incoming customer purchase orders with itemized breakdowns.
  - Advance order states along the verified lifecycle: `PENDING` ➔ `CONFIRMED` ➔ `COMPLETED` (or `CANCELLED`).
- **Revenue Analytics & Audit Ledger:**
  - Real-time calculation of realized earnings from completed orders.
  - In-memory recursive stock calculation (`InventoryAnalytics.calculateRecursiveStockUnits`).
  - Export order histories and financial ledgers to RFC 4180 compliant CSV files with spreadsheet formula injection protection.
- **Farmer Profile Management:** View registered farm credentials, location, and update account details.

---

### 🛒 **Customer Module**
- **Marketplace Browsing & Search:**
  - Browse live crop listings from all registered local farmers.
  - Real-time case-insensitive keyword filtering by crop name, farmer name, or variety description.
- **Active Shopping Cart:**
  - Add items with numerical quantity selectors (`JSpinner`).
  - Immediate client-side stock availability checks before cart insertion.
  - Real-time recalculation of line-item subtotals and order grand total.
- **Transactional Checkout:**
  - Multi-item checkout grouping cart items by farmer into distinct purchase orders.
  - Atomic stock deductions in MySQL with conditional `WHERE quantity >= ?` checks.
  - Automatic cart clearing upon verified checkout.
- **Order Tracking & History:**
  - Monitor live order statuses across the fulfillment lifecycle.
  - Review previous purchases with date timestamps and item summaries.
- **Customer Profile:** Manage delivery addresses, contact numbers, and change login passwords securely.

---

### 🛡️ **Administrator Module**
- **Central System Governance:** Role-restricted administration console (`AdminDashboard`) accessible only to users with the `ADMIN` role.
- **Live Platform Telemetry:**
  - Aggregate metric cards calculated directly from MySQL: Total Users, Active Farmers, Retail Customers, Produce Catalog Count, Active Listings, and Gross Platform Revenue.
- **User Account Management:**
  - Search and filter all registered platform users in a responsive `JTable`.
  - Toggle account active status (`is_active` flag) to suspend or reactivate accounts.
  - **Last-Admin Safeguard:** Strict validation rule preventing deactivation or demotion of the final remaining active administrator.
- **Produce Catalog Moderation:** Inspect and moderate listings across all farmers, with ability to toggle visibility or delete flagged produce.
- **Orders Oversight:** Global inspection of customer-farmer transactions with line-item detail modal dialogs.
- **Platform Hierarchy Tree:** Visual Swing `JTree` mapping `YieldGrid Platform ➔ Roles ➔ Users ➔ Produce Listings / Orders`.

---

### 👤 **Shared Account Capabilities (All Roles)**
- **Profile Editing Dialog:** In-place modification of full name and contact information with immediate persistence to MySQL.
- **Cryptographic Password Change:** Secure password update modal with current-password verification, new password length checks, and salted PBKDF2 hashing.
- **Session Lifecycle:** Centralized `SessionManager` maintaining in-memory session context, role dispatch, and clean garbage-collection on logout.

---

## 🛠️ Tech Stack

### **Application Framework & Presentation**
| Technology | Purpose | Specification |
|---|---|---|
| **Java SE** | Core programming language | JDK 17 LTS (Compatible with JDK 21 / 26) |
| **Java Swing** | Desktop Graphical User Interface | `JFrame`, `JPanel`, `JTable`, `JTree`, `JSpinner`, `JMenuBar` |
| **Java AWT** | Layout management, fonts, and graphics | `BorderLayout`, `GridBagLayout`, `FlowLayout`, `Color`, `Cursor` |
| **Nimbus / System L&F** | Modern desktop look-and-feel | Enhanced with custom `UITheme` and high-contrast button delegates |

### **Backend & Persistence**
| Technology | Purpose | Specification |
|---|---|---|
| **MySQL Server** | Relational Database Management System | MySQL 8.0+ / 8.4+ / 26.7+ |
| **JDBC Type-4** | Pure Java database connectivity | MySQL Connector/J `9.2.0` (`lib/mysql-connector-j-9.2.0.jar`) |
| **PreparedStatement** | Parameterized SQL execution | Complete protection against SQL injection attacks |
| **ACID Transactions** | Multi-item checkout consistency | `setAutoCommit(false)`, `commit()`, conditional rollback |

### **Security, Utilities & Concurrency**
| Component | Purpose | Details |
|---|---|---|
| **PasswordUtil** | Cryptographic password hashing | PBKDF2 with HMAC-SHA256, 10,000 iterations, 16-byte salt, constant-time compare |
| **DataExporter** | Audit report generation (`java.io`) | `PrintWriter`, `BufferedWriter`, RFC 4180 escaping, formula injection defense (`=`, `+`, `-`, `@`) |
| **InventoryAnalytics** | Algorithmic inventory recursion | Overloaded recursive traversal with explicit base cases and zero index out-of-bounds |
| **MultithreadingDemo** | Academic concurrency example (Unit-III) | Bounded buffer Producer-Consumer (`wait()`/`notifyAll()`, `ThreadGroup`, daemon threads) |

---

## 🏗️ Architecture

YieldGrid strictly implements a decoupled **Three-Tier Architecture**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   PRESENTATION LAYER (Java Swing GUI)                  │
│   LoginFrame • RegisterFrame • FarmerDashboard • CustomerDashboard     │
│   AdminDashboard • CropManagementPanel • CartPanel • OrdersPanel       │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ Method Invocations
┌───────────────────────────────────▼────────────────────────────────────┐
│                    SERVICE LAYER (Business Logic)                      │
│   AuthenticationService • CropService • OrderService • RevenueService  │
│   AdminService • SessionManager • PasswordUtil • DataExporter          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ PreparedStatement Execution
┌───────────────────────────────────▼────────────────────────────────────┐
│                  DATA ACCESS LAYER (DAO / Persistence)                 │
│   UserDAO • CropDAO • OrderDAO • AdminDAO • DBConnection (Singleton)   │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ TCP / Port 3306
┌───────────────────────────────────▼────────────────────────────────────┐
│                   DATABASE LAYER (Relational MySQL)                    │
│   users • crops • orders • order_items  (Third Normal Form - 3NF)      │
└────────────────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities
1. **Presentation Layer (Swing UI):** Renders GUI components, captures user input on the Event Dispatch Thread (EDT), displays validation dialogs, and delegates actions to services.
2. **Service Layer (Business Logic):** Enforces domain validation rules, access control policies, inventory limits, password cryptography, and transaction boundaries.
3. **Data Access Layer (DAOs):** Encapsulates all SQL statements (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) within `PreparedStatement` instances and maps database result sets into domain objects.
4. **Database Layer (MySQL):** Stores relational records in Third Normal Form (3NF) with foreign key constraints (`ON DELETE CASCADE`) enforcing referential integrity.

---

## 📁 Project Structure

```text
YieldGrid/
├── src/
│   └── yieldgrid/
│       ├── main/
│       │   └── Main.java                         # Application entrypoint and GUI bootstrap on EDT
│       ├── model/                                # Domain models & object-oriented hierarchies
│       │   ├── User.java                         # Abstract base class for all human actors
│       │   ├── AdminUser.java                    # Administrator model specializing User
│       │   ├── Farmer.java                       # Agricultural producer model
│       │   ├── Customer.java                     # Retail consumer model
│       │   ├── Crop.java                         # Produce inventory item entity
│       │   ├── CartItem.java                     # Shopping cart line item
│       │   ├── Order.java                        # Purchase order header entity
│       │   ├── OrderItem.java                    # Purchase order line item
│       │   └── OrderStatus.java                  # Java enum: PENDING, CONFIRMED, COMPLETED, CANCELLED
│       ├── interfaces/                           # Behavioral contracts
│       │   ├── DashboardActions.java             # Base dashboard contract with system constants
│       │   └── AdminActions.java                 # Extended interface for administrative operations
│       ├── exception/                            # Custom domain exceptions
│       │   ├── ValidationException.java          # Checked exception for malformed user inputs
│       │   ├── InsufficientStockException.java   # Checked exception for inventory shortages
│       │   └── AuthenticationException.java     # Checked exception for credential verification failures
│       ├── database/
│       │   └── DBConnection.java                 # Singleton connection manager & auto-seeding engine
│       ├── dao/                                  # Data Access Objects (CRUD & JDBC queries)
│       │   ├── UserDAO.java                      # User authentication, registration, and status updates
│       │   ├── CropDAO.java                      # Crop creation, listing, updating, and deletion
│       │   ├── OrderDAO.java                     # Atomic order placement and transaction handling
│       │   └── AdminDAO.java                     # System-wide metrics, moderation, and order audits
│       ├── service/                              # Business logic, authorization, and session state
│       │   ├── AuthenticationService.java        # Login, registration, and profile modification
│       │   ├── CropService.java                  # Produce validation, uniqueness, and ownership guards
│       │   ├── OrderService.java                 # Cart manipulation, stock validation, and checkout
│       │   ├── RevenueService.java               # Farmer sales accumulation and ledger filtering
│       │   ├── AdminService.java                 # Administrator role authorization & safety invariants
│       │   └── SessionManager.java               # In-memory session tracking and active cart storage
│       ├── util/                                 # Syllabus utilities & academic demonstrations
│       │   ├── PasswordUtil.java                 # Salted PBKDF2 password hashing & legacy migration
│       │   ├── DataExporter.java                 # CSV file export with RFC 4180 & formula escaping
│       │   ├── InventoryAnalytics.java           # Recursive stock accumulation (Unit-I recursion)
│       │   └── MultithreadingDemo.java           # Standalone Bounded Buffer Producer-Consumer (Unit-III)
│       ├── ui/                                   # Java Swing presentation components
│       │   ├── UITheme.java                      # Color tokens, fonts, and high-contrast button delegates
│       │   ├── LoginFrame.java                   # User authentication & role-based routing window
│       │   ├── RegisterFrame.java                # Account registration window
│       │   ├── FarmerDashboard.java              # Farmer tabbed workspace frame
│       │   ├── CustomerDashboard.java            # Customer marketplace & orders frame
│       │   ├── AdminDashboard.java               # Django-Admin style administrative console
│       │   ├── CropManagementPanel.java          # Farmer produce inventory management panel
│       │   ├── CropBrowsePanel.java              # Customer marketplace search & browsing panel
│       │   ├── CartPanel.java                    # Customer shopping cart & checkout panel
│       │   ├── OrdersPanel.java                  # Order history, fulfillment & status tracking panel
│       │   ├── RevenuePanel.java                 # Farmer revenue metrics & CSV audit panel
│       │   └── ProfilePanel.java                 # Account profile view, edit details & password modal
│       └── test/
│           └── WorkflowVerificationTest.java     # Automated test suite (53 tests across 15 domains)
├── database/
│   └── yieldgrid.sql                             # DDL schema definition and seed data script
├── lib/
│   └── mysql-connector-j-9.2.0.jar               # Official MySQL JDBC Type-4 Pure Java driver
├── static/
│   └── images/                                   # 15 Authentic application screenshots
├── config.example.properties                     # Database configuration template
├── COURSE_CONCEPT_MAP.md                         # Authoritative syllabus mapping document
├── Implementation.md                             # Academic project specification
├── YieldGrid_CBP_Project_Report.docx             # Complete academic project report (Word format)
├── YieldGrid_CBP_Project_Report.pdf              # Typeset academic project report (42 pages PDF)
├── compile.bat                                   # One-click Windows compilation script
├── run.bat                                       # One-click application launch script
└── .gitignore                                    # Git ignore rules for bin, credentials, and temp files
```

---

## 📋 Prerequisites

Ensure your development environment meets the following requirements:
1. **Java Development Kit (JDK):** Version **17 LTS** or newer (compatible with JDK 21 and JDK 26). Verify via:
   ```powershell
   java -version
   javac -version
   ```
2. **MySQL Server:** Version **8.0+** or **8.4+** running locally on default port `3306`.
3. **JDBC Driver:** Bundled in `lib/mysql-connector-j-9.2.0.jar` (no separate download required).

---

## 📦 Installation & Configuration

### Step 1: Clone the Repository
Open Windows PowerShell and clone the repository:
```powershell
git clone https://github.com/ysathyasai/Java_CBP.git
cd Java_CBP
```

### Step 2: Set Up Database Credentials
Create `config.properties` in the project root by copying `config.example.properties`:
```powershell
Copy-Item config.example.properties config.properties
```
Open `config.properties` and enter your local MySQL password:
```properties
db.url=jdbc:mysql://localhost:3306/yieldgrid
db.username=root
db.password=YOUR_LOCAL_MYSQL_PASSWORD
```
> *Note: `config.properties` is protected by `.gitignore` and is never committed to GitHub.*

### Step 3: Initialize MySQL Database (Optional)
YieldGrid automatically checks and creates missing tables upon startup. However, you can also import `database/yieldgrid.sql` manually via MySQL CLI or Workbench:
```powershell
mysql -u root -p < database/yieldgrid.sql
```

### Step 4: Compile the Application
Compile all source files into the `bin/` directory:
```powershell
.\compile.bat
```
*(Or run `javac` directly:)*
```powershell
javac -encoding UTF-8 -cp "lib/mysql-connector-j-9.2.0.jar" -d bin src\yieldgrid\model\*.java src\yieldgrid\interfaces\*.java src\yieldgrid\exception\*.java src\yieldgrid\database\*.java src\yieldgrid\dao\*.java src\yieldgrid\service\*.java src\yieldgrid\util\*.java src\yieldgrid\ui\*.java src\yieldgrid\main\*.java src\yieldgrid\test\*.java
```

### Step 5: Launch the Application
Run the Swing desktop GUI:
```powershell
.\run.bat
```
*(Or launch directly via Java:)*
```powershell
java -cp "bin;lib/mysql-connector-j-9.2.0.jar" yieldgrid.main.Main
```

### Step 6: Run Automated Verification Tests
Execute the comprehensive 53-assertion verification suite:
```powershell
java -cp "bin;lib/mysql-connector-j-9.2.0.jar" yieldgrid.test.WorkflowVerificationTest
```

### Step 7: Run the Multithreading Demo (Unit-III)
Execute the isolated bounded producer-consumer demonstration:
```powershell
java -cp "bin;lib/mysql-connector-j-9.2.0.jar" yieldgrid.util.MultithreadingDemo
```

---

## 🚀 Usage Guide & Role Workflows

### Default Public Test Accounts
YieldGrid comes pre-seeded with sample test accounts for each role:

| Role | Username | Default Password | Profile Name & Details | Pre-Seeded Context |
|---|---|---|---|---|
| **Admin** | `admin` | `admin123` | System Administrator | Full governance console, 6 KPI cards, user moderation |
| **Farmer** | `farmer1` | `farmer123` | Ramesh Kumar (Green Valley Farms) | Listed crops: Organic Tomato, Russet Potato, Red Onion |
| **Farmer** | `farmer2` | `farmer123` | Suresh Patel (Sunshine Organic) | Listed crops: Fresh Carrot, Organic Spinach, Green Chilli |
| **Customer** | `customer1` | `customer123` | Anita Sharma | Active buyer, Vijayawada delivery address |
| **Customer** | `customer2` | `customer123` | Vikram Reddy | Active buyer, Guntur delivery address |

*(All passwords can be modified via the Profile tab; changes immediately persist in MySQL).*

### 1. Farmer Workflow
1. Select role **Farmer** and log in with `farmer1` / `farmer123`.
2. **Manage Crops Tab:** Add a new produce batch (e.g., "Basmati Rice", 100 kg, Rs. 65/kg). Update existing quantities or toggle sale availability.
3. **Incoming Orders Tab:** Review orders placed by customers. Advance orders from `PENDING` to `CONFIRMED` and `COMPLETED`.
4. **Revenue Analytics Tab:** Inspect total gross earnings and average order values. Export ledger records to CSV.
5. **Profile Tab:** Click **Edit Details** to update phone numbers or farm locations; click **Change Password** to update login credentials.

### 2. Customer Workflow
1. Select role **Customer** and log in with `customer1` / `customer123`.
2. **Browse Produce Tab:** Search available crops using real-time search. Select an item and click **Add to Cart**.
3. **Shopping Cart Tab:** Adjust quantities using the spinner. Click **Proceed to Checkout** to execute an atomic multi-item transaction.
4. **Orders & Tracking Tab:** Track the order through fulfillment stages and review items purchased.
5. **Profile Tab:** Update shipping and contact information.

### 3. Administrator Workflow
1. Select role **Admin** and log in with `admin` / `admin123`.
2. **System Overview Tab:** Inspect platform health across 6 real-time KPI metrics cards.
3. **User Accounts Tab:** Search users, modify user roles, or toggle account status (`is_active`). Test the Last-Admin safeguard by attempting to deactivate the sole administrator.
4. **Produce Catalog Tab:** Moderate crops across all farmers globally.
5. **Orders Oversight Tab:** Inspect all purchase transactions across all users.
6. **Platform Hierarchy Tab:** Navigate the interactive `JTree` showing organizational links between roles, users, crops, and orders.

---

## 🗄️ Database & Schema Management

YieldGrid uses a normalized 4-table relational schema designed in **Third Normal Form (3NF)**:

```
  ┌───────────────────────┐              ┌──────────────────────────┐
  │         users         │              │          crops           │
  ├───────────────────────┤              ├──────────────────────────┤
  │ PK  user_id           │◄────────────┼│ FK  farmer_id            │
  │     name              │              │ PK  crop_id              │
  │     username (UNIQUE) │              │     crop_name            │
  │     password (PBKDF2) │              │     quantity, price      │
  │     role, is_active   │              │     available, created_at│
  └───────────┬───────────┘              └─────────────┬────────────┘
              │ 1:N (Places)                           │ 1:N (Referenced in)
              ▼                                        ▼
  ┌───────────────────────┐              ┌──────────────────────────┐
  │        orders         │ 1:N          │       order_items        │
  ├───────────────────────┤ (Contains)   ├──────────────────────────┤
  │ PK  order_id          ├─────────────►│ PK  order_item_id        │
  │ FK  customer_id       │              │ FK  order_id             │
  │ FK  farmer_id         │              │ FK  crop_id              │
  │     total_amount      │              │     quantity, unit_price │
  │     status, order_date│              │     subtotal             │
  └───────────────────────┘              └──────────────────────────┘
```

### Table Definitions
- **`users`:** Stores account credentials, roles (`ADMIN`, `FARMER`, `CUSTOMER`), active status flags, and contact details.
- **`crops`:** Stores produce listings with quantities, pricing, and foreign keys referencing the owning farmer (`users.user_id`).
- **`orders`:** Header records capturing transaction totals, order timestamps, fulfillment status, customer IDs, and farmer IDs.
- **`order_items`:** Line items capturing the exact quantity, historical unit price, and subtotal at the moment of purchase.

### Transactional Guarantees (ACID)
During checkout, `OrderDAO.placeOrder()` manages the connection explicitly:
1. `conn.setAutoCommit(false);` begins the transaction block.
2. Order headers and line items are inserted via batch prepared statements.
3. Inventory units are decremented using conditional atomic SQL:
   ```sql
   UPDATE crops SET quantity = quantity - ? WHERE crop_id = ? AND quantity >= ?;
   ```
4. If affected rows equal zero (stock exhausted by concurrent order), a `SQLException` / `InsufficientStockException` is thrown, triggering `conn.rollback()`.
5. Upon successful execution of all updates, `conn.commit()` finalizes changes and restores auto-commit mode.

---

## 📚 Course Concept Mapping (Syllabus)

The project comprehensively satisfies the curriculum of **Object Oriented Programming through Java (25PC1CS201)** across all five units. Detailed line-by-line references are documented in [COURSE_CONCEPT_MAP.md](COURSE_CONCEPT_MAP.md).

| Syllabus Unit | Key Pedagogical Concepts | Primary Implementation Files | Verification Status |
|---|---|---|---|
| **UNIT-I** | OOP Paradigm, Encapsulation, Constructors, `this`, Overloading, Recursion, Strings, Type Wrappers | `User.java`, `Crop.java`, `CartItem.java`, `InventoryAnalytics.java` | **Verified (100%)** |
| **UNIT-II** | Inheritance (`User` hierarchy), Polymorphism, Abstract Classes, Interfaces (`DashboardActions`, `AdminActions`), Packages, Generics | `Farmer.java`, `Customer.java`, `AdminUser.java`, `DashboardActions.java`, `AdminActions.java` | **Verified (100%)** |
| **UNIT-III** | Exception Hierarchy, Checked Exceptions, `try-with-resources`, Multithreading (`Runnable`, `Thread`, `wait`/`notifyAll`) | `ValidationException.java`, `InsufficientStockException.java`, `MultithreadingDemo.java` | **Verified (100%)** |
| **UNIT-IV** | Collections Framework (`List`, `Set`, `TreeSet`, `Map`), File I/O (`java.io` CSV export), Event Delegation, Layout Managers | `DataExporter.java`, `AdminDAO.java`, `CropService.java`, Swing Panels | **Verified (100%)** |
| **UNIT-V** | Swing GUI (`JTable`, `JTree`, `JSpinner`, `JMenuBar`, `JPopupMenu`), MVC Separation, Type-4 JDBC, ACID Transactions | `Main.java`, `LoginFrame.java`, `AdminDashboard.java`, `DBConnection.java`, `OrderDAO.java` | **Verified (100%)** |

---

## 🧪 Testing & Verification

The automated verification suite (`WorkflowVerificationTest.java`) validates all business logic, security algorithms, and database workflows across 15 focused domains.

```powershell
java -cp "bin;lib/mysql-connector-j-9.2.0.jar" yieldgrid.test.WorkflowVerificationTest
```

### Test Suite Execution Results (53 / 53 Passed)
```text
==================================================
YieldGrid — Course Concept & Workflow Verification
==================================================

--- 1. Testing Encapsulation & Models ---
  [PASS] Encapsulated getters return initialized state
  [PASS] Encapsulated setter updates field properly

--- 2. Testing Inheritance & Polymorphism ---
  [PASS] Subclasses inherit from abstract User base class
  [PASS] Polymorphic role descriptions dispatched correctly
  [PASS] Overridden equals() identifies same entity by ID and username
  [PASS] Overridden hashCode() is consistent with equals()

--- 3. Testing Interfaces & Extending Interfaces ---
  [PASS] Interface constant APPLICATION_NAME is accessible
  [PASS] Extending interfaces: AdminActions extends DashboardActions

--- 4. Testing Java Enum (OrderStatus) ---
  [PASS] Enum initial state and parser work accurately

--- 5. Testing Object Interaction & Cart ---
  [PASS] CartItem interacts with Crop to compute subtotal (30*5=150)
  [PASS] Cart tracks item addition
  [PASS] Cart clears successfully

--- 6. Testing Arithmetic & Composition ---
  [PASS] Order composition and total calculation (120+100=220)

--- 7. Testing String Handling & Searching ---
  [PASS] Case-insensitive substring search works

--- 8. Testing Validation & Custom Exceptions ---
  [PASS] ValidationException thrown for empty credentials
  [PASS] InsufficientStockException thrown when requesting beyond available stock

--- 9. Testing Access Control Rules ---
  [PASS] Cross-farmer modification blocked by access control

--- 10. Testing Password Hashing & Security ---
  [PASS] PBKDF2 hash formatted correctly with prefix
  [PASS] Random salt generates distinct hashes for identical passwords
  [PASS] Password verification succeeds for correct password
  [PASS] Password verification rejects invalid password
  [PASS] Legacy SHA-256 hash verified for backward compatibility
  [PASS] PasswordUtil detects legacy hash requires migration
  [PASS] PasswordUtil detects PBKDF2 hash does not require migration
  [PASS] PasswordUtil identifies hashed strings

--- 11. Testing Recursion & Method Overloading ---
  [PASS] Recursion accumulates inventory units accurately (50+30+20=100)
  [PASS] Recursion base cases: null and out-of-bounds return 0

--- 12. Testing Collections Framework ---
  [PASS] List allows duplicate elements
  [PASS] Set eliminates duplicate elements
  [PASS] TreeSet sorts elements natural ordering
  [PASS] Map stores and retrieves key-value entries

--- 13. Testing File I/O (CSV Export, Escaping & Reading) ---
  [PASS] CSV file created and exists on disk
  [PASS] BufferedReader read expected CSV lines (1 header + 2 records = 3)
  [PASS] Formula injection neutralized with leading quote
  [PASS] Internal quotes escaped per RFC 4180

--- 14. Testing Multithreading & Synchronization ---
  [PASS] Multithreading bounded producer-consumer processes all 3 items safely

--- 15. Testing Live Database Workflows & Transactions ---
  [PASS] Live MySQL connection successfully established
  [PASS] Admin authenticated successfully
  [PASS] AdminService grants access to authenticated AdminUser
  [PASS] AdminService blocks non-admin user
  [PASS] System metrics retrieved from database
  [PASS] Profile updated via authService
  [PASS] Updated profile persistently saved in MySQL
  [PASS] New user registered in database
  [PASS] Duplicate username rejected with ValidationException
  [PASS] Admin deactivates non-admin account
  [PASS] Deactivated account blocked from logging in
  [PASS] Safety safeguard prevents deactivating the last active administrator
  [PASS] Produce catalog loaded from database
  [PASS] Order placed via atomic transaction
  [PASS] Inventory quantity decremented safely in MySQL
  [PASS] Farmer revenue calculated successfully
  [PASS] Test data cleanly isolated and cleaned up from MySQL
==================================================
TEST SUMMARY:
Tests Passed: 53
Tests Failed: 0
==================================================
```

---

## 🔐 Security & Data Integrity

- **Password Cryptography:** Implements salted PBKDF2 with HMAC-SHA256 (`PBKDF2WithHmacSHA256`), 10,000 iterations, and a cryptographically secure 16-byte salt (`java.security.SecureRandom`). Backward-compatible legacy migration upgrades legacy passwords to salted PBKDF2 upon next successful login.
- **SQL Injection Prevention:** 100% of database operations use `PreparedStatement` with typed parameter binding (`setString`, `setInt`, `setDouble`, `setBoolean`). No dynamic string concatenation in SQL queries.
- **CSV Formula Injection Mitigation (CWE-1236):** `DataExporter.escapeCsvField()` prepends a single quotation mark (`'`) to any field starting with `=`, `+`, `-`, `@`, `\t`, or `\r`, preventing code execution when reports are opened in spreadsheet applications.
- **Zero Hardcoded Credentials:** Database credentials reside in `config.properties`, which is excluded from version control via `.gitignore`. A clean template is provided in `config.example.properties`.

---

## ⚠️ Known Limitations & Future Scope

### Current Academic Boundaries
- **Desktop Architecture:** Engineered as a native Java desktop GUI application. Cross-device multi-client operations require a centralized MySQL server on the local network.
- **Simulated Payment Settlement:** Orders transition financially upon confirmed delivery records; direct UPI or banking gateway APIs are not integrated.
- **Discrete Transit Tracking:** Deliveries update through status stages (`PENDING` ➔ `CONFIRMED` ➔ `COMPLETED`) rather than live GPS telematics.

### Future Enhancements
- 📱 **Mobile Companion App:** Developing Flutter/Android companion apps communicating with RESTful endpoints.
- 💳 **Digital Escrow Gateway:** Integrating Razorpay/UPI webhooks for instant escrow release upon customer-verified delivery.
- 🤖 **Predictive Harvest Pricing:** Machine learning models forecasting seasonal crop demand and optimal market pricing.

---

## 👥 Project Team

This project was developed by the following student team as a Course-Based Project (CBP):

| Name | Roll Number | Role | GitHub Profile |
|---|---|---|---|
| **Pervala Yashwanth** | `26075A6610` | Full-Stack Java Development & Database Architecture | — |
| **Yejju Sathyasai** | `26075A6613` | Architecture, Security, GUI Development & Documentation | [@ysathyasai](https://github.com/ysathyasai) |
| **Shaik Abdul Rasheed** | `26075A6612` | UI/UX Swing Engineering, QA & Verification Testing | — |

### Academic Guidance & Institution
- **Project Supervisor:** **Ms. K. Anitha**, Assistant Professor, Dept. of CSE (AI & ML) & IoT and R&AI
- **Head of Department:** **Dr. Sagar Yeruva**, Assoc. Professor & HOD
- **Institution:** **Vallurupalli Nageswara Rao Institute of Engineering and Technology (VNR VJIET)**, Hyderabad, India

---

## 📄 Documentation Links & Acknowledgements

- 📖 **Project Report (PDF, 42 Pages):** [YieldGrid_CBP_Project_Report.pdf](YieldGrid_CBP_Project_Report.pdf)
- 📝 **Project Report (Word DOCX):** [YieldGrid_CBP_Project_Report.docx](YieldGrid_CBP_Project_Report.docx)
- 🗺️ **Complete Course Concept Map (108 Topics):** [COURSE_CONCEPT_MAP.md](COURSE_CONCEPT_MAP.md)
- 📋 **Master Implementation Guide:** [Implementation.md](Implementation.md)
- 🗄️ **Database Schema & Seed Script:** [database/yieldgrid.sql](database/yieldgrid.sql)
- 📸 **Application Screenshots:** [static/images/](static/images/)

---

<div align="center">

**YieldGrid — Course-Based Project (CBP) • Object-Oriented Programming through Java**  
*Department of Computer Science & Engineering (AI & ML) • VNR VJIET, Hyderabad*

</div>
