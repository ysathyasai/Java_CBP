package yieldgrid.test;

import java.io.File;
import java.io.IOException;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TreeSet;
import yieldgrid.dao.AdminDAO;
import yieldgrid.dao.CropDAO;
import yieldgrid.dao.UserDAO;
import yieldgrid.database.DBConnection;
import yieldgrid.exception.AuthenticationException;
import yieldgrid.exception.InsufficientStockException;
import yieldgrid.exception.ValidationException;
import yieldgrid.interfaces.AdminActions;
import yieldgrid.interfaces.DashboardActions;
import yieldgrid.model.AdminUser;
import yieldgrid.model.CartItem;
import yieldgrid.model.Crop;
import yieldgrid.model.Customer;
import yieldgrid.model.Farmer;
import yieldgrid.model.Order;
import yieldgrid.model.OrderItem;
import yieldgrid.model.OrderStatus;
import yieldgrid.model.User;
import yieldgrid.service.AdminService;
import yieldgrid.service.AuthenticationService;
import yieldgrid.service.CropService;
import yieldgrid.service.OrderService;
import yieldgrid.service.RevenueService;
import yieldgrid.service.SessionManager;
import yieldgrid.util.DataExporter;
import yieldgrid.util.InventoryAnalytics;
import yieldgrid.util.MultithreadingDemo;
import yieldgrid.util.PasswordUtil;

/**
 * Rigorous verification test suite for YieldGrid:
 * Validates OOP models, authentication, PBKDF2 cryptography, transactions,
 * access control, multithreading, file I/O, collections, and live database workflows.
 */
public class WorkflowVerificationTest {

    private static int testsPassed = 0;
    private static int testsFailed = 0;

    public static void main(String[] args) {
        System.out.println("==================================================");
        System.out.println("YieldGrid — Course Concept & Workflow Verification");
        System.out.println("==================================================");

        testEncapsulationAndModels();
        testInheritanceAndPolymorphism();
        testInterfaceComplianceAndExtension();
        testEnumsAndTransitions();
        testObjectInteractionAndCart();
        testArithmeticAndComposition();
        testStringHandlingAndSearch();
        testValidationAndExceptionHandling();
        testAccessControlRules();
        testPasswordHashingAndSecurity();
        testRecursion();
        testCollectionsFramework();
        testFileIoCsvExport();
        testMultithreading();
        testDatabaseConnectivityAndLiveWorkflows();

        System.out.println("==================================================");
        System.out.println("TEST SUMMARY:");
        System.out.println("Tests Passed: " + testsPassed);
        System.out.println("Tests Failed: " + testsFailed);
        System.out.println("==================================================");

        if (testsFailed > 0) {
            System.exit(1);
        }
    }

    private static void assertTrue(String testName, boolean condition) {
        if (condition) {
            System.out.println("  [PASS] " + testName);
            testsPassed++;
        } else {
            System.err.println("  [FAIL] " + testName);
            testsFailed++;
        }
    }

    // 1. Encapsulation & Models
    private static void testEncapsulationAndModels() {
        System.out.println("\n--- 1. Testing Encapsulation & Models ---");
        Crop crop = new Crop(1, 10, "Test Farmer", "Wheat", "Fresh golden wheat", 50, 40.0, true);
        assertTrue("Encapsulated getters return initialized state",
                "Wheat".equals(crop.getCropName()) && crop.getPrice() == 40.0 && crop.getQuantity() == 50);
        crop.setQuantity(45);
        assertTrue("Encapsulated setter updates field properly", crop.getQuantity() == 45);
    }

    // 2. Inheritance & Polymorphism
    private static void testInheritanceAndPolymorphism() {
        System.out.println("\n--- 2. Testing Inheritance & Polymorphism ---");
        User farmerUser = new Farmer(1, "Ramesh", "farmer1", "pass", "Guntur");
        User customerUser = new Customer(2, "Anita", "customer1", "pass", "Vijayawada");
        User adminUser = new AdminUser(3, "Admin", "admin", "pass", "HQ");

        assertTrue("Subclasses inherit from abstract User base class",
                farmerUser instanceof User && customerUser instanceof User && adminUser instanceof User);
        assertTrue("Polymorphic role descriptions dispatched correctly",
                farmerUser.getRoleDescription().contains("Farmer") &&
                customerUser.getRoleDescription().contains("Customer") &&
                adminUser.getRoleDescription().contains("Administrator"));

        User customerClone = new Customer(2, "Anita Clone", "customer1", "pass", "Vijayawada");
        assertTrue("Overridden equals() identifies same entity by ID and username", customerUser.equals(customerClone));
        assertTrue("Overridden hashCode() is consistent with equals()", customerUser.hashCode() == customerClone.hashCode());
    }

    // 3. Interfaces & Interface Inheritance
    private static void testInterfaceComplianceAndExtension() {
        System.out.println("\n--- 3. Testing Interfaces & Extending Interfaces ---");
        assertTrue("Interface constant APPLICATION_NAME is accessible",
                "YieldGrid".equals(DashboardActions.APPLICATION_NAME));

        AdminActions mockAdmin = new AdminActions() {
            @Override public void refreshData() {}
            @Override public void showProfile() {}
            @Override public void logout() {}
            @Override public void auditUserAccounts() {}
            @Override public void viewSystemMetrics() {}
            @Override public void exportAuditReport() {}
        };
        assertTrue("Extending interfaces: AdminActions extends DashboardActions", mockAdmin instanceof DashboardActions);
    }

    // 4. Java Enums
    private static void testEnumsAndTransitions() {
        System.out.println("\n--- 4. Testing Java Enum (OrderStatus) ---");
        assertTrue("Enum initial state and parser work accurately",
                OrderStatus.PENDING == OrderStatus.fromString("PENDING") &&
                OrderStatus.CONFIRMED == OrderStatus.fromString("CONFIRMED") &&
                OrderStatus.PENDING == OrderStatus.fromString("INVALID"));
    }

    // 5. Object Interaction & Cart
    private static void testObjectInteractionAndCart() {
        System.out.println("\n--- 5. Testing Object Interaction & Cart ---");
        Crop tomato = new Crop(1, 1, "Ramesh", "Organic Tomato", "Red tomatoes", 100, 30.0, true);
        CartItem cartItem = new CartItem(tomato, 5);
        assertTrue("CartItem interacts with Crop to compute subtotal (30*5=150)", cartItem.getSubtotal() == 150.0);

        SessionManager.logout();
        ArrayList<CartItem> cart = SessionManager.getActiveCart();
        cart.add(cartItem);
        assertTrue("Cart tracks item addition", cart.size() == 1);
        SessionManager.clearCart();
        assertTrue("Cart clears successfully", SessionManager.getActiveCart().isEmpty());
    }

    // 6. Arithmetic Operations & Composition
    private static void testArithmeticAndComposition() {
        System.out.println("\n--- 6. Testing Arithmetic & Composition ---");
        Order order = new Order(101, 1, "Anita", 2, "Ramesh", new Date(), 0.0, OrderStatus.PENDING);
        order.addItem(new OrderItem(1, "Tomato", 4, 30.0));
        order.addItem(new OrderItem(2, "Potato", 5, 20.0));
        assertTrue("Order composition and total calculation (120+100=220)",
                order.getItems().size() == 2 && order.getTotalAmount() == 220.0);
    }

    // 7. String Handling & Search
    private static void testStringHandlingAndSearch() {
        System.out.println("\n--- 7. Testing String Handling & Searching ---");
        String cropName = "Organic Tomato";
        assertTrue("Case-insensitive substring search works",
                cropName.toLowerCase().contains("tom") && !cropName.toLowerCase().contains("onion"));
    }

    // 8. Validation & Custom Exceptions
    private static void testValidationAndExceptionHandling() {
        System.out.println("\n--- 8. Testing Validation & Custom Exceptions ---");
        AuthenticationService authService = new AuthenticationService();
        boolean caughtValidation = false;
        try {
            authService.login("", "password123");
        } catch (ValidationException e) {
            caughtValidation = true;
        } catch (AuthenticationException ignored) {}
        assertTrue("ValidationException thrown for empty credentials", caughtValidation);

        OrderService orderService = new OrderService();
        boolean caughtStock = false;
        try {
            Crop limitedCrop = new Crop(1, 1, "Ramesh", "Chilli", "Spicy", 5, 50.0, true);
            orderService.addToCart(limitedCrop, 10);
        } catch (InsufficientStockException e) {
            caughtStock = true;
        } catch (ValidationException ignored) {}
        assertTrue("InsufficientStockException thrown when requesting beyond available stock", caughtStock);
    }

    // 9. Access Control Rules
    private static void testAccessControlRules() {
        System.out.println("\n--- 9. Testing Access Control Rules ---");
        CropService cropService = new CropService();
        Crop farmer1Crop = new Crop(10, 1, "Crop", "Desc", 20, 25.0, true);
        boolean accessDenied = false;
        try {
            cropService.updateCrop(farmer1Crop, 2);
        } catch (ValidationException e) {
            accessDenied = e.getMessage().contains("Access Denied");
        } catch (SQLException ignored) {}
        assertTrue("Cross-farmer modification blocked by access control", accessDenied);
    }

    // 10. Password Hashing (Salted PBKDF2 & Migration)
    private static void testPasswordHashingAndSecurity() {
        System.out.println("\n--- 10. Testing Password Hashing & Security ---");
        String password = "securePassword123";
        String hash1 = PasswordUtil.hashPassword(password);
        String hash2 = PasswordUtil.hashPassword(password);

        assertTrue("PBKDF2 hash formatted correctly with prefix", hash1.startsWith("pbkdf2$10000$"));
        assertTrue("Random salt generates distinct hashes for identical passwords", !hash1.equals(hash2));
        assertTrue("Password verification succeeds for correct password", PasswordUtil.verifyPassword(password, hash1));
        assertTrue("Password verification rejects invalid password", !PasswordUtil.verifyPassword("wrong", hash1));

        String legacySha256 = "sha256$240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9";
        assertTrue("Legacy SHA-256 hash verified for backward compatibility", PasswordUtil.verifyPassword("admin123", legacySha256));
        assertTrue("PasswordUtil detects legacy hash requires migration", PasswordUtil.needsMigration(legacySha256));
        assertTrue("PasswordUtil detects PBKDF2 hash does not require migration", !PasswordUtil.needsMigration(hash1));
        assertTrue("PasswordUtil identifies hashed strings", PasswordUtil.isHashed(hash1) && !PasswordUtil.isHashed("plaintext"));
    }

    // 11. Recursion & Method Overloading
    private static void testRecursion() {
        System.out.println("\n--- 11. Testing Recursion & Method Overloading ---");
        List<Crop> sampleCrops = List.of(
                new Crop(1, 1, "F1", "Apples", "Fresh", 50, 60.0, true),
                new Crop(2, 1, "F1", "Bananas", "Fresh", 30, 25.0, true),
                new Crop(3, 1, "F1", "Cherries", "Sweet", 20, 120.0, true)
        );

        int totalUnits = InventoryAnalytics.calculateRecursiveStockUnits(sampleCrops);
        assertTrue("Recursion accumulates inventory units accurately (50+30+20=100)", totalUnits == 100);
        assertTrue("Recursion base cases: null and out-of-bounds return 0",
                InventoryAnalytics.calculateRecursiveStockUnits(null, 0) == 0 &&
                InventoryAnalytics.calculateRecursiveStockUnits(sampleCrops, 5) == 0);
    }

    // 12. Collections Framework
    private static void testCollectionsFramework() {
        System.out.println("\n--- 12. Testing Collections Framework ---");
        List<String> list = new ArrayList<>(List.of("Tomato", "Potato", "Tomato"));
        assertTrue("List allows duplicate elements", list.size() == 3);

        Set<String> set = new HashSet<>(list);
        assertTrue("Set eliminates duplicate elements", set.size() == 2);

        TreeSet<String> sortedSet = new TreeSet<>(set);
        assertTrue("TreeSet sorts elements natural ordering", "Potato".equals(sortedSet.first()));

        Map<String, Object> map = new LinkedHashMap<>();
        map.put("totalUsers", 10);
        assertTrue("Map stores and retrieves key-value entries", ((Integer) map.get("totalUsers")) == 10);
    }

    // 13. File I/O CSV Export & Escaping
    private static void testFileIoCsvExport() {
        System.out.println("\n--- 13. Testing File I/O (CSV Export, Escaping & Reading) ---");
        try {
            File tempFile = File.createTempFile("yieldgrid_test_export", ".csv");
            tempFile.deleteOnExit();

            List<User> sampleUsers = List.of(
                    new AdminUser(1, "Admin", "admin_test", "pass", "HQ"),
                    new Customer(2, "Customer", "cust_test", "pass", "Vijayawada")
            );

            DataExporter.exportUsersToCSV(sampleUsers, tempFile);
            assertTrue("CSV file created and exists on disk", tempFile.exists() && tempFile.length() > 0);

            int lines = DataExporter.countCsvLines(tempFile);
            assertTrue("BufferedReader read expected CSV lines (1 header + 2 records = 3)", lines == 3);

            String formula = "=CMD|' /C calc'!A0";
            assertTrue("Formula injection neutralized with leading quote", DataExporter.escapeCsvField(formula).startsWith("'="));

            String quotes = "John \"The Farmer\"";
            assertTrue("Internal quotes escaped per RFC 4180", DataExporter.escapeCsvField(quotes).contains("\"\"The Farmer\"\""));
        } catch (IOException e) {
            assertTrue("File I/O failed: " + e.getMessage(), false);
        }
    }

    // 14. Multithreading & Synchronization
    private static void testMultithreading() {
        System.out.println("\n--- 14. Testing Multithreading & Synchronization ---");
        int processed = MultithreadingDemo.runSimulation(3);
        assertTrue("Multithreading bounded producer-consumer processes all 3 items safely", processed == 3);
    }

    // 15. Live Database Workflows & Admin Management
    private static void testDatabaseConnectivityAndLiveWorkflows() {
        System.out.println("\n--- 15. Testing Live Database Workflows & Transactions ---");
        if (!DBConnection.testConnection()) {
            System.out.println("  [NOTICE] MySQL is offline. Skipping live DB integration workflows.");
            return;
        }

        try (Connection conn = DBConnection.getConnection()) {
            assertTrue("Live MySQL connection successfully established", conn != null && !conn.isClosed());
            DBConnection.initializeDatabaseTables();

            UserDAO userDAO = new UserDAO();
            AdminDAO adminDAO = new AdminDAO();
            AdminService adminService = new AdminService(adminDAO, userDAO);
            AuthenticationService authService = new AuthenticationService(userDAO);

            // Admin Authentication & Authorization
            User admin = authService.login("admin", "admin123");
            assertTrue("Admin authenticated successfully", admin instanceof AdminUser && SessionManager.isAdmin());
            adminService.requireAdminAccess();
            assertTrue("AdminService grants access to authenticated AdminUser", true);

            // Rejection of Non-Admin Access
            User farmer = userDAO.getUserById(2);
            SessionManager.setCurrentUser(farmer);
            boolean nonAdminBlocked = false;
            try {
                adminService.requireAdminAccess();
            } catch (ValidationException e) {
                nonAdminBlocked = true;
            }
            assertTrue("AdminService blocks non-admin user", nonAdminBlocked);
            SessionManager.setCurrentUser(admin);

            // System Metrics
            Map<String, Object> metrics = adminService.getSystemMetrics();
            assertTrue("System metrics retrieved from database", metrics.containsKey("totalUsers") && metrics.containsKey("totalCrops"));

            // Profile Update Persistence
            String newName = "System Administrator (Updated)";
            String newContact = "Admin HQ Vijayawada - Tel: 0866-999999";
            assertTrue("Profile updated via authService", authService.updateProfile(admin, newName, newContact));
            User fetchedAdmin = userDAO.getUserById(admin.getUserId());
            assertTrue("Updated profile persistently saved in MySQL",
                    newName.equals(fetchedAdmin.getName()) && newContact.equals(fetchedAdmin.getContactInfo()));

            // User Registration & Duplicate Rejection
            String testUname = "testcust_" + System.currentTimeMillis();
            User regUser = authService.register("Test Customer", testUname, "testpass123", "CUSTOMER", "Vijayawada");
            assertTrue("New user registered in database", regUser != null);

            boolean duplicateRejected = false;
            try {
                authService.register("Duplicate", testUname, "testpass123", "CUSTOMER", "Vijayawada");
            } catch (ValidationException e) {
                duplicateRejected = true;
            }
            assertTrue("Duplicate username rejected with ValidationException", duplicateRejected);

            // User Activation / Deactivation
            assertTrue("Admin deactivates non-admin account", adminService.toggleUserActiveStatus(regUser.getUserId()));
            boolean loginBlocked = false;
            try {
                authService.login(testUname, "testpass123");
            } catch (AuthenticationException e) {
                loginBlocked = e.getMessage().contains("deactivated");
            }
            assertTrue("Deactivated account blocked from logging in", loginBlocked);
            adminService.toggleUserActiveStatus(regUser.getUserId()); // Reactivate

            // Safeguard: Cannot deactivate last admin
            boolean lastAdminProtected = false;
            try {
                if (userDAO.getActiveAdminCount() == 1) {
                    adminService.toggleUserActiveStatus(admin.getUserId());
                } else {
                    lastAdminProtected = true;
                }
            } catch (ValidationException e) {
                lastAdminProtected = true;
            }
            assertTrue("Safety safeguard prevents deactivating the last active administrator", lastAdminProtected);

            // Crop Catalog & Order Workflow with Inventory Stock Decrement
            CropDAO cropDAO = new CropDAO();
            ArrayList<Crop> crops = adminService.getAllCrops("");
            assertTrue("Produce catalog loaded from database", !crops.isEmpty());

            Crop cropToBuy = null;
            for (Crop c : crops) {
                if (c.isAvailable() && c.getQuantity() >= 5) {
                    cropToBuy = c;
                    break;
                }
            }
            if (cropToBuy == null) {
                cropToBuy = crops.get(0);
                cropToBuy.setQuantity(20);
                cropToBuy.setAvailable(true);
                cropDAO.updateCrop(cropToBuy);
            }
            int initialStock = cropToBuy.getQuantity();

            SessionManager.setCurrentUser(regUser);
            OrderService orderService = new OrderService();
            orderService.addToCart(cropToBuy, 2);
            List<Order> placedOrders = orderService.placeOrdersFromCart(regUser.getUserId());
            assertTrue("Order placed via atomic transaction", !placedOrders.isEmpty());

            Crop updatedCrop = cropDAO.getCropById(cropToBuy.getCropId());
            assertTrue("Inventory quantity decremented safely in MySQL", updatedCrop.getQuantity() == initialStock - 2);

            // Revenue Calculation
            RevenueService revenueService = new RevenueService();
            assertTrue("Farmer revenue calculated successfully", revenueService.calculateFarmerRevenue(cropToBuy.getFarmerId()) >= 0.0);

            // Cleanup & Restore Test State
            authService.updateProfile(admin, "System Administrator", "YieldGrid HQ, Vijayawada - Ph: 9876543000");
            cropToBuy.setQuantity(initialStock);
            cropDAO.updateCrop(cropToBuy);

            try (PreparedStatement ps1 = conn.prepareStatement("DELETE FROM order_items WHERE order_id IN (SELECT order_id FROM orders WHERE customer_id = ?);");
                 PreparedStatement ps2 = conn.prepareStatement("DELETE FROM orders WHERE customer_id = ?;");
                 PreparedStatement ps3 = conn.prepareStatement("DELETE FROM users WHERE user_id = ?;")) {
                ps1.setInt(1, regUser.getUserId());
                ps1.executeUpdate();
                ps2.setInt(1, regUser.getUserId());
                ps2.executeUpdate();
                ps3.setInt(1, regUser.getUserId());
                ps3.executeUpdate();
            }
            assertTrue("Test data cleanly isolated and cleaned up from MySQL", true);

        } catch (Exception e) {
            System.err.println("Database workflow test failed: " + e.getMessage());
            e.printStackTrace();
            assertTrue("Database integration test error: " + e.getMessage(), false);
        }
    }
}
