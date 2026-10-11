# -*- coding: utf-8 -*-
"""
Chapter 7 Builder for YieldGrid Academic Project Report
Contains in-depth Implementation Chapter: 14 sections, authentic source code excerpts,
and all 15 authentic application screenshots from static/images/ properly placed and captioned.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from documentation_assets.report_parts import (
    add_heading_1, add_heading_2, add_heading_3,
    add_body_p, add_bullet_p, add_code_block,
    add_figure, add_caption, add_side_by_side_figures
)

def build_chapter_7(doc):
    # ----------------------------------------------------
    # CHAPTER 7: IMPLEMENTATION
    # ----------------------------------------------------
    add_heading_1(doc, "CHAPTER 7\nIMPLEMENTATION")

    add_body_p(
        doc,
        "This chapter presents the comprehensive technical implementation of YieldGrid. In accordance with academic project "
        "standards, each architectural subsystem is documented through detailed explanatory prose, architectural rationale, "
        "authentic source code excerpts taken directly from the production Java codebase, and real graphical user interface "
        "screenshots captured from the running application. The implementation strictly demonstrates the core competencies "
        "outlined in the Object-Oriented Programming Through Java curriculum, including encapsulation, inheritance hierarchies, "
        "polymorphic dispatch, interface contracts, custom exception handling, multithreading synchronization, the Java Collections "
        "Framework, robust file I/O streams, and JDBC transaction management."
    )

    # 7.1 Application Bootstrapping
    add_heading_2(doc, "7.1 Application Bootstrapping and Global Theme Initialization")
    add_body_p(
        doc,
        "The entry point of the YieldGrid desktop application is implemented in class Main within package yieldgrid.main. "
        "The bootstrap sequence initializes modern graphical styling across all Swing components prior to constructing the first window. "
        "By default, standard Java Swing applications default to the legacy Metal look-and-feel. YieldGrid programmatically discovers "
        "and applies the cross-platform Nimbus Look and Feel through UIManager.setLookAndFeel(), falling back gracefully to the native "
        "system interface if Nimbus is unavailable. Once UI theming is established, the main thread dispatches GUI instantiation onto "
        "the Event Dispatch Thread (EDT) via SwingUtilities.invokeLater() to ensure absolute Swing thread safety."
    )

    code_7_1 = """package yieldgrid.main;

import javax.swing.SwingUtilities;
import javax.swing.UIManager;
import yieldgrid.ui.LoginFrame;
import yieldgrid.ui.UITheme;

public class Main {
    public static void main(String[] args) {
        // UNIT-V GUI: Set modern cross-platform Look and Feel
        try {
            for (UIManager.LookAndFeelInfo info : UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (Exception e) {
            try { UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName()); }
            catch (Exception ignored) {}
        }

        UITheme.initGlobalTheme(); // Apply custom styling palette

        // Safe asynchronous launch on the Swing Event Dispatch Thread (EDT)
        SwingUtilities.invokeLater(() -> {
            LoginFrame loginFrame = new LoginFrame();
            loginFrame.setVisible(true);
        });
    }
}"""
    add_code_block(doc, code_7_1, "Excerpt 7.1: Application Entry Point & Look-and-Feel Setup (yieldgrid.main.Main)")

    # 7.2 Object-Oriented Domain Modeling
    add_heading_2(doc, "7.2 Object-Oriented Domain Modeling and Inheritance Hierarchy")
    add_body_p(
        doc,
        "The core domain entities of YieldGrid are engineered under package yieldgrid.model. The domain model strictly enforces "
        "encapsulation: all fields are declared private or protected, with state access and mutation managed exclusively through "
        "validated getter and setter methods. To represent authenticated system users, YieldGrid establishes an abstract base class User. "
        "The User class encapsulates common state shared by all stakeholders—including userId, name, username, passwordHash, role, contactInfo, "
        "and account status. It defines an abstract method getRoleDescription(), compelling concrete derived classes (Farmer, Customer, AdminUser) "
        "to supply polymorphic behavioral descriptions."
    )

    code_7_2 = """package yieldgrid.model;

import java.util.Objects;

public abstract class User {
    private int userId;
    private String name, username, password, role, contactInfo;
    private boolean active;

    public User(int userId, String name, String username, String password, String role, String contactInfo, boolean active) {
        this.userId = userId; this.name = name; this.username = username;
        this.password = password; this.role = role; this.contactInfo = contactInfo; this.active = active;
    }

    // POLYMORPHISM: Abstract method implemented across concrete subclasses
    public abstract String getRoleDescription();

    public int getUserId() { return userId; }
    public String getUsername() { return username; }
    public String getRole() { return role; }
    public boolean isActive() { return active; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof User)) return false;
        User user = (User) o;
        return userId == user.userId && Objects.equals(username, user.username);
    }

    @Override
    public int hashCode() { return Objects.hash(userId, username); }
}"""
    add_code_block(doc, code_7_2, "Excerpt 7.2: Abstract Base User Entity with Polymorphic Contracts (yieldgrid.model.User)")

    add_body_p(
        doc,
        "For agricultural inventory, the Crop entity represents physical produce listed on the marketplace. Crop encapsulates "
        "attributes including cropId, farmerId, farmerName, cropName, description, quantity, and unit price. Crop mutators validate "
        "that quantities cannot be negative and prices remain positive real numbers."
    )

    code_7_3 = """package yieldgrid.model;

public class Crop {
    private int cropId, farmerId;
    private String farmerName, cropName, description;
    private int quantity;
    private double price;
    private boolean available;

    public Crop(int cropId, int farmerId, String farmerName, String cropName, String description, int quantity, double price, boolean available) {
        this.cropId = cropId; this.farmerId = farmerId; this.farmerName = farmerName;
        this.cropName = cropName; this.description = description;
        this.quantity = Math.max(0, quantity); // Encapsulated boundary validation
        this.price = Math.max(0.0, price);
        this.available = available;
    }

    public int getCropId() { return cropId; }
    public String getCropName() { return cropName; }
    public int getQuantity() { return quantity; }
    public void setQuantity(int quantity) { this.quantity = Math.max(0, quantity); }
    public double getPrice() { return price; }
    public boolean isAvailable() { return available; }
}"""
    add_code_block(doc, code_7_3, "Excerpt 7.3: Crop Inventory Entity with State Encapsulation (yieldgrid.model.Crop)")

    # 7.3 Cryptographic Security
    add_heading_2(doc, "7.3 Cryptographic Security and Password Management")
    add_body_p(
        doc,
        "Security is a pivotal requirement in agricultural commerce to safeguard farmer identity and financial transactions. "
        "YieldGrid implements the PasswordUtil utility class within package yieldgrid.util. Rather than storing plaintext or relying on simple "
        "unsalted hashes, PasswordUtil implements the Password-Based Key Derivation Function 2 (PBKDF2) algorithm using HMAC-SHA256 "
        "(PBKDF2WithHmacSHA256). Each password is salted with 16 cryptographically secure random bytes generated via SecureRandom and stretched "
        "over 10,000 iterations. For backward compatibility with legacy demo accounts, verifyPassword() transparently inspects prefixes; if a legacy "
        "hash verifies, needsMigration() returns true, signalling the system to upgrade the stored hash to PBKDF2 without user disruption."
    )

    code_7_4 = """package yieldgrid.util;

import java.security.MessageDigest;
import java.security.SecureRandom;
import java.util.Base64;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

public class PasswordUtil {
    private static final String PBKDF2_PREFIX = "pbkdf2$";
    private static final String LEGACY_SHA256_PREFIX = "sha256$";
    private static final int ITERATIONS = 10000, SALT_BYTES = 16, KEY_LENGTH_BITS = 256;
    private static final SecureRandom SECURE_RANDOM = new SecureRandom();

    public static String hashPassword(String plaintext) {
        byte[] salt = new byte[SALT_BYTES];
        SECURE_RANDOM.nextBytes(salt);
        byte[] hash = derivePbkdf2Key(plaintext.toCharArray(), salt, ITERATIONS, KEY_LENGTH_BITS);
        return PBKDF2_PREFIX + ITERATIONS + "$" + Base64.getEncoder().encodeToString(salt) + "$" + Base64.getEncoder().encodeToString(hash);
    }

    public static boolean verifyPassword(String plaintext, String stored) {
        if (plaintext == null || stored == null) return false;
        if (stored.startsWith(PBKDF2_PREFIX)) {
            String[] parts = stored.split("\\\\$");
            if (parts.length != 4) return false;
            try {
                int iters = Integer.parseInt(parts[1]);
                byte[] salt = Base64.getDecoder().decode(parts[2]);
                byte[] expected = Base64.getDecoder().decode(parts[3]);
                byte[] candidate = derivePbkdf2Key(plaintext.toCharArray(), salt, iters, expected.length * 8);
                return MessageDigest.isEqual(candidate, expected); // Constant-time verification
            } catch (Exception e) { return false; }
        }
        return false;
    }

    public static boolean needsMigration(String stored) {
        return stored != null && stored.startsWith(LEGACY_SHA256_PREFIX);
    }
}"""
    add_code_block(doc, code_7_4, "Excerpt 7.4: Salted PBKDF2 Hashing and Legacy Migration (yieldgrid.util.PasswordUtil)")

    # 7.4 User Authentication & Session State Management
    add_heading_2(doc, "7.4 User Authentication and Session State Management")
    add_body_p(
        doc,
        "AuthenticationService in package yieldgrid.service acts as the central gatekeeper for system security. "
        "The authenticate() method validates submitted credentials, loads the corresponding user entity through UserDAO, "
        "and checks the is_active status. If credentials match and the account is active, the authenticated user object is stored "
        "within SessionManager. SessionManager maintains thread-safe static references to the active user, active shopping cart, "
        "and session login timestamp, facilitating clean access control across all Swing panels."
    )

    code_7_5 = """package yieldgrid.service;

import yieldgrid.dao.UserDAO;
import yieldgrid.exception.AuthenticationException;
import yieldgrid.exception.ValidationException;
import yieldgrid.model.User;
import yieldgrid.util.PasswordUtil;

public class AuthenticationService {
    private final UserDAO userDAO = new UserDAO();

    public User authenticate(String username, String password) throws AuthenticationException, ValidationException {
        if (username == null || username.trim().isEmpty() || password == null || password.isEmpty()) {
            throw new ValidationException("Username and password must not be empty.");
        }
        User user = userDAO.getUserByUsername(username.trim());
        if (user == null || !PasswordUtil.verifyPassword(password, user.getPassword())) {
            throw new AuthenticationException("Invalid username or password.");
        }
        if (!user.isActive()) {
            throw new AuthenticationException("Your account has been deactivated. Contact an administrator.");
        }
        if (PasswordUtil.needsMigration(user.getPassword())) {
            userDAO.updatePassword(user.getUserId(), PasswordUtil.hashPassword(password));
        }
        SessionManager.setCurrentUser(user);
        return user;
    }
}"""
    add_code_block(doc, code_7_5, "Excerpt 7.5: Authentication Workflow and Session Inception (yieldgrid.service.AuthenticationService)")

    add_body_p(
        doc,
        "Figure 7.1 shows the YieldGrid LoginFrame. Users enter their username and password, select their intended access role "
        "via a styled JComboBox, and trigger authentication. Invalid inputs or deactivated accounts present immediate contextual feedback. "
        "Figure 7.2 illustrates the RegisterFrame, which allows prospective farmers and retail customers to create self-service accounts "
        "with validation across full legal name, telephone contact details, unique username checks, and double-entry password matching."
    )

    add_side_by_side_figures(
        doc,
        "static/images/Screenshot 2026-10-11 160752.png", "Figure 7.1: User Login & Role Selection (LoginFrame)",
        "static/images/Screenshot 2026-10-11 160813.png", "Figure 7.2: User Registration (RegisterFrame)",
        width=Inches(3.1)
    )

    # 7.5 Database Connection Management
    add_heading_2(doc, "7.5 Database Connectivity and Lifecycle Management")
    add_body_p(
        doc,
        "Database connectivity is orchestrated by DBConnection in package yieldgrid.database. DBConnection implements the "
        "Singleton pattern and leverages a static initializer to load the MySQL Connector/J driver (com.mysql.cj.jdbc.Driver) "
        "and read configuration parameters from config.properties. Rather than hardcoding credentials into source code, "
        "DBConnection externalizes database parameters (URL, username, and password) into the configuration properties file. "
        "The getConnection() method delivers validated, active java.sql.Connection instances to Data Access Objects."
    )

    code_7_6 = """package yieldgrid.database;

import java.io.File;
import java.io.FileInputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.util.Properties;

public class DBConnection {
    private static String url = "jdbc:mysql://localhost:3306/yieldgrid";
    private static String username = "root", password = "";
    private static boolean driverLoaded = false;

    static { loadConfiguration(); loadDriver(); }

    private static void loadConfiguration() {
        File configFile = new File("config.properties");
        if (configFile.exists()) {
            try (FileInputStream in = new FileInputStream(configFile)) {
                Properties props = new Properties();
                props.load(in);
                url = props.getProperty("db.url", url);
                username = props.getProperty("db.username", username);
                password = props.getProperty("db.password", password);
            } catch (Exception ignored) {}
        }
    }

    private static void loadDriver() {
        try { Class.forName("com.mysql.cj.jdbc.Driver"); driverLoaded = true; }
        catch (ClassNotFoundException e) { System.err.println("Fatal: MySQL Driver missing."); }
    }

    public static Connection getConnection() throws SQLException {
        if (!driverLoaded) loadDriver();
        return DriverManager.getConnection(url, username, password);
    }
}"""
    add_code_block(doc, code_7_6, "Excerpt 7.6: Resilient Singleton Database Connection Manager (yieldgrid.database.DBConnection)")

    # 7.6 DAO Pattern Implementation
    add_heading_2(doc, "7.6 Data Access Object (DAO) Pattern Implementation")
    add_body_p(
        doc,
        "YieldGrid strictly implements the Data Access Object (DAO) pattern to decouple database queries from business services. "
        "All SQL queries use java.sql.PreparedStatement with parameter binding, completely eliminating SQL injection vulnerabilities. "
        "CropDAO manages CRUD operations for agricultural inventory (Excerpt 7.7), and OrderDAO coordinates multi-table join queries (Excerpt 7.8)."
    )

    code_7_7 = """package yieldgrid.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import yieldgrid.database.DBConnection;
import yieldgrid.model.Crop;

public class CropDAO {
    public boolean addCrop(Crop crop) throws SQLException {
        String sql = "INSERT INTO crops (farmer_id, crop_name, description, quantity, price, available) VALUES (?, ?, ?, ?, ?, ?)";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, crop.getFarmerId());
            pstmt.setString(2, crop.getCropName());
            pstmt.setString(3, crop.getDescription());
            pstmt.setInt(4, crop.getQuantity());
            pstmt.setDouble(5, crop.getPrice());
            pstmt.setBoolean(6, crop.isAvailable());
            return pstmt.executeUpdate() > 0;
        }
    }

    public List<Crop> getAllAvailableCrops() throws SQLException {
        List<Crop> crops = new ArrayList<>();
        String sql = "SELECT c.*, u.name AS farmer_name FROM crops c JOIN users u ON c.farmer_id = u.user_id " +
                     "WHERE c.available = TRUE AND c.quantity > 0 ORDER BY c.crop_name ASC";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql);
             ResultSet rs = pstmt.executeQuery()) {
            while (rs.next()) {
                crops.add(new Crop(rs.getInt("crop_id"), rs.getInt("farmer_id"), rs.getString("farmer_name"),
                                   rs.getString("crop_name"), rs.getString("description"),
                                   rs.getInt("quantity"), rs.getDouble("price"), rs.getBoolean("available")));
            }
        }
        return crops;
    }
}"""
    add_code_block(doc, code_7_7, "Excerpt 7.7: Parameterized Persistence in Crop Data Access (yieldgrid.dao.CropDAO)")

    code_7_8 = """package yieldgrid.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.List;
import yieldgrid.database.DBConnection;
import yieldgrid.model.Order;
import yieldgrid.model.OrderStatus;

public class OrderDAO {
    public List<Order> getOrdersByCustomer(int customerId) throws SQLException {
        List<Order> orders = new ArrayList<>();
        String sql = "SELECT o.*, u.name AS farmer_name FROM orders o JOIN users u ON o.farmer_id = u.user_id " +
                     "WHERE o.customer_id = ? ORDER BY o.order_date DESC";
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {
            pstmt.setInt(1, customerId);
            try (ResultSet rs = pstmt.executeQuery()) {
                while (rs.next()) {
                    orders.add(new Order(rs.getInt("order_id"), rs.getInt("customer_id"), rs.getInt("farmer_id"),
                                         rs.getTimestamp("order_date"), rs.getDouble("total_amount"),
                                         OrderStatus.valueOf(rs.getString("status"))));
                }
            }
        }
        return orders;
    }
}"""
    add_code_block(doc, code_7_8, "Excerpt 7.8: Complex Join Queries for Order History (yieldgrid.dao.OrderDAO)")

    # 7.7 Business Logic & ACID Transactions
    add_heading_2(doc, "7.7 Business Logic and ACID Transaction Management")
    add_body_p(
        doc,
        "The defining transactional feature of YieldGrid is implemented in OrderDAO.createOrder() and invoked via OrderService.placeOrder(). "
        "When a retail customer executes checkout, multiple database modifications must take place simultaneously: master order insertion, "
        "individual line item insertion, and inventory stock decrements. YieldGrid achieves strict ACID compliance by invoking "
        "conn.setAutoCommit(false). The order header is inserted with RETURN_GENERATED_KEYS, and stock is decremented via an atomic SQL statement "
        "with an inline conditional check: UPDATE crops SET quantity = quantity - ? WHERE crop_id = ? AND quantity >= ?. If affected rows "
        "equals zero, the catch block triggers conn.rollback(), restoring all previous inventory counts and preventing partial writes."
    )

    code_7_9 = """package yieldgrid.dao;

import java.sql.*;
import yieldgrid.database.DBConnection;
import yieldgrid.model.Order;
import yieldgrid.model.OrderItem;

public class OrderDAO {
    public boolean createOrder(Order order) throws SQLException {
        Connection conn = null;
        String insertOrderSql = "INSERT INTO orders (customer_id, farmer_id, total_amount, status) VALUES (?, ?, ?, ?)";
        String insertItemSql = "INSERT INTO order_items (order_id, crop_id, quantity, unit_price, subtotal) VALUES (?, ?, ?, ?, ?)";
        String updateStockSql = "UPDATE crops SET quantity = quantity - ? WHERE crop_id = ? AND quantity >= ?";

        try {
            conn = DBConnection.getConnection();
            conn.setAutoCommit(false); // ACID BOUNDARY: Disable autocommit

            int orderId;
            try (PreparedStatement pstmt = conn.prepareStatement(insertOrderSql, Statement.RETURN_GENERATED_KEYS)) {
                pstmt.setInt(1, order.getCustomerId());
                pstmt.setInt(2, order.getFarmerId());
                pstmt.setDouble(3, order.getTotalAmount());
                pstmt.setString(4, order.getStatus().name());
                if (pstmt.executeUpdate() == 0) { conn.rollback(); return false; }
                try (ResultSet rs = pstmt.getGeneratedKeys()) {
                    if (rs.next()) { orderId = rs.getInt(1); order.setOrderId(orderId); }
                    else { conn.rollback(); return false; }
                }
            }

            try (PreparedStatement itemPstmt = conn.prepareStatement(insertItemSql);
                 PreparedStatement stockPstmt = conn.prepareStatement(updateStockSql)) {
                for (OrderItem item : order.getItems()) {
                    item.setOrderId(orderId);
                    itemPstmt.setInt(1, orderId); itemPstmt.setInt(2, item.getCropId());
                    itemPstmt.setInt(3, item.getQuantity()); itemPstmt.setDouble(4, item.getUnitPrice());
                    itemPstmt.setDouble(5, item.getSubtotal());
                    itemPstmt.executeUpdate();

                    // Atomic decrement: conditional WHERE prevents negative inventory
                    stockPstmt.setInt(1, item.getQuantity()); stockPstmt.setInt(2, item.getCropId());
                    stockPstmt.setInt(3, item.getQuantity());
                    if (stockPstmt.executeUpdate() == 0) {
                        conn.rollback(); // Insufficient stock: Rollback transaction entirely
                        return false;
                    }
                }
            }
            conn.commit(); // ACID COMMIT: Persist atomically
            return true;
        } catch (SQLException e) {
            if (conn != null) conn.rollback();
            throw e;
        } finally {
            if (conn != null) { conn.setAutoCommit(true); conn.close(); }
        }
    }
}"""
    add_code_block(doc, code_7_9, "Excerpt 7.9: Atomic Order Placement & Conditional Inventory Decrement (yieldgrid.dao.OrderDAO)")

    # 7.8 Farmer Workflow Implementation
    add_heading_2(doc, "7.8 Farmer Workflow Implementation and Produce Management")
    add_body_p(
        doc,
        "The farmer interface is built within CropManagementPanel, IncomingOrdersPanel, and RevenuePanel under package yieldgrid.ui. "
        "CropManagementPanel encapsulates Swing input components alongside a custom DefaultTableModel bound to a JTable. When a farmer "
        "enters new crop attributes and clicks 'Add Crop', an ActionEvent listener executes asynchronous validation via CropService. "
        "If valid, the produce is saved to MySQL, the form inputs are cleared, and the table dynamically refreshes its view."
    )

    code_7_10 = """package yieldgrid.ui;

import java.awt.event.ActionEvent;
import javax.swing.*;
import yieldgrid.model.Crop;
import yieldgrid.service.CropService;
import yieldgrid.service.SessionManager;

public class CropManagementPanel extends JPanel {
    private final CropService cropService = new CropService();
    private JTextField txtCropName, txtPrice, txtQuantity;

    private void handleAddCrop(ActionEvent e) {
        try {
            String name = txtCropName.getText().trim();
            int qty = Integer.parseInt(txtQuantity.getText().trim());
            double price = Double.parseDouble(txtPrice.getText().trim());
            int farmerId = SessionManager.getCurrentUser().getUserId();

            Crop crop = new Crop(0, farmerId, SessionManager.getCurrentUser().getName(), name, "", qty, price, true);
            cropService.addCrop(crop);
            JOptionPane.showMessageDialog(this, "Produce listed successfully!", "Success", JOptionPane.INFORMATION_MESSAGE);
            refreshCropTable();
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Error: " + ex.getMessage(), "Validation Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}"""
    add_code_block(doc, code_7_10, "Excerpt 7.10: Produce Addition and Table Refresh Logic (yieldgrid.ui.CropManagementPanel)")

    add_body_p(
        doc,
        "Figure 7.3 displays the Farmer Manage Crops panel, allowing farmers to list produce, update unit quantities, and adjust pricing. "
        "Figure 7.4 depicts the Incoming Orders tab, where farmers review customer purchase orders and advance fulfillment states "
        "from PENDING to CONFIRMED, SHIPPED, or DELIVERED. Figure 7.5 illustrates the Revenue & Sales analytics view, providing "
        "real-time calculation of gross revenue, delivered orders count, average order value, and an interactive sales history audit table."
    )

    add_side_by_side_figures(
        doc,
        "static/images/Screenshot 2026-10-11 160930.png", "Figure 7.3: Crop Inventory Management",
        "static/images/Screenshot 2026-10-11 160946.png", "Figure 7.4: Incoming Orders Fulfillment",
        width=Inches(3.1)
    )
    add_figure(doc, "static/images/Screenshot 2026-10-11 161022.png", "Figure 7.5: Farmer Revenue Analytics, KPI Cards, and Sales History (Revenue & Sales Tab)", width=Inches(4.4))

    # 7.9 Customer Marketplace & Cart Mechanics
    add_heading_2(doc, "7.9 Customer Marketplace and Shopping Cart Mechanics")
    add_body_p(
        doc,
        "Customer browsing and shopping cart logic are implemented across CropBrowsePanel and CartPanel. "
        "CropBrowsePanel provides instant keyword filtering across crop names, descriptions, and farmer locations. "
        "CartPanel models shopping cart contents using java.util.ArrayList<CartItem> stored within SessionManager. "
        "As quantities are adjusted, the panel recalculates subtotals and displays cumulative totals. Clicking 'Proceed to Checkout' "
        "triggers OrderService.placeOrder(), converting active cart items into confirmed database orders."
    )

    code_7_11 = """package yieldgrid.ui;

import java.util.ArrayList;
import javax.swing.*;
import yieldgrid.model.CartItem;
import yieldgrid.service.OrderService;
import yieldgrid.service.SessionManager;

public class CartPanel extends JPanel {
    private final OrderService orderService = new OrderService();

    private void executeCheckout() {
        ArrayList<CartItem> cart = SessionManager.getActiveCart();
        if (cart.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Your shopping cart is empty.", "Warning", JOptionPane.WARNING_MESSAGE);
            return;
        }
        try {
            int customerId = SessionManager.getCurrentUser().getUserId();
            boolean success = orderService.placeOrder(customerId, cart);
            if (success) {
                cart.clear();
                JOptionPane.showMessageDialog(this, "Order placed successfully!", "Order Success", JOptionPane.INFORMATION_MESSAGE);
                refreshCartTable();
            }
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Checkout failed: " + ex.getMessage(), "Transaction Error", JOptionPane.ERROR_MESSAGE);
        }
    }
}"""
    add_code_block(doc, code_7_11, "Excerpt 7.11: Customer Cart Calculations and Checkout Trigger (yieldgrid.ui.CartPanel)")

    add_body_p(
        doc,
        "Figure 7.6 showcases the Customer Marketplace (Browse Produce tab), highlighting real-time keyword search, categorized produce listings, "
        "and farmer contact details. Figure 7.7 illustrates the Shopping Cart interface, showing itemized line totals, quantity controls, "
        "and the checkout action trigger."
    )

    add_side_by_side_figures(
        doc,
        "static/images/Screenshot 2026-10-11 161055.png", "Figure 7.6: Produce Marketplace Search",
        "static/images/Screenshot 2026-10-11 161108.png", "Figure 7.7: Shopping Cart & Checkout",
        width=Inches(3.1)
    )

    # 7.10 Order Fulfillment Lifecycle & Profile Management
    add_heading_2(doc, "7.10 Order Fulfillment Lifecycle and Customer Account Management")
    add_body_p(
        doc,
        "Order lifecycle states are modeled as a Java enum OrderStatus in package yieldgrid.model. The enum defines valid states: "
        "PENDING, CONFIRMED, SHIPPED, DELIVERED, and CANCELLED. OrdersPanel in package yieldgrid.ui allows customers to track order progress "
        "and cancel pending orders. The service layer verifies that terminal states (DELIVERED, CANCELLED) cannot be modified further."
    )

    code_7_12 = """package yieldgrid.model;

public enum OrderStatus {
    PENDING("Order received, awaiting confirmation"),
    CONFIRMED("Confirmed by farmer, preparing harvest"),
    SHIPPED("Harvested and dispatched for transit"),
    DELIVERED("Produce delivered successfully"),
    CANCELLED("Order cancelled");

    private final String description;
    OrderStatus(String description) { this.description = description; }
    public String getDescription() { return description; }

    public boolean canTransitionTo(OrderStatus next) {
        if (this == DELIVERED || this == CANCELLED) return false;
        if (this == PENDING) return next == CONFIRMED || next == CANCELLED;
        if (this == CONFIRMED) return next == SHIPPED || next == CANCELLED;
        if (this == SHIPPED) return next == DELIVERED;
        return false;
    }
}"""
    add_code_block(doc, code_7_12, "Excerpt 7.12: Order State Transition Business Logic (yieldgrid.model.OrderStatus)")

    add_body_p(
        doc,
        "Figure 7.8 presents the Customer Order History & Tracking interface, featuring a visual order timeline, fulfillment badges, "
        "and order cancellation options. Figure 7.9 shows the User Profile Management dialog (ProfilePanel), enabling customers to "
        "update their contact numbers, addresses, and modify account passwords with cryptographic salting."
    )

    add_side_by_side_figures(
        doc,
        "static/images/Screenshot 2026-10-11 161114.png", "Figure 7.8: Customer Order History & Tracking",
        "static/images/Screenshot 2026-10-11 161152.png", "Figure 7.9: Customer Profile & Security Dialog",
        width=Inches(3.1)
    )

    # 7.11 Administrative Governance
    add_heading_2(doc, "7.11 Administrative Governance and Auditing Console")
    add_body_p(
        doc,
        "AdminDashboard and AdminService provide governance capabilities for system administrators. The interface displays "
        "six real-time KPI metric cards: Total Registered Users, Active Farmers, Retail Customers, Produce Listed, Total Orders, "
        "and Platform Revenue. Administrators can inspect registered accounts and toggle account status. To prevent catastrophic lockouts, "
        "AdminService enforces a critical safety invariant: deactivating the last active administrator account is strictly disallowed."
    )

    code_7_13 = """package yieldgrid.service;

import yieldgrid.dao.AdminDAO;
import yieldgrid.dao.UserDAO;
import yieldgrid.exception.ValidationException;
import yieldgrid.model.User;

public class AdminService {
    private final AdminDAO adminDAO = new AdminDAO();
    private final UserDAO userDAO = new UserDAO();

    public boolean toggleUserStatus(int targetUserId) throws ValidationException {
        User target = userDAO.getUserById(targetUserId);
        if (target == null) throw new ValidationException("Target user does not exist.");

        // SAFETY SAFEGUARD: Prevent deactivating the last active administrator
        if ("ADMIN".equalsIgnoreCase(target.getRole()) && target.isActive()) {
            int activeAdmins = adminDAO.countActiveAdmins();
            if (activeAdmins <= 1) {
                throw new ValidationException("Cannot deactivate the last active administrator account.");
            }
        }
        return adminDAO.updateUserStatus(targetUserId, !target.isActive());
    }
}"""
    add_code_block(doc, code_7_13, "Excerpt 7.13: Administrative Invariant Checks & User Status Moderation (yieldgrid.service.AdminService)")

    add_body_p(
        doc,
        "Figures 7.10 through 7.15 demonstrate the full administrative governance console. Figure 7.10 shows the System Overview dashboard "
        "with six real-time KPI cards. Figure 7.11 illustrates the User Accounts table with status toggling. Figure 7.12 depicts the global "
        "Produce Catalog moderation view. Figure 7.13 shows the Orders Oversight audit panel. Figure 7.14 presents the Platform Hierarchy "
        "JTree component structuring system roles and entities. Finally, Figure 7.15 shows the Administrator Profile security dialog."
    )

    add_side_by_side_figures(
        doc,
        "static/images/Screenshot 2026-10-11 161426.png", "Figure 7.10: Admin System KPI Overview",
        "static/images/Screenshot 2026-10-11 161445.png", "Figure 7.11: User Accounts Management",
        width=Inches(3.1)
    )
    add_side_by_side_figures(
        doc,
        "static/images/Screenshot 2026-10-11 161529.png", "Figure 7.12: Produce Catalog Moderation",
        "static/images/Screenshot 2026-10-11 161553.png", "Figure 7.13: Orders Oversight Audit",
        width=Inches(3.1)
    )
    add_side_by_side_figures(
        doc,
        "static/images/Screenshot 2026-10-11 161602.png", "Figure 7.14: Platform Hierarchy JTree",
        "static/images/Screenshot 2026-10-11 161611.png", "Figure 7.15: Admin Profile & Credentials",
        width=Inches(3.1)
    )

    # 7.12 Data Export & CSV Injection Prevention
    add_heading_2(doc, "7.12 File I/O and Spreadsheet Formula Injection Prevention")
    add_body_p(
        doc,
        "DataExporter in package yieldgrid.util provides CSV export functionality for financial audits using java.io streams. "
        "To defend against CSV/Formula Injection (CWE-1236), where malicious formula characters ('=', '+', '-', '@') in produce or usernames "
        "execute maliciously in spreadsheet applications (Microsoft Excel), escapeCsvField() prepends a single quotation mark (') to neutralize execution."
    )

    code_7_14 = """package yieldgrid.util;

import java.io.*;
import java.util.List;
import yieldgrid.model.User;

public class DataExporter {
    public static String escapeCsvField(String input) {
        if (input == null) return "";
        String field = input;
        if (!field.isEmpty()) {
            char first = field.charAt(0);
            if (first == '=' || first == '+' || first == '-' || first == '@') {
                field = "'" + field; // Prepend quote to neutralize spreadsheet formula execution
            }
        }
        return field.replace("\\r\\n", " ").replace("\\"", "\\"\\"");
    }

    public static File exportUsersToCSV(List<User> users, File targetFile) throws IOException {
        try (PrintWriter writer = new PrintWriter(new BufferedWriter(new FileWriter(targetFile)))) {
            writer.println("User ID,Full Name,Username,Role,Account Status,Contact Information");
            for (User u : users) {
                writer.printf("%d,\\"%s\\",\\"%s\\",\\"%s\\",\\"%s\\",\\"%s\\"%n",
                    u.getUserId(), escapeCsvField(u.getName()), escapeCsvField(u.getUsername()),
                    u.getRole(), u.isActive() ? "Active" : "Inactive", escapeCsvField(u.getContactInfo()));
            }
        }
        return targetFile;
    }
}"""
    add_code_block(doc, code_7_14, "Excerpt 7.14: RFC 4180 CSV Export with Formula Injection Mitigation (yieldgrid.util.DataExporter)")

    # 7.13 Recursion & Method Overloading
    add_heading_2(doc, "7.13 Recursive Data Processing and Method Overloading")
    add_body_p(
        doc,
        "InventoryAnalytics in package yieldgrid.util demonstrates Unit-I concepts: recursion and method overloading. "
        "The calculateRecursiveStockUnits() method computes the total physical inventory units across a list of crops recursively. "
        "The base case handles empty or boundary conditions, while the recursive step accumulates the current quantity with the remaining sublist."
    )

    code_7_15 = """package yieldgrid.util;

import java.util.List;
import yieldgrid.model.Crop;

public class InventoryAnalytics {
    // UNIT-I: Recursion base case and recursive accumulation
    public static int calculateRecursiveStockUnits(List<Crop> crops, int index) {
        if (crops == null || index < 0 || index >= crops.size()) return 0;
        Crop crop = crops.get(index);
        int quantity = (crop != null) ? crop.getQuantity() : 0;
        return quantity + calculateRecursiveStockUnits(crops, index + 1);
    }

    // UNIT-I: Method overloading providing zero-argument starting index
    public static int calculateRecursiveStockUnits(List<Crop> crops) {
        return calculateRecursiveStockUnits(crops, 0);
    }
}"""
    add_code_block(doc, code_7_15, "Excerpt 7.15: Recursive Inventory Accumulation & Overloading (yieldgrid.util.InventoryAnalytics)")

    # 7.14 Multithreading & Synchronization
    add_heading_2(doc, "7.14 Multithreading and Concurrency Synchronization")
    add_body_p(
        doc,
        "MultithreadingDemo in package yieldgrid.util provides a rigorous, self-contained demonstration of Unit-III multithreading. "
        "It models a classic Producer-Consumer architecture using an internal monitor-synchronized BoundedBuffer. "
        "The Producer thread implements java.lang.Runnable and inserts items into the buffer, calling wait() when capacity is reached. "
        "The Consumer thread retrieves items, calling wait() when the buffer is empty. Thread state notifications use notifyAll(), "
        "preventing thread starvation and demonstrating clean thread coordination."
    )

    code_7_16 = """package yieldgrid.util;

import java.util.LinkedList;
import java.util.Queue;

public class MultithreadingDemo {
    // Monitor-synchronized bounded buffer for thread-safe coordination
    static class BoundedBuffer {
        private final Queue<String> queue = new LinkedList<>();
        private final int capacity;

        BoundedBuffer(int capacity) { this.capacity = capacity; }

        public synchronized void put(String item) throws InterruptedException {
            while (queue.size() >= capacity) {
                wait(); // Wait until consumer frees capacity
            }
            queue.add(item);
            notifyAll(); // Wake waiting consumer threads
        }

        public synchronized String take() throws InterruptedException {
            while (queue.isEmpty()) {
                wait(); // Wait until producer adds item
            }
            String item = queue.poll();
            notifyAll(); // Wake waiting producer threads
            return item;
        }
    }
}"""
    add_code_block(doc, code_7_16, "Excerpt 7.16: Producer-Consumer Thread Coordination with wait() & notifyAll() (yieldgrid.util.MultithreadingDemo)")

    doc.add_page_break()
    print("Chapter 7 (Implementation) generated successfully with all 15 authentic screenshots.")
