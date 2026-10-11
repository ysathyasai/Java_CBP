package yieldgrid.model;

/*
 * COURSE CONCEPT:
 * Abstract Classes, Encapsulation, Constructors, Polymorphism
 *
 * PURPOSE:
 * User is the abstract base class representing all human actors in YieldGrid.
 * It encapsulates common credentials, identity, and contact information shared
 * by both Farmers and Customers, establishing an OOP inheritance hierarchy.
 */

// OOP CONCEPT: Abstract Class
// The User class cannot be instantiated directly because every user in YieldGrid
// must be either a Farmer or a Customer with role-specific behaviour.
public abstract class User {

    // OOP CONCEPT: Encapsulation
    // All instance variables are declared private to protect internal state.
    // Outside classes must interact through defined getter and setter methods.
    private int userId;
    private String name;
    private String username;
    private String password;
    private String role;
    private String contactInfo;
    private boolean active = true;

    // OOP CONCEPT: Constructor
    // Parameterized constructor to initialize common state when creating user instances
    public User(int userId, String name, String username, String password, String role, String contactInfo, boolean active) {
        this.userId = userId;
        this.name = name;
        this.username = username;
        this.password = password;
        this.role = role;
        this.contactInfo = contactInfo;
        this.active = active;
    }

    // OOP CONCEPT: Constructor Overloading
    // Overloaded constructor with active defaulting to true
    public User(int userId, String name, String username, String password, String role, String contactInfo) {
        this(userId, name, username, password, role, contactInfo, true);
    }

    // OOP CONCEPT: Constructor Overloading
    // Overloaded constructor for new registrations where database auto-generates the userId
    public User(String name, String username, String password, String role, String contactInfo) {
        this(0, name, username, password, role, contactInfo, true);
    }

    // OOP CONCEPT: Polymorphism / Abstract Method
    // Subclasses (Farmer, Customer, AdminUser) MUST provide their own implementation of role description
    public abstract String getRoleDescription();

    // OOP CONCEPT: Polymorphism / Abstract Method
    // Subclasses define their specific title shown on their respective dashboard headers
    public abstract String getDashboardTitle();

    // OOP CONCEPT: Encapsulation - Getters and Setters
    public int getUserId() {
        return userId;
    }

    public void setUserId(int userId) {
        this.userId = userId;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getRole() {
        return role;
    }

    public void setRole(String role) {
        this.role = role;
    }

    public String getContactInfo() {
        return contactInfo;
    }

    public void setContactInfo(String contactInfo) {
        this.contactInfo = contactInfo;
    }

    public boolean isActive() {
        return active;
    }

    public void setActive(boolean active) {
        this.active = active;
    }

    // OBJECT CLASS: Overriding equals() to compare users by their unique userId and username
    @Override
    public boolean equals(Object obj) {
        if (this == obj) return true;
        if (obj == null || getClass() != obj.getClass()) return false;
        User other = (User) obj;
        return userId == other.userId && (username != null ? username.equals(other.username) : other.username == null);
    }

    // OBJECT CLASS: Overriding hashCode() consistent with equals()
    @Override
    public int hashCode() {
        int result = Integer.hashCode(userId);
        result = 31 * result + (username != null ? username.hashCode() : 0);
        return result;
    }

    // STRING HANDLING & OBJECT CLASS:
    // Overridden toString() method returning a formatted summary of user profile
    @Override
    public String toString() {
        return "User [ID=" + userId + ", Name=" + name + ", Username=" + username + ", Role=" + role + ", Active=" + active + "]";
    }
}
