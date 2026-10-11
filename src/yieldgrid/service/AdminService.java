package yieldgrid.service;

import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Map;
import yieldgrid.dao.AdminDAO;
import yieldgrid.dao.UserDAO;
import yieldgrid.exception.ValidationException;
import yieldgrid.model.Crop;
import yieldgrid.model.Order;
import yieldgrid.model.OrderStatus;
import yieldgrid.model.User;

/*
 * COURSE CONCEPT:
 * Access Control, Business Rules, Validation, Collections (Map, List), Exception Handling
 *
 * PURPOSE:
 * AdminService enforces centralized administration business logic.
 * Every administrative operation verifies that the invoking user is authenticated
 * with the ADMIN role, protecting user accounts, inventory records, and order integrity.
 */

public class AdminService {

    private final AdminDAO adminDAO;
    private final UserDAO userDAO;

    public AdminService() {
        this.adminDAO = new AdminDAO();
        this.userDAO = new UserDAO();
    }

    public AdminService(AdminDAO adminDAO, UserDAO userDAO) {
        this.adminDAO = adminDAO;
        this.userDAO = userDAO;
    }

    // ACCESS CONTROL: Enforce administrator authorization
    public void requireAdminAccess() throws ValidationException {
        if (!SessionManager.isLoggedIn() || !SessionManager.isAdmin()) {
            throw new ValidationException("Access Denied: Only users with the ADMIN role can perform administrative operations.");
        }
    }

    // PLATFORM METRICS:
    public Map<String, Object> getSystemMetrics() throws ValidationException, SQLException {
        requireAdminAccess();
        return adminDAO.getSystemMetrics();
    }

    // USER MANAGEMENT: Search & filter accounts
    public ArrayList<User> searchUsers(String query, String roleFilter) throws ValidationException, SQLException {
        requireAdminAccess();
        UserDAO.UserFilterCriteria criteria = new UserDAO.UserFilterCriteria(query, roleFilter, null);
        return userDAO.searchUsers(criteria);
    }

    // USER MANAGEMENT: Toggle account active status with lockout prevention
    public boolean toggleUserActiveStatus(int targetUserId) throws ValidationException, SQLException {
        requireAdminAccess();

        User targetUser = userDAO.getUserById(targetUserId);
        if (targetUser == null) {
            throw new ValidationException("User account ID " + targetUserId + " does not exist.");
        }

        // SAFETY RULE: Prevent deactivating the last active administrator
        if ("ADMIN".equalsIgnoreCase(targetUser.getRole()) && targetUser.isActive()) {
            int activeAdmins = userDAO.getActiveAdminCount();
            if (activeAdmins <= 1) {
                throw new ValidationException("Cannot deactivate administrator: At least one active Administrator account must remain.");
            }
        }

        boolean newStatus = !targetUser.isActive();
        return userDAO.setUserActiveStatus(targetUserId, newStatus);
    }

    // USER MANAGEMENT: Edit account details
    public boolean updateUserDetails(int targetUserId, String name, String contactInfo, String role, boolean active)
            throws ValidationException, SQLException {
        requireAdminAccess();

        if (name == null || name.trim().isEmpty()) {
            throw new ValidationException("Name cannot be empty.");
        }
        if (role == null || (!role.equalsIgnoreCase("ADMIN") && !role.equalsIgnoreCase("FARMER") && !role.equalsIgnoreCase("CUSTOMER"))) {
            throw new ValidationException("Role must be ADMIN, FARMER, or CUSTOMER.");
        }

        User targetUser = userDAO.getUserById(targetUserId);
        if (targetUser == null) {
            throw new ValidationException("Target user not found.");
        }

        // Safety check if changing role away from ADMIN
        if ("ADMIN".equalsIgnoreCase(targetUser.getRole()) && !role.equalsIgnoreCase("ADMIN") && targetUser.isActive()) {
            int activeAdmins = userDAO.getActiveAdminCount();
            if (activeAdmins <= 1) {
                throw new ValidationException("Cannot revoke admin privileges: At least one active Administrator must remain.");
            }
        }

        targetUser.setName(name.trim());
        targetUser.setContactInfo(contactInfo != null ? contactInfo.trim() : "");
        targetUser.setRole(role.toUpperCase());
        targetUser.setActive(active);

        return userDAO.updateUser(targetUser);
    }

    // CROP MANAGEMENT: List all crops across farmers
    public ArrayList<Crop> getAllCrops(String searchQuery) throws ValidationException, SQLException {
        requireAdminAccess();
        ArrayList<Crop> all = adminDAO.getAllCropsAcrossFarmers();
        if (searchQuery == null || searchQuery.trim().isEmpty()) {
            return all;
        }

        String q = searchQuery.trim().toLowerCase();
        ArrayList<Crop> filtered = new ArrayList<>();
        for (Crop c : all) {
            if (c.getCropName().toLowerCase().contains(q) ||
                c.getFarmerName().toLowerCase().contains(q) ||
                c.getDescription().toLowerCase().contains(q)) {
                filtered.add(c);
            }
        }
        return filtered;
    }

    // CROP MANAGEMENT: Administrative update
    public boolean updateCrop(Crop crop) throws ValidationException, SQLException {
        requireAdminAccess();
        if (crop == null) {
            throw new ValidationException("Crop details cannot be null.");
        }
        if (crop.getQuantity() < 0) {
            throw new ValidationException("Quantity cannot be negative.");
        }
        if (crop.getPrice() <= 0) {
            throw new ValidationException("Price must be greater than zero.");
        }
        return adminDAO.updateCropAsAdmin(crop);
    }

    // CROP MANAGEMENT: Toggle crop availability
    public boolean toggleCropAvailability(int cropId, boolean available) throws ValidationException, SQLException {
        requireAdminAccess();
        return adminDAO.toggleCropAvailability(cropId, available);
    }

    // ORDER MANAGEMENT: List all orders across platform
    public ArrayList<Order> getAllOrders(String statusFilter) throws ValidationException, SQLException {
        requireAdminAccess();
        ArrayList<Order> all = adminDAO.getAllOrdersAcrossPlatform();
        if (statusFilter == null || statusFilter.equalsIgnoreCase("ALL")) {
            return all;
        }

        ArrayList<Order> filtered = new ArrayList<>();
        for (Order o : all) {
            if (o.getStatus().name().equalsIgnoreCase(statusFilter)) {
                filtered.add(o);
            }
        }
        return filtered;
    }

    // ORDER MANAGEMENT: Administrative status update
    public boolean updateOrderStatus(int orderId, OrderStatus newStatus) throws ValidationException, SQLException {
        requireAdminAccess();
        if (newStatus == null) {
            throw new ValidationException("Order status cannot be null.");
        }
        return adminDAO.updateOrderStatusAsAdmin(orderId, newStatus);
    }
}
