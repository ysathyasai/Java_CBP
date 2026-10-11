package yieldgrid.dao;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;
import yieldgrid.database.DBConnection;
import yieldgrid.model.Crop;
import yieldgrid.model.Order;
import yieldgrid.model.OrderStatus;

/*
 * COURSE CONCEPT:
 * JDBC, SQL Aggregations, Collections (Map, List), Database Queries, PreparedStatement
 *
 * PURPOSE:
 * AdminDAO handles central data queries and management operations across all
 * system tables (users, crops, orders, order_items), providing underlying persistence
 * for the Django-Admin style YieldGrid Administration Console.
 */

public class AdminDAO {

    private final OrderDAO orderDAO = new OrderDAO();

    // SQL AGGREGATION & REPORTING (COLLECTIONS: Map / LinkedHashMap - UNIT-IV)
    // Computes aggregate system statistics directly from MySQL database tables
    public Map<String, Object> getSystemMetrics() throws SQLException {
        Map<String, Object> metrics = new LinkedHashMap<>();

        String sqlUsers = "SELECT "
                + "COUNT(*) AS total_users, "
                + "SUM(CASE WHEN role = 'FARMER' AND is_active = TRUE THEN 1 ELSE 0 END) AS active_farmers, "
                + "SUM(CASE WHEN role = 'CUSTOMER' AND is_active = TRUE THEN 1 ELSE 0 END) AS active_customers, "
                + "SUM(CASE WHEN role = 'ADMIN' AND is_active = TRUE THEN 1 ELSE 0 END) AS active_admins, "
                + "SUM(CASE WHEN is_active = FALSE THEN 1 ELSE 0 END) AS inactive_users "
                + "FROM users;";

        String sqlCrops = "SELECT COUNT(*) AS total_crops, "
                + "SUM(CASE WHEN available = TRUE AND quantity > 0 THEN 1 ELSE 0 END) AS active_listings, "
                + "COALESCE(SUM(quantity), 0) AS total_inventory_units "
                + "FROM crops;";

        String sqlOrders = "SELECT COUNT(*) AS total_orders, "
                + "SUM(CASE WHEN status = 'COMPLETED' THEN 1 ELSE 0 END) AS completed_orders, "
                + "SUM(CASE WHEN status = 'PENDING' THEN 1 ELSE 0 END) AS pending_orders, "
                + "COALESCE(SUM(CASE WHEN status = 'COMPLETED' THEN total_amount ELSE 0 END), 0.0) AS gross_revenue "
                + "FROM orders;";

        try (Connection conn = DBConnection.getConnection();
             Statement stmt = conn.createStatement()) {

            try (ResultSet rs = stmt.executeQuery(sqlUsers)) {
                if (rs.next()) {
                    metrics.put("totalUsers", rs.getInt("total_users"));
                    metrics.put("activeFarmers", rs.getInt("active_farmers"));
                    metrics.put("activeCustomers", rs.getInt("active_customers"));
                    metrics.put("activeAdmins", rs.getInt("active_admins"));
                    metrics.put("inactiveUsers", rs.getInt("inactive_users"));
                }
            }

            try (ResultSet rs = stmt.executeQuery(sqlCrops)) {
                if (rs.next()) {
                    metrics.put("totalCrops", rs.getInt("total_crops"));
                    metrics.put("activeListings", rs.getInt("active_listings"));
                    metrics.put("totalInventoryUnits", rs.getInt("total_inventory_units"));
                }
            }

            try (ResultSet rs = stmt.executeQuery(sqlOrders)) {
                if (rs.next()) {
                    metrics.put("totalOrders", rs.getInt("total_orders"));
                    metrics.put("completedOrders", rs.getInt("completed_orders"));
                    metrics.put("pendingOrders", rs.getInt("pending_orders"));
                    metrics.put("grossRevenue", rs.getDouble("gross_revenue"));
                }
            }
        }
        return metrics;
    }

    // CRUD CONCEPT: READ (ALL CROPS ACROSS FARMERS)
    // Allows administrator to inspect all crops regardless of owner
    public ArrayList<Crop> getAllCropsAcrossFarmers() throws SQLException {
        String sql = "SELECT c.crop_id, c.farmer_id, u.name AS farmer_name, c.crop_name, "
                   + "c.description, c.quantity, c.price, c.available "
                   + "FROM crops c "
                   + "JOIN users u ON c.farmer_id = u.user_id "
                   + "ORDER BY c.crop_id DESC;";

        ArrayList<Crop> list = new ArrayList<>();
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql);
             ResultSet rs = pstmt.executeQuery()) {

            while (rs.next()) {
                list.add(new Crop(
                    rs.getInt("crop_id"),
                    rs.getInt("farmer_id"),
                    rs.getString("farmer_name"),
                    rs.getString("crop_name"),
                    rs.getString("description"),
                    rs.getInt("quantity"),
                    rs.getDouble("price"),
                    rs.getBoolean("available")
                ));
            }
        }
        return list;
    }

    // CRUD CONCEPT: UPDATE (ADMINISTRATIVE CROP OVERRIDE)
    public boolean updateCropAsAdmin(Crop crop) throws SQLException {
        String sql = "UPDATE crops SET crop_name = ?, description = ?, quantity = ?, price = ?, available = ? WHERE crop_id = ?;";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setString(1, crop.getCropName());
            pstmt.setString(2, crop.getDescription());
            pstmt.setInt(3, crop.getQuantity());
            pstmt.setDouble(4, crop.getPrice());
            boolean avail = crop.isAvailable() && crop.getQuantity() > 0;
            pstmt.setBoolean(5, avail);
            pstmt.setInt(6, crop.getCropId());

            return pstmt.executeUpdate() > 0;
        }
    }

    // CRUD CONCEPT: UPDATE (TOGGLE CROP AVAILABILITY)
    public boolean toggleCropAvailability(int cropId, boolean available) throws SQLException {
        String sql = "UPDATE crops SET available = ? WHERE crop_id = ?;";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setBoolean(1, available);
            pstmt.setInt(2, cropId);

            return pstmt.executeUpdate() > 0;
        }
    }

    // CRUD CONCEPT: READ (ALL ORDERS ACROSS PLATFORM)
    public ArrayList<Order> getAllOrdersAcrossPlatform() throws SQLException {
        String sql = "SELECT o.order_id, o.customer_id, u_cust.name AS customer_name, "
                   + "o.farmer_id, u_farm.name AS farmer_name, o.order_date, o.total_amount, o.status "
                   + "FROM orders o "
                   + "JOIN users u_cust ON o.customer_id = u_cust.user_id "
                   + "JOIN users u_farm ON o.farmer_id = u_farm.user_id "
                   + "ORDER BY o.order_id DESC;";

        ArrayList<Order> list = new ArrayList<>();
        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql);
             ResultSet rs = pstmt.executeQuery()) {

            while (rs.next()) {
                Order order = new Order(
                    rs.getInt("order_id"),
                    rs.getInt("customer_id"),
                    rs.getString("customer_name"),
                    rs.getInt("farmer_id"),
                    rs.getString("farmer_name"),
                    rs.getTimestamp("order_date"),
                    rs.getDouble("total_amount"),
                    OrderStatus.fromString(rs.getString("status"))
                );
                order.setItems(orderDAO.getOrderItems(order.getOrderId()));
                list.add(order);
            }
        }
        return list;
    }

    // CRUD CONCEPT: UPDATE (ADMINISTRATIVE ORDER STATUS UPDATE)
    public boolean updateOrderStatusAsAdmin(int orderId, OrderStatus newStatus) throws SQLException {
        String sql = "UPDATE orders SET status = ? WHERE order_id = ?;";

        try (Connection conn = DBConnection.getConnection();
             PreparedStatement pstmt = conn.prepareStatement(sql)) {

            pstmt.setString(1, newStatus.name());
            pstmt.setInt(2, orderId);

            return pstmt.executeUpdate() > 0;
        }
    }
}
