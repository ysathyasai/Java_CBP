package yieldgrid.service;

import java.sql.SQLException;
import yieldgrid.dao.UserDAO;
import yieldgrid.exception.AuthenticationException;
import yieldgrid.exception.ValidationException;
import yieldgrid.model.Customer;
import yieldgrid.model.Farmer;
import yieldgrid.model.User;
import yieldgrid.util.PasswordUtil;

/*
 * COURSE CONCEPT:
 * Business Validation, Exception Handling, Polymorphism, String Handling, Encapsulation
 *
 * PURPOSE:
 * AuthenticationService enforces business rules for user registration, login,
 * account profile modifications, and secure password updates, ensuring strict
 * separation between the Swing presentation layer and direct database operations.
 */

public class AuthenticationService {

    private final UserDAO userDAO;

    public AuthenticationService() {
        this.userDAO = new UserDAO();
    }

    // Constructor injection for testing
    public AuthenticationService(UserDAO userDAO) {
        this.userDAO = userDAO;
    }

    // BUSINESS LOGIC & VALIDATION:
    // Throws ValidationException when input is malformed, and AuthenticationException on invalid credentials
    public User login(String username, String password) throws ValidationException, AuthenticationException {
        // STRING HANDLING & VALIDATION:
        if (username == null || username.trim().isEmpty()) {
            throw new ValidationException("Username cannot be empty.");
        }
        if (password == null || password.trim().isEmpty()) {
            throw new ValidationException("Password cannot be empty.");
        }

        try {
            User user = userDAO.authenticate(username.trim(), password.trim());
            if (user == null) {
                // EXCEPTION HANDLING: Custom AuthenticationException thrown on credential mismatch
                throw new AuthenticationException("Invalid username or password. Please verify your credentials.");
            }

            // ACCESS CONTROL & STATUS VERIFICATION:
            if (!user.isActive()) {
                throw new AuthenticationException("Your account has been deactivated. Please contact an administrator.");
            }

            // Set session
            SessionManager.setCurrentUser(user);
            return user;
        } catch (SQLException e) {
            throw new AuthenticationException("Database communication error during authentication: " + e.getMessage(), e);
        }
    }

    // BUSINESS LOGIC & VALIDATION:
    // Registers a new Farmer or Customer after strict validation checks
    public User register(String name, String username, String password, String role, String contactInfo)
            throws ValidationException, AuthenticationException {

        // STRING HANDLING & INPUT VALIDATION:
        if (name == null || name.trim().isEmpty()) {
            throw new ValidationException("Full name is required.");
        }
        if (username == null || username.trim().length() < 3) {
            throw new ValidationException("Username must be at least 3 characters long.");
        }
        if (password == null || password.trim().length() < 4) {
            throw new ValidationException("Password must be at least 4 characters long.");
        }
        if (role == null || (!role.equalsIgnoreCase("FARMER") && !role.equalsIgnoreCase("CUSTOMER"))) {
            throw new ValidationException("Role must be specified as either FARMER or CUSTOMER.");
        }

        try {
            if (userDAO.isUsernameTaken(username.trim())) {
                throw new ValidationException("The username '" + username.trim() + "' is already registered. Please choose another.");
            }

            // OOP CONCEPT: Polymorphism / Subclass instantiation
            User newUser;
            if ("FARMER".equalsIgnoreCase(role.trim())) {
                newUser = new Farmer(name.trim(), username.trim(), password.trim(), contactInfo != null ? contactInfo.trim() : "");
            } else {
                newUser = new Customer(name.trim(), username.trim(), password.trim(), contactInfo != null ? contactInfo.trim() : "");
            }

            boolean success = userDAO.registerUser(newUser);
            if (!success) {
                throw new AuthenticationException("Failed to save user account to database.");
            }

            return newUser;
        } catch (SQLException e) {
            throw new AuthenticationException("Database error during registration: " + e.getMessage(), e);
        }
    }

    // PROFILE PERSISTENCE:
    // Updates user details in MySQL; changes persist across logout and application restarts
    public boolean updateProfile(User user, String newName, String newContactInfo)
            throws ValidationException, AuthenticationException {

        if (user == null) {
            throw new ValidationException("User session is invalid.");
        }
        if (newName == null || newName.trim().isEmpty()) {
            throw new ValidationException("Full name cannot be blank.");
        }

        user.setName(newName.trim());
        user.setContactInfo(newContactInfo != null ? newContactInfo.trim() : "");

        try {
            boolean updated = userDAO.updateUser(user);
            if (!updated) {
                throw new AuthenticationException("Failed to persist updated profile to the database.");
            }
            return true;
        } catch (SQLException e) {
            throw new AuthenticationException("Database error during profile update: " + e.getMessage(), e);
        }
    }

    // SECURE PASSWORD CHANGE:
    // Explicit password update flow enforcing current password check and new password rules
    public boolean changePassword(int userId, String currentPassword, String newPassword, String confirmPassword)
            throws ValidationException, AuthenticationException {

        if (currentPassword == null || currentPassword.isEmpty()) {
            throw new ValidationException("Current password must be provided.");
        }
        if (newPassword == null || newPassword.length() < 4) {
            throw new ValidationException("New password must be at least 4 characters long.");
        }
        if (!newPassword.equals(confirmPassword)) {
            throw new ValidationException("New password and confirmation do not match.");
        }

        try {
            User existing = userDAO.getUserById(userId);
            if (existing == null) {
                throw new AuthenticationException("User account not found.");
            }
            if (!PasswordUtil.verifyPassword(currentPassword, existing.getPassword())) {
                throw new ValidationException("Current password entered is incorrect.");
            }

            String hashedNew = PasswordUtil.hashPassword(newPassword);
            boolean updated = userDAO.updatePassword(userId, hashedNew);
            if (updated) {
                existing.setPassword(hashedNew);
            }
            return updated;
        } catch (SQLException e) {
            throw new AuthenticationException("Database error during password modification: " + e.getMessage(), e);
        }
    }
}
