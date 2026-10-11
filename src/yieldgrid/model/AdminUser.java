package yieldgrid.model;

/*
 * COURSE CONCEPT:
 * Inheritance (Specialization), Polymorphism (Method Overriding), Super Keyword, Final Keyword
 *
 * PURPOSE:
 * AdminUser represents an authorized system administrator in YieldGrid.
 * Similar to Django's superuser, AdminUser inherits all base User attributes
 * while obtaining central management authority over platform data, accounts,
 * crop listings, and customer orders.
 */

// OOP CONCEPT: Inheritance (Specialization & Extension)
// AdminUser specializes the abstract User class to provide administrative identity and behavior
public class AdminUser extends User {

    // Final constant specifying administrative privilege level
    private static final String ADMIN_PRIVILEGE_LEVEL = "FULL_ACCESS";

    // OOP CONCEPT: Constructor & super Keyword
    // Calls superclass constructor to initialize all base account fields
    public AdminUser(int userId, String name, String username, String password, String contactInfo, boolean active) {
        super(userId, name, username, password, "ADMIN", contactInfo, active);
    }

    // Constructor overloading with default active status
    public AdminUser(int userId, String name, String username, String password, String contactInfo) {
        this(userId, name, username, password, contactInfo, true);
    }

    // Constructor overloading for programmatic administrator creation
    public AdminUser(String name, String username, String password, String contactInfo) {
        super(name, username, password, "ADMIN", contactInfo);
    }

    // OOP CONCEPT: Polymorphism & Method Overriding
    // Implements abstract method defined in User base class
    @Override
    public String getRoleDescription() {
        return "Administrator: Central system oversight, account moderation, catalog curation, and order auditing.";
    }

    // OOP CONCEPT: Method Overriding
    @Override
    public String getDashboardTitle() {
        return "YieldGrid — Central Administration Console";
    }

    // ENCAPSULATION & FINAL KEYWORD:
    // Getter returning administrative privilege level
    public final String getPrivilegeLevel() {
        return ADMIN_PRIVILEGE_LEVEL;
    }
}
