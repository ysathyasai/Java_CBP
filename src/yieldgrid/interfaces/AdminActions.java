package yieldgrid.interfaces;

/*
 * COURSE CONCEPT:
 * Interfaces, Extending Interfaces (Interface Inheritance), Polymorphism
 *
 * PURPOSE:
 * AdminActions extends DashboardActions, demonstrating interface inheritance in Java.
 * An interface can extend another interface using the 'extends' keyword, inheriting all
 * abstract method declarations while adding role-specific contracts for system administration.
 */

// OOP CONCEPT: Extending Interfaces
// AdminActions inherits refreshData(), showProfile(), and logout() from DashboardActions
// and introduces administrator-specific operational contracts.
public interface AdminActions extends DashboardActions {

    // Additional contract methods specific to administrative management
    void auditUserAccounts();

    void viewSystemMetrics();

    void exportAuditReport();
}
