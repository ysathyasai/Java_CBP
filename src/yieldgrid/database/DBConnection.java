package yieldgrid.database;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Properties;

/*
 * COURSE CONCEPT:
 * JDBC (Java Database Connectivity), Static Utility, Properties / File I/O, Exception Handling
 *
 * PURPOSE:
 * DBConnection manages the database connection lifecycle for YieldGrid.
 * It dynamically reads database configuration (URL, username, and password)
 * from 'config.properties' without hardcoding credentials into source code.
 */

public class DBConnection {

    // JDBC CONCEPT:
    // Credentials and connection parameters read dynamically from external config.properties
    private static String url = "jdbc:mysql://localhost:3306/yieldgrid";
    private static String username = "root";
    private static String password = "";
    private static boolean driverLoaded = false;

    // STATIC INITIALIZER / METHOD:
    // Loads MySQL Connector/J driver and configuration properties when class is first referenced
    static {
        loadConfiguration();
        loadDriver();
    }

    // METHOD CONCEPT / FILE HANDLING:
    // Reads config.properties to externalize credentials
    private static void loadConfiguration() {
        Properties props = new Properties();
        File configFile = new File("config.properties");

        if (configFile.exists()) {
            try (InputStream in = new FileInputStream(configFile)) {
                props.load(in);
                url = props.getProperty("db.url", url);
                username = props.getProperty("db.username", username);
                password = props.getProperty("db.password", password);
            } catch (IOException e) {
                System.err.println("Warning: Could not read config.properties: " + e.getMessage());
            }
        } else {
            System.err.println("Notice: config.properties not found in working directory. Using default connection parameters.");
        }
    }

    // JDBC CONCEPT: Driver Loading
    private static void loadDriver() {
        try {
            // Load MySQL Connector/J JDBC driver
            Class.forName("com.mysql.cj.jdbc.Driver");
            driverLoaded = true;
        } catch (ClassNotFoundException e) {
            System.err.println("Error: MySQL JDBC Driver not found in classpath. Ensure mysql-connector-j jar is present.");
        }
    }

    // JDBC CONCEPT: Connection Factory
    // Establishes and returns a fresh Connection object for executing SQL statements
    public static Connection getConnection() throws SQLException {
        if (!driverLoaded) {
            loadDriver();
        }
        // Always refresh config in case the user updated config.properties while running
        loadConfiguration();
        return DriverManager.getConnection(url, username, password);
    }

    // JDBC & SQL CONCEPT: Table Initialization
    // Ensures tables required by YieldGrid exist in the 'yieldgrid' database
    public static void initializeDatabaseTables() {
        String createUsersTable = "CREATE TABLE IF NOT EXISTS users ("
                + "user_id INT AUTO_INCREMENT PRIMARY KEY, "
                + "name VARCHAR(100) NOT NULL, "
                + "username VARCHAR(50) NOT NULL UNIQUE, "
                + "password VARCHAR(255) NOT NULL, "
                + "role VARCHAR(20) NOT NULL, "
                + "contact_info VARCHAR(150), "
                + "is_active BOOLEAN DEFAULT TRUE, "
                + "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
                + ");";

        String createCropsTable = "CREATE TABLE IF NOT EXISTS crops ("
                + "crop_id INT AUTO_INCREMENT PRIMARY KEY, "
                + "farmer_id INT NOT NULL, "
                + "crop_name VARCHAR(100) NOT NULL, "
                + "description TEXT, "
                + "quantity INT NOT NULL, "
                + "price DECIMAL(10, 2) NOT NULL, "
                + "available BOOLEAN NOT NULL DEFAULT TRUE, "
                + "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                + "FOREIGN KEY (farmer_id) REFERENCES users(user_id) ON DELETE CASCADE"
                + ");";

        String createOrdersTable = "CREATE TABLE IF NOT EXISTS orders ("
                + "order_id INT AUTO_INCREMENT PRIMARY KEY, "
                + "customer_id INT NOT NULL, "
                + "farmer_id INT NOT NULL, "
                + "order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP, "
                + "total_amount DECIMAL(10, 2) NOT NULL, "
                + "status VARCHAR(20) NOT NULL DEFAULT 'PENDING', "
                + "FOREIGN KEY (customer_id) REFERENCES users(user_id) ON DELETE CASCADE, "
                + "FOREIGN KEY (farmer_id) REFERENCES users(user_id) ON DELETE CASCADE"
                + ");";

        String createOrderItemsTable = "CREATE TABLE IF NOT EXISTS order_items ("
                + "order_item_id INT AUTO_INCREMENT PRIMARY KEY, "
                + "order_id INT NOT NULL, "
                + "crop_id INT NOT NULL, "
                + "quantity INT NOT NULL, "
                + "unit_price DECIMAL(10, 2) NOT NULL, "
                + "subtotal DECIMAL(10, 2) NOT NULL, "
                + "FOREIGN KEY (order_id) REFERENCES orders(order_id) ON DELETE CASCADE, "
                + "FOREIGN KEY (crop_id) REFERENCES crops(crop_id) ON DELETE CASCADE"
                + ");";

        try (Connection conn = getConnection(); Statement stmt = conn.createStatement()) {
            stmt.execute(createUsersTable);
            stmt.execute(createCropsTable);
            stmt.execute(createOrdersTable);
            stmt.execute(createOrderItemsTable);

            // Safe schema migrations:
            try {
                stmt.execute("ALTER TABLE users MODIFY COLUMN password VARCHAR(255) NOT NULL;");
            } catch (SQLException ignored) {
            }
            try {
                stmt.execute("ALTER TABLE users ADD COLUMN is_active BOOLEAN DEFAULT TRUE;");
            } catch (SQLException ignored) {
            }

            insertSeedDataIfEmpty(conn);
        } catch (SQLException e) {
            System.err.println("Database initialization notice: " + e.getMessage());
        }
    }

    // SQL / CRUD CONCEPT: Seed Data & Admin Initialization
    // Inserts default sample farmers, customers, crops, and administrator safely using PreparedStatements
    private static void insertSeedDataIfEmpty(Connection conn) {
        try (Statement stmt = conn.createStatement()) {
            // Check if users table is empty
            var rs = stmt.executeQuery("SELECT COUNT(*) AS total FROM users;");
            if (rs.next() && rs.getInt("total") == 0) {
                // Seed Admin, Farmers & Customers with salted PBKDF2 hashed passwords
                String adminPass = yieldgrid.util.PasswordUtil.hashPassword("admin123");
                String farmerPass = yieldgrid.util.PasswordUtil.hashPassword("farmer123");
                String customerPass = yieldgrid.util.PasswordUtil.hashPassword("customer123");

                String insertUserSql = "INSERT INTO users (user_id, name, username, password, role, contact_info, is_active) VALUES (?, ?, ?, ?, ?, ?, ?);";
                try (PreparedStatement psUser = conn.prepareStatement(insertUserSql)) {
                    // 1. Admin
                    psUser.setInt(1, 1);
                    psUser.setString(2, "System Administrator");
                    psUser.setString(3, "admin");
                    psUser.setString(4, adminPass);
                    psUser.setString(5, "ADMIN");
                    psUser.setString(6, "YieldGrid HQ, Vijayawada - Ph: 9876543000");
                    psUser.setBoolean(7, true);
                    psUser.addBatch();

                    // 2. Farmer 1
                    psUser.setInt(1, 2);
                    psUser.setString(2, "Ramesh Kumar (Green Valley Farms)");
                    psUser.setString(3, "farmer1");
                    psUser.setString(4, farmerPass);
                    psUser.setString(5, "FARMER");
                    psUser.setString(6, "Guntur, AP - Ph: 9876543210");
                    psUser.setBoolean(7, true);
                    psUser.addBatch();

                    // 3. Farmer 2
                    psUser.setInt(1, 3);
                    psUser.setString(2, "Suresh Patel (Sunshine Organic Farm)");
                    psUser.setString(3, "farmer2");
                    psUser.setString(4, farmerPass);
                    psUser.setString(5, "FARMER");
                    psUser.setString(6, "Krishna District - Ph: 9876543211");
                    psUser.setBoolean(7, true);
                    psUser.addBatch();

                    // 4. Customer 1
                    psUser.setInt(1, 4);
                    psUser.setString(2, "Anita Sharma");
                    psUser.setString(3, "customer1");
                    psUser.setString(4, customerPass);
                    psUser.setString(5, "CUSTOMER");
                    psUser.setString(6, "Flat 402, Lotus Apts, Vijayawada");
                    psUser.setBoolean(7, true);
                    psUser.addBatch();

                    // 5. Customer 2
                    psUser.setInt(1, 5);
                    psUser.setString(2, "Vikram Reddy");
                    psUser.setString(3, "customer2");
                    psUser.setString(4, customerPass);
                    psUser.setString(5, "CUSTOMER");
                    psUser.setString(6, "Plot 18, Green Meadows, Guntur");
                    psUser.setBoolean(7, true);
                    psUser.addBatch();

                    psUser.executeBatch();
                }

                // Seed Crops
                String insertCropSql = "INSERT INTO crops (crop_id, farmer_id, crop_name, description, quantity, price, available) VALUES (?, ?, ?, ?, ?, ?, ?);";
                try (PreparedStatement psCrop = conn.prepareStatement(insertCropSql)) {
                    psCrop.setInt(1, 1);
                    psCrop.setInt(2, 2);
                    psCrop.setString(3, "Organic Tomato");
                    psCrop.setString(4, "Freshly harvested farm-fresh red ripe tomatoes (per kg)");
                    psCrop.setInt(5, 150);
                    psCrop.setDouble(6, 35.00);
                    psCrop.setBoolean(7, true);
                    psCrop.addBatch();

                    psCrop.setInt(1, 2);
                    psCrop.setInt(2, 2);
                    psCrop.setString(3, "Russet Potato");
                    psCrop.setString(4, "Cleaned grade-A earthy potatoes suitable for all dishes (per kg)");
                    psCrop.setInt(5, 200);
                    psCrop.setDouble(6, 28.00);
                    psCrop.setBoolean(7, true);
                    psCrop.addBatch();

                    psCrop.setInt(1, 3);
                    psCrop.setInt(2, 2);
                    psCrop.setString(3, "Red Onion");
                    psCrop.setString(4, "Crisp pungent red onions grown with minimal pesticides (per kg)");
                    psCrop.setInt(5, 120);
                    psCrop.setDouble(6, 42.00);
                    psCrop.setBoolean(7, true);
                    psCrop.addBatch();

                    psCrop.setInt(1, 4);
                    psCrop.setInt(2, 3);
                    psCrop.setString(3, "Fresh Carrot");
                    psCrop.setString(4, "Sweet and crunchy orange carrots rich in vitamin A (per kg)");
                    psCrop.setInt(5, 80);
                    psCrop.setDouble(6, 50.00);
                    psCrop.setBoolean(7, true);
                    psCrop.addBatch();

                    psCrop.setInt(1, 5);
                    psCrop.setInt(2, 3);
                    psCrop.setString(3, "Organic Spinach");
                    psCrop.setString(4, "Tender green spinach leaves harvested every morning (per bunch)");
                    psCrop.setInt(5, 90);
                    psCrop.setDouble(6, 20.00);
                    psCrop.setBoolean(7, true);
                    psCrop.addBatch();

                    psCrop.setInt(1, 6);
                    psCrop.setInt(2, 3);
                    psCrop.setString(3, "Guntur Green Chilli");
                    psCrop.setString(4, "Spicy aromatic green chillies freshly plucked (per kg)");
                    psCrop.setInt(5, 60);
                    psCrop.setDouble(6, 65.00);
                    psCrop.setBoolean(7, true);
                    psCrop.addBatch();

                    psCrop.executeBatch();
                }
            } else {
                // If users already exist, ensure an administrator account is present
                var adminRs = stmt.executeQuery("SELECT COUNT(*) AS admin_count FROM users WHERE role = 'ADMIN';");
                if (adminRs.next() && adminRs.getInt("admin_count") == 0) {
                    String adminPass = yieldgrid.util.PasswordUtil.hashPassword("admin123");
                    String insAdminSql = "INSERT INTO users (name, username, password, role, contact_info, is_active) VALUES (?, ?, ?, ?, ?, ?);";
                    try (PreparedStatement psAdmin = conn.prepareStatement(insAdminSql)) {
                        psAdmin.setString(1, "System Administrator");
                        psAdmin.setString(2, "admin");
                        psAdmin.setString(3, adminPass);
                        psAdmin.setString(4, "ADMIN");
                        psAdmin.setString(5, "YieldGrid HQ, Vijayawada - Ph: 9876543000");
                        psAdmin.setBoolean(6, true);
                        psAdmin.executeUpdate();
                    }
                }

                // Smooth migration for existing unhashed passwords: hash any legacy plaintext passwords
                var existingUsers = stmt.executeQuery("SELECT user_id, password FROM users;");
                java.util.Map<Integer, String> toUpdate = new java.util.HashMap<>();
                while (existingUsers.next()) {
                    int uid = existingUsers.getInt("user_id");
                    String pass = existingUsers.getString("password");
                    if (pass != null && !yieldgrid.util.PasswordUtil.isHashed(pass)) {
                        toUpdate.put(uid, yieldgrid.util.PasswordUtil.hashPassword(pass));
                    }
                }
                for (var entry : toUpdate.entrySet()) {
                    try (var ps = conn.prepareStatement("UPDATE users SET password = ? WHERE user_id = ?;")) {
                        ps.setString(1, entry.getValue());
                        ps.setInt(2, entry.getKey());
                        ps.executeUpdate();
                    }
                }
            }
        } catch (SQLException e) {
            System.err.println("Seed data insertion notice: " + e.getMessage());
        }
    }

    // Helper method to test connectivity
    public static boolean testConnection() {
        try (Connection conn = getConnection()) {
            return conn != null && !conn.isClosed();
        } catch (SQLException e) {
            return false;
        }
    }
}
