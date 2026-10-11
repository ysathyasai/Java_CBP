package yieldgrid.ui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.GridLayout;
import java.awt.Insets;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import java.io.IOException;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Map;
import javax.swing.BorderFactory;
import javax.swing.ButtonGroup;
import javax.swing.JButton;
import javax.swing.JCheckBox;
import javax.swing.JCheckBoxMenuItem;
import javax.swing.JComboBox;
import javax.swing.JDialog;
import javax.swing.JFileChooser;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JMenu;
import javax.swing.JMenuBar;
import javax.swing.JMenuItem;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPopupMenu;
import javax.swing.JRadioButtonMenuItem;
import javax.swing.JScrollPane;
import javax.swing.JSeparator;
import javax.swing.JSpinner;
import javax.swing.JTabbedPane;
import javax.swing.JTable;
import javax.swing.JTextField;
import javax.swing.JTree;
import javax.swing.SpinnerNumberModel;
import javax.swing.SwingConstants;
import javax.swing.event.ChangeEvent;
import javax.swing.event.ChangeListener;
import javax.swing.table.DefaultTableModel;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import yieldgrid.exception.ValidationException;
import yieldgrid.interfaces.AdminActions;
import yieldgrid.model.AdminUser;
import yieldgrid.model.Crop;
import yieldgrid.model.Order;
import yieldgrid.model.OrderItem;
import yieldgrid.model.OrderStatus;
import yieldgrid.model.User;
import yieldgrid.service.AdminService;
import yieldgrid.service.SessionManager;
import yieldgrid.util.DataExporter;

/*
 * COURSE CONCEPT:
 * UNIT-V: Java Swing Components and Containers (JFrame, JComponent, JLabel, JTextField, JButton,
 * JCheckBox, JRadioButton, JComboBox, JTable, Trees [JTree], Menus [JMenuBar, JMenu, JMenuItem,
 * JCheckBoxMenuItem, JRadioButtonMenuItem, JSeparator, JPopupMenu]), MVC Architecture.
 * UNIT-II: Extending Interfaces (implements AdminActions extends DashboardActions), Polymorphism.
 * UNIT-IV: Delegation Event Model, Mouse and Keyboard Events, Adapter Classes, Layout Managers.
 *
 * PURPOSE:
 * AdminDashboard is the central management console for YieldGrid, analogous to Django Admin.
 * It provides administrative role-based oversight of platform users, farmer crops, customer orders,
 * aggregate revenue metrics, and system tree hierarchy.
 */

public class AdminDashboard extends JFrame implements AdminActions {

    private final AdminUser adminUser;
    private final AdminService adminService;

    // GUI Containers & Components
    private JTabbedPane tabbedPane;
    private JLabel lblHeaderTitle;

    // Overview Tab
    private JPanel overviewPanel;
    private JLabel lblMetricUsers;
    private JLabel lblMetricFarmers;
    private JLabel lblMetricCustomers;
    private JLabel lblMetricCrops;
    private JLabel lblMetricOrders;
    private JLabel lblMetricRevenue;

    // Users Tab
    private JTable userTable;
    private DefaultTableModel userTableModel;
    private JTextField txtUserSearch;
    private JComboBox<String> cmbRoleFilter;
    private JPopupMenu userPopupMenu;

    // Crops Tab
    private JTable cropTable;
    private DefaultTableModel cropTableModel;
    private JTextField txtCropSearch;

    // Orders Tab
    private JTable orderTable;
    private DefaultTableModel orderTableModel;
    private JComboBox<String> cmbOrderStatusFilter;

    // Trees Tab
    private JTree hierarchyTree;
    private DefaultTreeModel treeModel;

    // Profile Tab
    private ProfilePanel profilePanel;

    public AdminDashboard(AdminUser adminUser) {
        this.adminUser = adminUser;
        this.adminService = new AdminService();
        initializeUI();
    }

    private void initializeUI() {
        setTitle(adminUser.getDashboardTitle());
        setSize(1080, 720);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        // SWING MENUS CONCEPT: JMenuBar, JMenu, JMenuItem, JSeparator, CheckBox &
        // RadioButton Menu Items
        setupMenuBar();

        JPanel mainPanel = new JPanel(new BorderLayout());
        mainPanel.setBackground(UITheme.COLOR_BG);

        // TOP HEADER BAR:
        JPanel headerBar = new JPanel(new BorderLayout());
        headerBar.setBackground(UITheme.COLOR_PRIMARY_DARK);
        headerBar.setBorder(BorderFactory.createEmptyBorder(12, 20, 12, 20));

        lblHeaderTitle = new JLabel("YieldGrid — Central Administration Console");
        lblHeaderTitle.setFont(UITheme.FONT_TITLE);
        lblHeaderTitle.setForeground(Color.WHITE);
        headerBar.add(lblHeaderTitle, BorderLayout.WEST);

        JPanel userSection = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 0));
        userSection.setBackground(UITheme.COLOR_PRIMARY_DARK);

        JLabel lblAdminName = new JLabel("Admin: " + adminUser.getName());
        lblAdminName.setFont(UITheme.FONT_BOLD);
        lblAdminName.setForeground(new Color(220, 237, 200));
        userSection.add(lblAdminName);

        JButton btnProfile = UITheme.createSecondaryButton("Profile");
        btnProfile.addActionListener(e -> showProfile());
        userSection.add(btnProfile);

        JButton btnLogout = UITheme.createDangerButton("Logout");
        btnLogout.addActionListener(e -> logout());
        userSection.add(btnLogout);

        headerBar.add(userSection, BorderLayout.EAST);
        mainPanel.add(headerBar, BorderLayout.NORTH);

        // TABBED PANE FOR MODULES:
        tabbedPane = new JTabbedPane();
        tabbedPane.setFont(UITheme.FONT_BOLD);
        tabbedPane.setBackground(UITheme.COLOR_CARD_BG);

        // Initialize Individual Tabs
        overviewPanel = createOverviewTab();
        JPanel userManagementPanel = createUserManagementTab();
        JPanel cropManagementPanel = createCropManagementTab();
        JPanel orderManagementPanel = createOrderManagementTab();
        JPanel treeHierarchyPanel = createTreeHierarchyTab();
        profilePanel = new ProfilePanel(adminUser, () -> {
            lblAdminName.setText("Admin: " + adminUser.getName());
        });

        tabbedPane.addTab("System Overview", overviewPanel);
        tabbedPane.addTab("User Accounts", userManagementPanel);
        tabbedPane.addTab("Produce Catalog", cropManagementPanel);
        tabbedPane.addTab("Orders Oversight", orderManagementPanel);
        tabbedPane.addTab("Platform Hierarchy", treeHierarchyPanel);
        tabbedPane.addTab("Admin Profile", profilePanel);

        // EVENT HANDLING: Tab change updates view
        tabbedPane.addChangeListener(new ChangeListener() {
            @Override
            public void stateChanged(ChangeEvent e) {
                refreshData();
            }
        });

        mainPanel.add(tabbedPane, BorderLayout.CENTER);
        add(mainPanel);

        // Initial Data Load
        refreshData();
    }

    // SWING CONCEPT: Menus and Menu-Related Classes
    private void setupMenuBar() {
        JMenuBar menuBar = new JMenuBar();

        // 1. File Menu
        JMenu menuFile = new JMenu("File");
        menuFile.setFont(UITheme.FONT_BOLD);

        JMenuItem miRefresh = new JMenuItem("Refresh System Data (F5)");
        miRefresh.addActionListener(e -> refreshData());
        menuFile.add(miRefresh);

        JMenuItem miExportUsers = new JMenuItem("Export Users Directory (CSV)...");
        miExportUsers.addActionListener(e -> exportUsersCsv());
        menuFile.add(miExportUsers);

        JMenuItem miExportOrders = new JMenuItem("Export Orders Report (CSV)...");
        miExportOrders.addActionListener(e -> exportOrdersCsv());
        menuFile.add(miExportOrders);

        menuFile.add(new JSeparator()); // MENU CONCEPT: JSeparator

        JMenuItem miExit = new JMenuItem("Exit Application");
        miExit.addActionListener(e -> logout());
        menuFile.add(miExit);

        // 2. View Menu
        JMenu menuView = new JMenu("View");
        menuView.setFont(UITheme.FONT_BOLD);

        // MENU CONCEPT: JCheckBoxMenuItem
        JCheckBoxMenuItem miActiveOnly = new JCheckBoxMenuItem("Filter Active Only in Tables");
        miActiveOnly.setSelected(false);
        miActiveOnly.addActionListener(e -> loadUsersTable());
        menuView.add(miActiveOnly);

        menuView.add(new JSeparator());

        // MENU CONCEPT: JRadioButtonMenuItem & ButtonGroup
        ButtonGroup themeGroup = new ButtonGroup();
        JRadioButtonMenuItem miThemeDefault = new JRadioButtonMenuItem("Standard Forest Theme", true);
        JRadioButtonMenuItem miThemeHighContrast = new JRadioButtonMenuItem("High Contrast Theme", false);
        themeGroup.add(miThemeDefault);
        themeGroup.add(miThemeHighContrast);
        menuView.add(miThemeDefault);
        menuView.add(miThemeHighContrast);

        // 3. Help Menu
        JMenu menuHelp = new JMenu("Help");
        menuHelp.setFont(UITheme.FONT_BOLD);

        JMenuItem miAbout = new JMenuItem("About YieldGrid Administration Console");
        miAbout.addActionListener(e -> {
            JOptionPane.showMessageDialog(this,
                    "YieldGrid Central Administration Console\n"
                            + "Version: " + SYSTEM_VERSION + "\n"
                            + "Application: " + APPLICATION_NAME + " Farm-to-Retail Inventory\n"
                            + "Role-restricted control panel modeled on Django Admin architecture.",
                    "About YieldGrid Admin",
                    JOptionPane.INFORMATION_MESSAGE);
        });
        menuHelp.add(miAbout);

        menuBar.add(menuFile);
        menuBar.add(menuView);
        menuBar.add(menuHelp);

        setJMenuBar(menuBar);
    }

    // TAB 1: SYSTEM OVERVIEW
    private JPanel createOverviewTab() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(UITheme.COLOR_BG);
        panel.setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        // Metric Cards Grid (LAYOUT MANAGER: GridLayout - UNIT-IV)
        JPanel grid = new JPanel(new GridLayout(2, 3, 16, 16));
        grid.setBackground(UITheme.COLOR_BG);

        lblMetricUsers = new JLabel("0", SwingConstants.CENTER);
        lblMetricFarmers = new JLabel("0", SwingConstants.CENTER);
        lblMetricCustomers = new JLabel("0", SwingConstants.CENTER);
        lblMetricCrops = new JLabel("0", SwingConstants.CENTER);
        lblMetricOrders = new JLabel("0", SwingConstants.CENTER);
        lblMetricRevenue = new JLabel("₹0.00", SwingConstants.CENTER);

        grid.add(createMetricCard("TOTAL REGISTERED USERS", lblMetricUsers, UITheme.COLOR_PRIMARY));
        grid.add(createMetricCard("ACTIVE FARMERS", lblMetricFarmers, UITheme.COLOR_PRIMARY_DARK));
        grid.add(createMetricCard("ACTIVE CUSTOMERS", lblMetricCustomers, UITheme.COLOR_SUCCESS));
        grid.add(createMetricCard("CATALOG CROPS LISTED", lblMetricCrops, UITheme.COLOR_ACCENT));
        grid.add(createMetricCard("PLATFORM ORDERS PLACED", lblMetricOrders, UITheme.COLOR_TEXT_DARK));
        grid.add(createMetricCard("GROSS MARKET REVENUE", lblMetricRevenue, new Color(46, 125, 50)));

        panel.add(grid, BorderLayout.NORTH);

        // System Health & Telemetry Card
        JPanel infoCard = UITheme.createCardPanel();
        infoCard.setLayout(new GridLayout(4, 1, 8, 8));
        infoCard.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createEmptyBorder(20, 0, 0, 0),
                BorderFactory.createEmptyBorder(15, 20, 15, 20)));

        JLabel lblSysTitle = new JLabel("YieldGrid Platform Status & Security Context");
        lblSysTitle.setFont(UITheme.FONT_SUBTITLE);
        lblSysTitle.setForeground(UITheme.COLOR_PRIMARY_DARK);

        JLabel lblDbInfo = new JLabel(
                "• Database Architecture: MySQL Relational Engine via Type-4 Pure Java JDBC Driver (Connector/J)");
        lblDbInfo.setFont(UITheme.FONT_REGULAR);

        JLabel lblSecInfo = new JLabel(
                "• Security Policy: SHA-256 salted password hashing; role-restricted administrative authorization.");
        lblSecInfo.setFont(UITheme.FONT_REGULAR);

        JLabel lblThreadInfo = new JLabel(
                "• Background Services: YieldGrid-Audit-Daemon active in worker ThreadGroup with daemon lifecycle.");
        lblThreadInfo.setFont(UITheme.FONT_REGULAR);

        infoCard.add(lblSysTitle);
        infoCard.add(lblDbInfo);
        infoCard.add(lblSecInfo);
        infoCard.add(lblThreadInfo);

        panel.add(infoCard, BorderLayout.CENTER);
        return panel;
    }

    private JPanel createMetricCard(String title, JLabel valueLabel, Color accentColor) {
        JPanel card = UITheme.createCardPanel();
        card.setLayout(new BorderLayout(8, 8));
        card.setBorder(BorderFactory.createCompoundBorder(
                BorderFactory.createMatteBorder(4, 0, 0, 0, accentColor),
                BorderFactory.createEmptyBorder(12, 14, 12, 14)));

        JLabel lblTitle = new JLabel(title);
        lblTitle.setFont(UITheme.FONT_SMALL);
        lblTitle.setForeground(UITheme.COLOR_TEXT_MUTED);

        valueLabel.setFont(UITheme.FONT_TITLE);
        valueLabel.setForeground(accentColor);

        card.add(lblTitle, BorderLayout.NORTH);
        card.add(valueLabel, BorderLayout.CENTER);
        return card;
    }

    // TAB 2: USER ACCOUNT MANAGEMENT
    private JPanel createUserManagementTab() {
        JPanel panel = new JPanel(new BorderLayout(10, 10));
        panel.setBackground(UITheme.COLOR_BG);
        panel.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));

        // Filter Bar (LAYOUT MANAGER: FlowLayout - UNIT-IV)
        JPanel filterBar = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 6));
        filterBar.setBackground(UITheme.COLOR_CARD_BG);
        filterBar.setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));

        filterBar.add(new JLabel("Search Users:"));
        txtUserSearch = new JTextField(14);
        txtUserSearch.addActionListener(e -> loadUsersTable());
        filterBar.add(txtUserSearch);

        filterBar.add(new JLabel("Role Filter:"));
        cmbRoleFilter = new JComboBox<>(new String[] { "ALL", "ADMIN", "FARMER", "CUSTOMER" });
        cmbRoleFilter.addActionListener(e -> loadUsersTable());
        filterBar.add(cmbRoleFilter);

        JButton btnSearch = UITheme.createPrimaryButton("Search");
        btnSearch.addActionListener(e -> loadUsersTable());
        filterBar.add(btnSearch);

        JButton btnReset = UITheme.createSecondaryButton("Reset");
        btnReset.addActionListener(e -> {
            txtUserSearch.setText("");
            cmbRoleFilter.setSelectedIndex(0);
            loadUsersTable();
        });
        filterBar.add(btnReset);

        panel.add(filterBar, BorderLayout.NORTH);

        // User Accounts Table (SWING CONCEPT: JTable, DefaultTableModel - UNIT-V)
        String[] cols = { "User ID", "Full Name", "Username", "Role", "Status", "Contact / Location" };
        userTableModel = new DefaultTableModel(cols, 0) {
            @Override
            public boolean isCellEditable(int row, int col) {
                return false;
            }
        };
        userTable = new JTable(userTableModel);
        userTable.setFont(UITheme.FONT_REGULAR);
        userTable.setRowHeight(24);
        userTable.getTableHeader().setFont(UITheme.FONT_BOLD);
        userTable.getTableHeader().setBackground(UITheme.COLOR_PRIMARY_DARK);
        userTable.getTableHeader().setForeground(Color.WHITE);

        // POPUP MENU CONCEPT: Creating a popup menu (UNIT-V)
        setupUserTablePopupMenu();

        panel.add(new JScrollPane(userTable), BorderLayout.CENTER);

        // Action Buttons Bar
        JPanel btnBar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 8));
        btnBar.setBackground(UITheme.COLOR_BG);

        JButton btnToggleStatus = UITheme.createSecondaryButton("Toggle Active/Inactive");
        btnToggleStatus.addActionListener(e -> handleToggleUserStatus());
        btnBar.add(btnToggleStatus);

        JButton btnEditUser = UITheme.createPrimaryButton("Edit Selected User");
        btnEditUser.addActionListener(e -> handleEditUser());
        btnBar.add(btnEditUser);

        JButton btnExport = UITheme.createAccentButton("Export Directory (CSV)");
        btnExport.addActionListener(e -> exportUsersCsv());
        btnBar.add(btnExport);

        panel.add(btnBar, BorderLayout.SOUTH);
        return panel;
    }

    // POPUP MENU & ADAPTER CLASS CONCEPT: JPopupMenu, MouseAdapter (UNIT-IV &
    // UNIT-V)
    private void setupUserTablePopupMenu() {
        userPopupMenu = new JPopupMenu();
        JMenuItem miEdit = new JMenuItem("Edit User Details...");
        miEdit.addActionListener(e -> handleEditUser());

        JMenuItem miToggle = new JMenuItem("Toggle Active / Deactivate");
        miToggle.addActionListener(e -> handleToggleUserStatus());

        userPopupMenu.add(miEdit);
        userPopupMenu.add(new JSeparator());
        userPopupMenu.add(miToggle);

        // EVENT HANDLING: Adapter Class (MouseAdapter)
        userTable.addMouseListener(new MouseAdapter() {
            @Override
            public void mousePressed(MouseEvent e) {
                showPopup(e);
            }

            @Override
            public void mouseReleased(MouseEvent e) {
                showPopup(e);
            }

            private void showPopup(MouseEvent e) {
                if (e.isPopupTrigger()) {
                    int row = userTable.rowAtPoint(e.getPoint());
                    if (row >= 0 && row < userTable.getRowCount()) {
                        userTable.setRowSelectionInterval(row, row);
                        userPopupMenu.show(e.getComponent(), e.getX(), e.getY());
                    }
                }
            }
        });
    }

    // TAB 3: PRODUCE CATALOG MANAGEMENT
    private JPanel createCropManagementTab() {
        JPanel panel = new JPanel(new BorderLayout(10, 10));
        panel.setBackground(UITheme.COLOR_BG);
        panel.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));

        JPanel filterBar = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 6));
        filterBar.setBackground(UITheme.COLOR_CARD_BG);
        filterBar.setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));

        filterBar.add(new JLabel("Search Crops:"));
        txtCropSearch = new JTextField(16);
        txtCropSearch.addActionListener(e -> loadCropsTable());
        filterBar.add(txtCropSearch);

        JButton btnSearch = UITheme.createPrimaryButton("Search");
        btnSearch.addActionListener(e -> loadCropsTable());
        filterBar.add(btnSearch);

        JButton btnReset = UITheme.createSecondaryButton("Show All");
        btnReset.addActionListener(e -> {
            txtCropSearch.setText("");
            loadCropsTable();
        });
        filterBar.add(btnReset);

        panel.add(filterBar, BorderLayout.NORTH);

        String[] cols = { "Crop ID", "Farmer Name", "Produce Name", "Description", "Stock (Units)", "Price (₹)",
                "Status" };
        cropTableModel = new DefaultTableModel(cols, 0) {
            @Override
            public boolean isCellEditable(int r, int c) {
                return false;
            }
        };
        cropTable = new JTable(cropTableModel);
        cropTable.setFont(UITheme.FONT_REGULAR);
        cropTable.setRowHeight(24);
        cropTable.getTableHeader().setFont(UITheme.FONT_BOLD);
        cropTable.getTableHeader().setBackground(UITheme.COLOR_PRIMARY_DARK);
        cropTable.getTableHeader().setForeground(Color.WHITE);

        panel.add(new JScrollPane(cropTable), BorderLayout.CENTER);

        JPanel btnBar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 8));
        btnBar.setBackground(UITheme.COLOR_BG);

        JButton btnToggleAvail = UITheme.createSecondaryButton("Toggle Availability");
        btnToggleAvail.addActionListener(e -> handleToggleCropAvailability());
        btnBar.add(btnToggleAvail);

        JButton btnEditCrop = UITheme.createPrimaryButton("Edit Stock & Price");
        btnEditCrop.addActionListener(e -> handleEditCrop());
        btnBar.add(btnEditCrop);

        panel.add(btnBar, BorderLayout.SOUTH);
        return panel;
    }

    // TAB 4: ORDERS OVERSIGHT
    private JPanel createOrderManagementTab() {
        JPanel panel = new JPanel(new BorderLayout(10, 10));
        panel.setBackground(UITheme.COLOR_BG);
        panel.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));

        JPanel filterBar = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 6));
        filterBar.setBackground(UITheme.COLOR_CARD_BG);
        filterBar.setBorder(BorderFactory.createEmptyBorder(8, 8, 8, 8));

        filterBar.add(new JLabel("Status Filter:"));
        cmbOrderStatusFilter = new JComboBox<>(
                new String[] { "ALL", "PENDING", "CONFIRMED", "COMPLETED", "CANCELLED" });
        cmbOrderStatusFilter.addActionListener(e -> loadOrdersTable());
        filterBar.add(cmbOrderStatusFilter);

        JButton btnRefresh = UITheme.createPrimaryButton("Refresh Orders");
        btnRefresh.addActionListener(e -> loadOrdersTable());
        filterBar.add(btnRefresh);

        panel.add(filterBar, BorderLayout.NORTH);

        String[] cols = { "Order ID", "Customer Name", "Farmer Name", "Order Date", "Total (₹)", "Current Status" };
        orderTableModel = new DefaultTableModel(cols, 0) {
            @Override
            public boolean isCellEditable(int r, int c) {
                return false;
            }
        };
        orderTable = new JTable(orderTableModel);
        orderTable.setFont(UITheme.FONT_REGULAR);
        orderTable.setRowHeight(24);
        orderTable.getTableHeader().setFont(UITheme.FONT_BOLD);
        orderTable.getTableHeader().setBackground(UITheme.COLOR_PRIMARY_DARK);
        orderTable.getTableHeader().setForeground(Color.WHITE);

        panel.add(new JScrollPane(orderTable), BorderLayout.CENTER);

        JPanel btnBar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 8));
        btnBar.setBackground(UITheme.COLOR_BG);

        JButton btnViewItems = UITheme.createPrimaryButton("View Order Items");
        btnViewItems.addActionListener(e -> handleViewOrderItems());
        btnBar.add(btnViewItems);

        JButton btnUpdateStatus = UITheme.createSecondaryButton("Update Order Status");
        btnUpdateStatus.addActionListener(e -> handleUpdateOrderStatus());
        btnBar.add(btnUpdateStatus);

        JButton btnExport = UITheme.createAccentButton("Export Orders (CSV)");
        btnExport.addActionListener(e -> exportOrdersCsv());
        btnBar.add(btnExport);

        panel.add(btnBar, BorderLayout.SOUTH);
        return panel;
    }

    // TAB 5: PLATFORM HIERARCHY (SWING CONCEPT: Trees [JTree] - UNIT-V)
    private JPanel createTreeHierarchyTab() {
        JPanel panel = new JPanel(new BorderLayout(10, 10));
        panel.setBackground(UITheme.COLOR_BG);
        panel.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));

        JPanel header = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 6));
        header.setBackground(UITheme.COLOR_CARD_BG);
        JLabel lblTreeDesc = new JLabel("YieldGrid Role & Produce Catalog Organizational Hierarchy");
        lblTreeDesc.setFont(UITheme.FONT_BOLD);
        header.add(lblTreeDesc);

        JButton btnRefreshTree = UITheme.createPrimaryButton("Reload Hierarchy");
        btnRefreshTree.addActionListener(e -> loadHierarchyTree());
        header.add(btnRefreshTree);

        panel.add(header, BorderLayout.NORTH);

        // Default Mutable Tree Model
        DefaultMutableTreeNode root = new DefaultMutableTreeNode("YieldGrid Platform Root");
        treeModel = new DefaultTreeModel(root);
        hierarchyTree = new JTree(treeModel);
        hierarchyTree.setFont(UITheme.FONT_REGULAR);
        hierarchyTree.setRowHeight(22);

        panel.add(new JScrollPane(hierarchyTree), BorderLayout.CENTER);
        return panel;
    }

    // DATA LOADING METHODS
    private void loadOverviewMetrics() {
        try {
            Map<String, Object> metrics = adminService.getSystemMetrics();
            int totalUsers = (int) metrics.getOrDefault("totalUsers", 0);
            int farmers = (int) metrics.getOrDefault("activeFarmers", 0);
            int customers = (int) metrics.getOrDefault("activeCustomers", 0);
            int crops = (int) metrics.getOrDefault("totalCrops", 0);
            int orders = (int) metrics.getOrDefault("totalOrders", 0);
            double revenue = (double) metrics.getOrDefault("grossRevenue", 0.0);

            lblMetricUsers.setText(String.valueOf(totalUsers));
            lblMetricFarmers.setText(String.valueOf(farmers));
            lblMetricCustomers.setText(String.valueOf(customers));
            lblMetricCrops.setText(String.valueOf(crops));
            lblMetricOrders.setText(String.valueOf(orders));
            lblMetricRevenue.setText(String.format("₹%.2f", revenue));

        } catch (ValidationException | SQLException e) {
            System.err.println("Overview metrics load error: " + e.getMessage());
        }
    }

    private void loadUsersTable() {
        String query = txtUserSearch != null ? txtUserSearch.getText() : "";
        String role = cmbRoleFilter != null ? (String) cmbRoleFilter.getSelectedItem() : "ALL";

        try {
            ArrayList<User> users = adminService.searchUsers(query, role);
            userTableModel.setRowCount(0);
            for (User u : users) {
                userTableModel.addRow(new Object[] {
                        u.getUserId(),
                        u.getName(),
                        u.getUsername(),
                        u.getRole(),
                        u.isActive() ? "ACTIVE" : "INACTIVE",
                        u.getContactInfo()
                });
            }
        } catch (ValidationException | SQLException e) {
            JOptionPane.showMessageDialog(this, "Failed to load user accounts: " + e.getMessage(), "Database Error",
                    JOptionPane.ERROR_MESSAGE);
        }
    }

    private void loadCropsTable() {
        String search = txtCropSearch != null ? txtCropSearch.getText() : "";
        try {
            ArrayList<Crop> crops = adminService.getAllCrops(search);
            cropTableModel.setRowCount(0);
            for (Crop c : crops) {
                cropTableModel.addRow(new Object[] {
                        c.getCropId(),
                        c.getFarmerName(),
                        c.getCropName(),
                        c.getDescription(),
                        c.getQuantity(),
                        String.format("%.2f", c.getPrice()),
                        c.isAvailable() ? "AVAILABLE" : "OUT OF STOCK"
                });
            }
        } catch (ValidationException | SQLException e) {
            JOptionPane.showMessageDialog(this, "Failed to load crops: " + e.getMessage(), "Database Error",
                    JOptionPane.ERROR_MESSAGE);
        }
    }

    private void loadOrdersTable() {
        String status = cmbOrderStatusFilter != null ? (String) cmbOrderStatusFilter.getSelectedItem() : "ALL";
        try {
            ArrayList<Order> orders = adminService.getAllOrders(status);
            orderTableModel.setRowCount(0);
            for (Order o : orders) {
                orderTableModel.addRow(new Object[] {
                        o.getOrderId(),
                        o.getCustomerName(),
                        o.getFarmerName(),
                        o.getOrderDate(),
                        String.format("%.2f", o.getTotalAmount()),
                        o.getStatus().name()
                });
            }
        } catch (ValidationException | SQLException e) {
            JOptionPane.showMessageDialog(this, "Failed to load orders: " + e.getMessage(), "Database Error",
                    JOptionPane.ERROR_MESSAGE);
        }
    }

    // SWING CONCEPT: Populating JTree nodes dynamically
    private void loadHierarchyTree() {
        try {
            ArrayList<User> users = adminService.searchUsers("", "ALL");
            ArrayList<Crop> crops = adminService.getAllCrops("");

            DefaultMutableTreeNode root = new DefaultMutableTreeNode("YieldGrid Platform Root");

            DefaultMutableTreeNode adminNode = new DefaultMutableTreeNode("Administrators");
            DefaultMutableTreeNode farmerNode = new DefaultMutableTreeNode("Farmers (Producers)");
            DefaultMutableTreeNode customerNode = new DefaultMutableTreeNode("Customers (Retail Buyers)");
            DefaultMutableTreeNode cropNode = new DefaultMutableTreeNode("Active Produce Listings");

            for (User u : users) {
                String label = u.getName() + " (@" + u.getUsername() + ") [" + (u.isActive() ? "Active" : "Inactive")
                        + "]";
                DefaultMutableTreeNode userNode = new DefaultMutableTreeNode(label);
                if ("ADMIN".equalsIgnoreCase(u.getRole())) {
                    adminNode.add(userNode);
                } else if ("FARMER".equalsIgnoreCase(u.getRole())) {
                    farmerNode.add(userNode);
                } else {
                    customerNode.add(userNode);
                }
            }

            for (Crop c : crops) {
                String cropLabel = c.getCropName() + " (" + c.getQuantity() + " units @ ₹" + c.getPrice() + ") by "
                        + c.getFarmerName();
                cropNode.add(new DefaultMutableTreeNode(cropLabel));
            }

            root.add(adminNode);
            root.add(farmerNode);
            root.add(customerNode);
            root.add(cropNode);

            treeModel.setRoot(root);
            treeModel.reload();

            // Expand top-level nodes for visual presentation
            for (int i = 0; i < hierarchyTree.getRowCount(); i++) {
                hierarchyTree.expandRow(i);
            }

        } catch (ValidationException | SQLException e) {
            System.err.println("Tree hierarchy load error: " + e.getMessage());
        }
    }

    // ACTION HANDLERS
    private void handleToggleUserStatus() {
        int row = userTable.getSelectedRow();
        if (row < 0) {
            JOptionPane.showMessageDialog(this, "Please select a user from the table first.", "Selection Required",
                    JOptionPane.WARNING_MESSAGE);
            return;
        }

        int userId = (int) userTableModel.getValueAt(row, 0);
        String name = (String) userTableModel.getValueAt(row, 1);
        String status = (String) userTableModel.getValueAt(row, 4);
        boolean currentActive = "ACTIVE".equalsIgnoreCase(status);

        int confirm = JOptionPane.showConfirmDialog(this,
                "Are you sure you want to " + (currentActive ? "deactivate" : "activate") + " account for:\n" + name
                        + " (ID: " + userId + ")?",
                "Confirm Status Change",
                JOptionPane.YES_NO_OPTION);

        if (confirm == JOptionPane.YES_OPTION) {
            try {
                boolean success = adminService.toggleUserActiveStatus(userId);
                if (success) {
                    JOptionPane.showMessageDialog(this, "User status updated successfully.", "Success",
                            JOptionPane.INFORMATION_MESSAGE);
                    loadUsersTable();
                    loadOverviewMetrics();
                }
            } catch (ValidationException | SQLException e) {
                JOptionPane.showMessageDialog(this, e.getMessage(), "Operation Failed", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    private void handleEditUser() {
        int row = userTable.getSelectedRow();
        if (row < 0) {
            JOptionPane.showMessageDialog(this, "Please select a user to edit.", "Selection Required",
                    JOptionPane.WARNING_MESSAGE);
            return;
        }

        int userId = (int) userTableModel.getValueAt(row, 0);
        String name = (String) userTableModel.getValueAt(row, 1);
        String role = (String) userTableModel.getValueAt(row, 3);
        String status = (String) userTableModel.getValueAt(row, 4);
        String contact = (String) userTableModel.getValueAt(row, 5);

        JDialog dialog = new JDialog(this, "Edit User Account (ID: " + userId + ")", true);
        dialog.setSize(440, 320);
        dialog.setLocationRelativeTo(this);
        dialog.setLayout(new BorderLayout());

        JPanel form = new JPanel(new GridBagLayout());
        form.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));
        form.setBackground(UITheme.COLOR_CARD_BG);
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(6, 6, 6, 6);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        gbc.gridx = 0;
        gbc.gridy = 0;
        form.add(new JLabel("Full Name:"), gbc);
        gbc.gridx = 1;
        JTextField txtName = new JTextField(name, 16);
        form.add(txtName, gbc);

        gbc.gridx = 0;
        gbc.gridy = 1;
        form.add(new JLabel("Contact / Location:"), gbc);
        gbc.gridx = 1;
        JTextField txtContact = new JTextField(contact != null ? contact : "", 16);
        form.add(txtContact, gbc);

        gbc.gridx = 0;
        gbc.gridy = 2;
        form.add(new JLabel("Account Role:"), gbc);
        gbc.gridx = 1;
        JComboBox<String> cmbRole = new JComboBox<>(new String[] { "ADMIN", "FARMER", "CUSTOMER" });
        cmbRole.setSelectedItem(role);
        form.add(cmbRole, gbc);

        gbc.gridx = 0;
        gbc.gridy = 3;
        form.add(new JLabel("Active Status:"), gbc);
        gbc.gridx = 1;
        JCheckBox chkActive = new JCheckBox("Account is Active", "ACTIVE".equalsIgnoreCase(status));
        form.add(chkActive, gbc);

        JPanel btnBar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 10));
        btnBar.setBackground(UITheme.COLOR_CARD_BG);

        JButton btnCancel = UITheme.createSecondaryButton("Cancel");
        btnCancel.addActionListener(e -> dialog.dispose());
        btnBar.add(btnCancel);

        JButton btnSave = UITheme.createPrimaryButton("Save Changes");
        btnSave.addActionListener(e -> {
            try {
                boolean ok = adminService.updateUserDetails(
                        userId,
                        txtName.getText(),
                        txtContact.getText(),
                        (String) cmbRole.getSelectedItem(),
                        chkActive.isSelected());
                if (ok) {
                    JOptionPane.showMessageDialog(dialog, "Account details successfully saved to database.",
                            "Account Updated", JOptionPane.INFORMATION_MESSAGE);
                    dialog.dispose();
                    loadUsersTable();
                    loadOverviewMetrics();
                }
            } catch (ValidationException | SQLException ex) {
                JOptionPane.showMessageDialog(dialog, ex.getMessage(), "Update Error", JOptionPane.ERROR_MESSAGE);
            }
        });
        btnBar.add(btnSave);

        dialog.add(form, BorderLayout.CENTER);
        dialog.add(btnBar, BorderLayout.SOUTH);
        dialog.setVisible(true);
    }

    private void handleToggleCropAvailability() {
        int row = cropTable.getSelectedRow();
        if (row < 0) {
            JOptionPane.showMessageDialog(this, "Please select a crop to toggle availability.", "Selection Required",
                    JOptionPane.WARNING_MESSAGE);
            return;
        }

        int cropId = (int) cropTableModel.getValueAt(row, 0);
        String name = (String) cropTableModel.getValueAt(row, 2);
        String status = (String) cropTableModel.getValueAt(row, 6);
        boolean makeAvailable = !"AVAILABLE".equalsIgnoreCase(status);

        try {
            boolean success = adminService.toggleCropAvailability(cropId, makeAvailable);
            if (success) {
                JOptionPane.showMessageDialog(this, "Crop availability for '" + name + "' updated.", "Success",
                        JOptionPane.INFORMATION_MESSAGE);
                loadCropsTable();
            }
        } catch (ValidationException | SQLException e) {
            JOptionPane.showMessageDialog(this, e.getMessage(), "Operation Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void handleEditCrop() {
        int row = cropTable.getSelectedRow();
        if (row < 0) {
            JOptionPane.showMessageDialog(this, "Please select a crop to edit.", "Selection Required",
                    JOptionPane.WARNING_MESSAGE);
            return;
        }

        int cropId = (int) cropTableModel.getValueAt(row, 0);
        String farmerName = (String) cropTableModel.getValueAt(row, 1);
        String cropName = (String) cropTableModel.getValueAt(row, 2);
        String desc = (String) cropTableModel.getValueAt(row, 3);
        int quantity = (int) cropTableModel.getValueAt(row, 4);
        double price = Double.parseDouble((String) cropTableModel.getValueAt(row, 5));
        boolean avail = "AVAILABLE".equalsIgnoreCase((String) cropTableModel.getValueAt(row, 6));

        JDialog dialog = new JDialog(this, "Administrative Edit — " + cropName, true);
        dialog.setSize(420, 320);
        dialog.setLocationRelativeTo(this);
        dialog.setLayout(new BorderLayout());

        JPanel form = new JPanel(new GridBagLayout());
        form.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));
        form.setBackground(UITheme.COLOR_CARD_BG);
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(6, 6, 6, 6);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        gbc.gridx = 0;
        gbc.gridy = 0;
        form.add(new JLabel("Crop Name:"), gbc);
        gbc.gridx = 1;
        JTextField txtName = new JTextField(cropName, 15);
        form.add(txtName, gbc);

        gbc.gridx = 0;
        gbc.gridy = 1;
        form.add(new JLabel("Description:"), gbc);
        gbc.gridx = 1;
        JTextField txtDesc = new JTextField(desc, 15);
        form.add(txtDesc, gbc);

        gbc.gridx = 0;
        gbc.gridy = 2;
        form.add(new JLabel("Stock Quantity:"), gbc);
        gbc.gridx = 1;
        JSpinner spinQty = new JSpinner(new SpinnerNumberModel(quantity, 0, 100000, 1));
        form.add(spinQty, gbc);

        gbc.gridx = 0;
        gbc.gridy = 3;
        form.add(new JLabel("Unit Price (₹):"), gbc);
        gbc.gridx = 1;
        JTextField txtPrice = new JTextField(String.format("%.2f", price), 15);
        form.add(txtPrice, gbc);

        gbc.gridx = 0;
        gbc.gridy = 4;
        form.add(new JLabel("Listing Status:"), gbc);
        gbc.gridx = 1;
        JCheckBox chkAvail = new JCheckBox("Available for Purchase", avail);
        form.add(chkAvail, gbc);

        JPanel btnBar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 10));
        btnBar.setBackground(UITheme.COLOR_CARD_BG);

        JButton btnCancel = UITheme.createSecondaryButton("Cancel");
        btnCancel.addActionListener(e -> dialog.dispose());
        btnBar.add(btnCancel);

        JButton btnSave = UITheme.createPrimaryButton("Save Changes");
        btnSave.addActionListener(e -> {
            try {
                double parsedPrice = Double.parseDouble(txtPrice.getText().trim());
                int parsedQty = (Integer) spinQty.getValue();
                Crop updated = new Crop(cropId, 0, farmerName, txtName.getText().trim(), txtDesc.getText().trim(),
                        parsedQty, parsedPrice, chkAvail.isSelected());

                boolean ok = adminService.updateCrop(updated);
                if (ok) {
                    JOptionPane.showMessageDialog(dialog, "Crop details successfully saved.", "Success",
                            JOptionPane.INFORMATION_MESSAGE);
                    dialog.dispose();
                    loadCropsTable();
                    loadOverviewMetrics();
                }
            } catch (NumberFormatException nfe) {
                JOptionPane.showMessageDialog(dialog, "Please enter a valid numeric unit price.", "Validation Error",
                        JOptionPane.ERROR_MESSAGE);
            } catch (ValidationException | SQLException ex) {
                JOptionPane.showMessageDialog(dialog, ex.getMessage(), "Update Error", JOptionPane.ERROR_MESSAGE);
            }
        });
        btnBar.add(btnSave);

        dialog.add(form, BorderLayout.CENTER);
        dialog.add(btnBar, BorderLayout.SOUTH);
        dialog.setVisible(true);
    }

    private void handleViewOrderItems() {
        int row = orderTable.getSelectedRow();
        if (row < 0) {
            JOptionPane.showMessageDialog(this, "Please select an order to view its items.", "Selection Required",
                    JOptionPane.WARNING_MESSAGE);
            return;
        }

        int orderId = (int) orderTableModel.getValueAt(row, 0);
        String cust = (String) orderTableModel.getValueAt(row, 1);
        String farm = (String) orderTableModel.getValueAt(row, 2);
        String total = (String) orderTableModel.getValueAt(row, 4);

        try {
            ArrayList<Order> allOrders = adminService.getAllOrders("ALL");
            Order target = null;
            for (Order o : allOrders) {
                if (o.getOrderId() == orderId) {
                    target = o;
                    break;
                }
            }

            if (target == null) {
                JOptionPane.showMessageDialog(this, "Order not found.", "Error", JOptionPane.ERROR_MESSAGE);
                return;
            }

            JDialog dialog = new JDialog(this, "Order Items Breakdown (Order #" + orderId + ")", true);
            dialog.setSize(520, 340);
            dialog.setLocationRelativeTo(this);
            dialog.setLayout(new BorderLayout(10, 10));

            JPanel top = new JPanel(new GridLayout(2, 1, 4, 4));
            top.setBorder(BorderFactory.createEmptyBorder(10, 15, 10, 15));
            top.add(new JLabel("Customer: " + cust + " | Farmer: " + farm));
            top.add(new JLabel("Total Paid: ₹" + total + " | Order Status: " + target.getStatus().name()));
            dialog.add(top, BorderLayout.NORTH);

            String[] cols = { "Crop ID", "Crop Name", "Quantity", "Unit Price (₹)", "Subtotal (₹)" };
            DefaultTableModel itemsModel = new DefaultTableModel(cols, 0);
            if (target.getItems() != null) {
                for (OrderItem it : target.getItems()) {
                    itemsModel.addRow(new Object[] {
                            it.getCropId(),
                            it.getCropName(),
                            it.getQuantity(),
                            String.format("%.2f", it.getUnitPrice()),
                            String.format("%.2f", it.getSubtotal())
                    });
                }
            }
            JTable itemsTable = new JTable(itemsModel);
            itemsTable.setFont(UITheme.FONT_REGULAR);
            itemsTable.setRowHeight(22);
            dialog.add(new JScrollPane(itemsTable), BorderLayout.CENTER);

            JPanel bottom = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 10));
            JButton btnClose = UITheme.createPrimaryButton("Close");
            btnClose.addActionListener(e -> dialog.dispose());
            bottom.add(btnClose);
            dialog.add(bottom, BorderLayout.SOUTH);

            dialog.setVisible(true);

        } catch (ValidationException | SQLException e) {
            JOptionPane.showMessageDialog(this, e.getMessage(), "Error", JOptionPane.ERROR_MESSAGE);
        }
    }

    private void handleUpdateOrderStatus() {
        int row = orderTable.getSelectedRow();
        if (row < 0) {
            JOptionPane.showMessageDialog(this, "Please select an order to update status.", "Selection Required",
                    JOptionPane.WARNING_MESSAGE);
            return;
        }

        int orderId = (int) orderTableModel.getValueAt(row, 0);
        String currentStatusStr = (String) orderTableModel.getValueAt(row, 5);

        OrderStatus[] choices = OrderStatus.values();
        OrderStatus selected = (OrderStatus) JOptionPane.showInputDialog(this,
                "Select new status for Order #" + orderId + ":",
                "Update Order Status",
                JOptionPane.QUESTION_MESSAGE,
                null,
                choices,
                OrderStatus.fromString(currentStatusStr));

        if (selected != null) {
            try {
                boolean success = adminService.updateOrderStatus(orderId, selected);
                if (success) {
                    JOptionPane.showMessageDialog(this, "Order #" + orderId + " updated to " + selected.name(),
                            "Status Updated", JOptionPane.INFORMATION_MESSAGE);
                    loadOrdersTable();
                    loadOverviewMetrics();
                }
            } catch (ValidationException | SQLException e) {
                JOptionPane.showMessageDialog(this, e.getMessage(), "Status Update Failed", JOptionPane.ERROR_MESSAGE);
            }
        }
    }

    // CSV EXPORT METHODS (FILE I/O - UNIT-IV)
    private void exportUsersCsv() {
        try {
            ArrayList<User> users = adminService.searchUsers("", "ALL");
            JFileChooser chooser = new JFileChooser();
            chooser.setSelectedFile(new File("yieldgrid_users_directory.csv"));
            int result = chooser.showSaveDialog(this);
            if (result == JFileChooser.APPROVE_OPTION) {
                File target = chooser.getSelectedFile();
                DataExporter.exportUsersToCSV(users, target);
                JOptionPane.showMessageDialog(this,
                        "User accounts exported successfully to:\n" + target.getAbsolutePath(), "Export Complete",
                        JOptionPane.INFORMATION_MESSAGE);
            }
        } catch (ValidationException | SQLException | IOException e) {
            JOptionPane.showMessageDialog(this, "Export failed: " + e.getMessage(), "Export Error",
                    JOptionPane.ERROR_MESSAGE);
        }
    }

    private void exportOrdersCsv() {
        try {
            ArrayList<Order> orders = adminService.getAllOrders("ALL");
            JFileChooser chooser = new JFileChooser();
            chooser.setSelectedFile(new File("yieldgrid_orders_report.csv"));
            int result = chooser.showSaveDialog(this);
            if (result == JFileChooser.APPROVE_OPTION) {
                File target = chooser.getSelectedFile();
                DataExporter.exportOrdersToCSV(orders, target);
                JOptionPane.showMessageDialog(this,
                        "Orders report exported successfully to:\n" + target.getAbsolutePath(), "Export Complete",
                        JOptionPane.INFORMATION_MESSAGE);
            }
        } catch (ValidationException | SQLException | IOException e) {
            JOptionPane.showMessageDialog(this, "Export failed: " + e.getMessage(), "Export Error",
                    JOptionPane.ERROR_MESSAGE);
        }
    }

    // INTERFACE METHOD IMPLEMENTATIONS (AdminActions & DashboardActions)
    @Override
    public void refreshData() {
        int selected = tabbedPane.getSelectedIndex();
        if (selected == 0) {
            loadOverviewMetrics();
        } else if (selected == 1) {
            loadUsersTable();
        } else if (selected == 2) {
            loadCropsTable();
        } else if (selected == 3) {
            loadOrdersTable();
        } else if (selected == 4) {
            loadHierarchyTree();
        }
    }

    @Override
    public void showProfile() {
        tabbedPane.setSelectedComponent(profilePanel);
    }

    @Override
    public void logout() {
        int confirm = JOptionPane.showConfirmDialog(this,
                "Are you sure you want to log out of the Administration Console?",
                "Confirm Logout",
                JOptionPane.YES_NO_OPTION);

        if (confirm == JOptionPane.YES_OPTION) {
            SessionManager.logout();
            LoginFrame loginFrame = new LoginFrame();
            loginFrame.setVisible(true);
            dispose();
        }
    }

    @Override
    public void auditUserAccounts() {
        loadUsersTable();
    }

    @Override
    public void viewSystemMetrics() {
        loadOverviewMetrics();
    }

    @Override
    public void exportAuditReport() {
        exportUsersCsv();
    }
}
