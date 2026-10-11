package yieldgrid.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import yieldgrid.database.DBConnection;
import yieldgrid.model.AdminUser;
import yieldgrid.model.Customer;
import yieldgrid.model.Farmer;
import yieldgrid.model.User;
import yieldgrid.util.PasswordUtil;

/*
 * COURSE CONCEPT:
 * JDBC, PreparedStatement, ResultSet, SQL CRUD (Create, Read, Update, Delete),
 * Polymorphism, Nested Classes (Static Nested Class), Exception Handling
 *
 * PURPOSE:
 * UserDAO (Data Access Object) handles all persistent database interactions
 * for User accounts, including registration, authentication, user profile updates,
 * password modification, and administrative user account queries.
 */

public class UserDAO {

    // NESTED CLASS CONCEPT: Static Nested Class (UNIT-I)
    // Encapsulates filter criteria parameters for user search operations
    public static class UserFilterCriteria {
        private final String searchQuery;
        private final String roleFilter;
        private final Boolean activeOnly;

        public UserFilterCriteria(String searchQuery, String roleFilter, Boolean activeOnly) {
            this.searchQuery = searchQuery;
            this.roleFilter = roleFilter;
            this.activeOnly = activeOnly;
        }

        public String getSearchQuery() { return searchQuery; }
        public String getRoleFilter() { return roleFilter; }
        public Boolean getActiveOnly() { return activeOnly; }
    }

    // CRUD CONCEPT: CREATE (INSERT)
    // PreparedStatement: Uses parameterised queries to insert new user records securely with hashed passwords
    public boolean registerUser(User user) throws SQLException {
        String sql = "INSERT INTO users (name, username, password, role, contact_info, is_active) VALUES (?, ?, ?, ?, ?, ?);";

        // JDBC CONCEPT: Connection & try-with-resources
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql, Statement.RETURN_GENERATED_KEYS)) {

            // SECURITY: Ensure password is cryptographically hashed with SHA-256
            String rawPassword = user.getPassword();
            String hashedPassword = PasswordUtil.isHashed(rawPassword) ? rawPassword : PasswordUtil.hashPassword(rawPassword);
            user.setPassword(hashedPassword);

            // PreparedStatement Parameter Binding:
            pstmt.setString(1, user.getName());
            pstmt.setString(2, user.getUsername());
            pstmt.setString(3, hashedPassword);
            pstmt.setString(4, user.getRole());
            pstmt.setString(5, user.getContactInfo());
            pstmt.setBoolean(6, user.isActive());

            int affectedRows = pstmt.executeUpdate();
            if (affectedRows > 0) {
                // DATABASE RETRIEVAL: Retrieve auto-generated primary key
                try (ResultSet generatedKeys = pstmt.getGeneratedKeys()) {
                    if (generatedKeys.next()) {
                        user.setUserId(generatedKeys.getInt(1));
                    }
                }
                return true;
            }
            return false;
        }
    }

    // CRUD CONCEPT: READ (SELECT & AUTHENTICATE)
    // Authenticates user credentials using secure SHA-256 verification and returns polymorphic User subclass
    public User authenticate(String username, String password) throws SQLException {
        String sql = "SELECT user_id, name, username, password, role, contact_info, is_active FROM users WHERE username = ?;";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setString(1, username);

            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    String storedPassword = rs.getString("password");
                    // SECURITY: Verify password using salted PBKDF2 with legacy fallback
                    if (PasswordUtil.verifyPassword(password, storedPassword)) {
                        // Smooth upgrade: if legacy SHA-256 or plaintext, upgrade to salted PBKDF2
                        if (PasswordUtil.needsMigration(storedPassword)) {
                            updatePassword(rs.getInt("user_id"), PasswordUtil.hashPassword(password));
                        }
                        return mapRowToUser(rs);
                    }
                }
            }
        }
        return null;
    }

    // CRUD CONCEPT: READ (SELECT)
    // Checks if a username is already taken during registration
    public boolean isUsernameTaken(String username) throws SQLException {
        String sql = "SELECT COUNT(*) FROM users WHERE username = ?;";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setString(1, username);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    return rs.getInt(1) > 0;
                }
            }
        }
        return false;
    }

    // CRUD CONCEPT: READ (SELECT)
    // Fetches a User by their unique ID
    public User getUserById(int userId) throws SQLException {
        String sql = "SELECT user_id, name, username, password, role, contact_info, is_active FROM users WHERE user_id = ?;";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setInt(1, userId);
            try (ResultSet rs = pstmt.executeQuery()) {
                if (rs.next()) {
                    return mapRowToUser(rs);
                }
            }
        }
        return null;
    }

    // CRUD CONCEPT: UPDATE (USER PROFILE PERSISTENCE)
    // Updates user details in MySQL database; changes persist after logout and application restart
    public boolean updateUser(User user) throws SQLException {
        String sql = "UPDATE users SET name = ?, contact_info = ?, role = ?, is_active = ? WHERE user_id = ?;";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setString(1, user.getName());
            pstmt.setString(2, user.getContactInfo());
            pstmt.setString(3, user.getRole());
            pstmt.setBoolean(4, user.isActive());
            pstmt.setInt(5, user.getUserId());

            return pstmt.executeUpdate() > 0;
        }
    }

    // CRUD CONCEPT: UPDATE (PASSWORD MODIFICATION)
    // Updates hashed password for user account
    public boolean updatePassword(int userId, String hashedNewPassword) throws SQLException {
        String sql = "UPDATE users SET password = ? WHERE user_id = ?;";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setString(1, hashedNewPassword);
            pstmt.setInt(2, userId);

            return pstmt.executeUpdate() > 0;
        }
    }

    // CRUD CONCEPT: UPDATE (ACCOUNT ACTIVATION / DEACTIVATION)
    public boolean setUserActiveStatus(int userId, boolean active) throws SQLException {
        String sql = "UPDATE users SET is_active = ? WHERE user_id = ?;";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setBoolean(1, active);
            pstmt.setInt(2, userId);

            return pstmt.executeUpdate() > 0;
        }
    }

    // CRUD CONCEPT: READ (SELECT ALL USERS FOR ADMIN MANAGEMENT)
    public ArrayList<User> getAllUsers() throws SQLException {
        String sql = "SELECT user_id, name, username, password, role, contact_info, is_active FROM users ORDER BY user_id ASC;";
        ArrayList<User> users = new ArrayList<>();

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql);
             ResultSet rs = pstmt.executeQuery()) {

            while (rs.next()) {
                users.add(mapRowToUser(rs));
            }
        }
        return users;
    }

    // CRUD CONCEPT: READ (SEARCH & FILTER USERS USING NESTED CRITERIA)
    public ArrayList<User> searchUsers(UserFilterCriteria criteria) throws SQLException {
        StringBuilder sql = new StringBuilder("SELECT user_id, name, username, password, role, contact_info, is_active FROM users WHERE 1=1 ");

        if (criteria != null) {
            if (criteria.getRoleFilter() != null && !criteria.getRoleFilter().equalsIgnoreCase("ALL")) {
                sql.append(" AND role = ? ");
            }
            if (criteria.getActiveOnly() != null && criteria.getActiveOnly()) {
                sql.append(" AND is_active = TRUE ");
            }
            if (criteria.getSearchQuery() != null && !criteria.getSearchQuery().trim().isEmpty()) {
                sql.append(" AND (LOWER(name) LIKE ? OR LOWER(username) LIKE ? OR LOWER(contact_info) LIKE ?) ");
            }
        }
        sql.append(" ORDER BY user_id ASC;");

        ArrayList<User> users = new ArrayList<>();
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql.toString())) {

            int paramIndex = 1;
            if (criteria != null) {
                if (criteria.getRoleFilter() != null && !criteria.getRoleFilter().equalsIgnoreCase("ALL")) {
                    pstmt.setString(paramIndex++, criteria.getRoleFilter().toUpperCase());
                }
                if (criteria.getSearchQuery() != null && !criteria.getSearchQuery().trim().isEmpty()) {
                    String queryPattern = "%" + criteria.getSearchQuery().trim().toLowerCase() + "%";
                    pstmt.setString(paramIndex++, queryPattern);
                    pstmt.setString(paramIndex++, queryPattern);
                    pstmt.setString(paramIndex++, queryPattern);
                }
            }

            try (ResultSet rs = pstmt.executeQuery()) {
                while (rs.next()) {
                    users.add(mapRowToUser(rs));
                }
            }
        }
        return users;
    }

    // AUDIT & SAFETY: Count active administrators to prevent lockout
    public int getActiveAdminCount() throws SQLException {
        String sql = "SELECT COUNT(*) FROM users WHERE role = 'ADMIN' AND is_active = TRUE;";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql);
             ResultSet rs = pstmt.executeQuery()) {

            if (rs.next()) {
                return rs.getInt(1);
            }
        }
        return 0;
    }

    // OOP CONCEPT: Polymorphism / Factory Mapping
    // Returns concrete subclass instance (AdminUser, Farmer, Customer) referenced through base class User
    private User mapRowToUser(ResultSet rs) throws SQLException {
        int id = rs.getInt("user_id");
        String name = rs.getString("name");
        String uname = rs.getString("username");
        String pass = rs.getString("password");
        String role = rs.getString("role");
        String contact = rs.getString("contact_info");

        // Safely retrieve is_active (defaults to true if column unavailable)
        boolean active = true;
        try {
            active = rs.getBoolean("is_active");
        } catch (SQLException ignored) {
            active = true;
        }

        // CONDITIONAL LOGIC & POLYMORPHISM:
        // Demonstrates assigning concrete subclass objects to a User superclass reference
        User user;
        if ("ADMIN".equalsIgnoreCase(role)) {
            user = new AdminUser(id, name, uname, pass, contact, active);
        } else if ("FARMER".equalsIgnoreCase(role)) {
            user = new Farmer(id, name, uname, pass, contact, active);
        } else {
            user = new Customer(id, name, uname, pass, contact, active);
        }
        return user;
    }
}
