package yieldgrid.ui;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.FlowLayout;
import java.awt.Frame;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JDialog;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JPasswordField;
import javax.swing.JTextField;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;
import yieldgrid.exception.AuthenticationException;
import yieldgrid.exception.ValidationException;
import yieldgrid.model.User;
import yieldgrid.service.AuthenticationService;

/*
 * COURSE CONCEPT:
 * Java Swing (JDialog, JTextField, JPasswordField, JOptionPane), Event Handling (ActionListener),
 * Encapsulation, Polymorphism, Layout Managers (GridBagLayout, BorderLayout, FlowLayout),
 * Persistence (Database Profile Updates)
 *
 * PURPOSE:
 * ProfilePanel displays authenticated user profile information and allows users
 * (Farmers, Customers, Administrators) to edit their details and update passwords.
 * All changes persist directly into the MySQL database across application restarts.
 */

public class ProfilePanel extends JPanel {

    // OOP CONCEPT: Polymorphism
    // Accepts any User (Farmer, Customer, or AdminUser) through base class
    // reference
    private final User user;
    private final AuthenticationService authService;
    private Runnable onProfileUpdatedCallback;

    private JLabel valName;
    private JLabel valContact;
    private JLabel valStatus;

    public ProfilePanel(User user) {
        this(user, null);
    }

    public ProfilePanel(User user, Runnable onProfileUpdatedCallback) {
        this.user = user;
        this.authService = new AuthenticationService();
        this.onProfileUpdatedCallback = onProfileUpdatedCallback;
        initializeUI();
    }

    public void setOnProfileUpdatedCallback(Runnable callback) {
        this.onProfileUpdatedCallback = callback;
    }

    private void initializeUI() {
        setLayout(new BorderLayout());
        setBackground(UITheme.COLOR_BG);
        setBorder(BorderFactory.createEmptyBorder(20, 20, 20, 20));

        JPanel card = UITheme.createCardPanel();
        card.setLayout(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(10, 14, 10, 14);
        gbc.anchor = GridBagConstraints.WEST;
        gbc.fill = GridBagConstraints.HORIZONTAL;

        JLabel lblTitle = new JLabel("User Account Profile", SwingConstants.CENTER);
        lblTitle.setFont(UITheme.FONT_TITLE);
        lblTitle.setForeground(UITheme.COLOR_PRIMARY_DARK);
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.gridwidth = 2;
        card.add(lblTitle, gbc);

        gbc.gridwidth = 1;

        // User ID
        addProfileRow(card, gbc, 1, "Account ID:", String.valueOf(user.getUserId()), null);

        // Name
        valName = new JLabel(user.getName());
        addProfileRow(card, gbc, 2, "Full Name / Organization:", null, valName);

        // Username
        addProfileRow(card, gbc, 3, "Username:", user.getUsername(), null);

        // Role
        addProfileRow(card, gbc, 4, "System Role:", user.getRole(), null);

        // Role Description (Polymorphic call)
        addProfileRow(card, gbc, 5, "Role Details:", user.getRoleDescription(), null);

        // Contact
        valContact = new JLabel(
                user.getContactInfo() != null && !user.getContactInfo().isEmpty() ? user.getContactInfo()
                        : "Not Specified");
        addProfileRow(card, gbc, 6, "Contact / Location:", null, valContact);

        // Status
        valStatus = new JLabel(user.isActive() ? "Active Account" : "Deactivated");
        valStatus.setForeground(user.isActive() ? new Color(46, 125, 50) : UITheme.COLOR_DANGER);
        addProfileRow(card, gbc, 7, "Account Status:", null, valStatus);

        // Action Buttons Row: Edit Profile and Change Password
        gbc.gridy = 8;
        gbc.gridx = 0;
        gbc.gridwidth = 2;
        JPanel btnPanel = new JPanel(new FlowLayout(FlowLayout.CENTER, 15, 10));
        btnPanel.setOpaque(false);

        JButton btnEdit = UITheme.createPrimaryButton("Edit Profile Details");
        btnEdit.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                showEditProfileDialog();
            }
        });
        btnPanel.add(btnEdit);

        JButton btnPassword = UITheme.createSecondaryButton("Change Password");
        btnPassword.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                showChangePasswordDialog();
            }
        });
        btnPanel.add(btnPassword);

        card.add(btnPanel, gbc);

        JPanel centerWrapper = new JPanel(new GridBagLayout());
        centerWrapper.setBackground(UITheme.COLOR_BG);
        centerWrapper.add(card);
        add(centerWrapper, BorderLayout.CENTER);
    }

    private void addProfileRow(JPanel panel, GridBagConstraints gbc, int row, String label, String textValue,
            JLabel existingLabel) {
        gbc.gridy = row;
        gbc.gridx = 0;
        JLabel lbl = new JLabel(label);
        lbl.setFont(UITheme.FONT_BOLD);
        lbl.setForeground(UITheme.COLOR_TEXT_DARK);
        panel.add(lbl, gbc);

        gbc.gridx = 1;
        JLabel val = existingLabel;
        if (val == null) {
            val = new JLabel(textValue != null && !textValue.isEmpty() ? textValue : "Not Specified");
        }
        val.setFont(UITheme.FONT_REGULAR);
        if (existingLabel == null) {
            val.setForeground(UITheme.COLOR_TEXT_MUTED);
        }
        panel.add(val, gbc);
    }

    // MODAL DIALOG: Edit Profile details (Name, Contact Info)
    private void showEditProfileDialog() {
        Frame parentFrame = (Frame) SwingUtilities.getWindowAncestor(this);
        JDialog dialog = new JDialog(parentFrame, "Edit Profile Details", true);
        dialog.setSize(420, 260);
        dialog.setLocationRelativeTo(this);
        dialog.setLayout(new BorderLayout());

        JPanel form = new JPanel(new GridBagLayout());
        form.setBorder(BorderFactory.createEmptyBorder(15, 15, 15, 15));
        form.setBackground(UITheme.COLOR_CARD_BG);
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(8, 8, 8, 8);
        gbc.fill = GridBagConstraints.HORIZONTAL;

        gbc.gridx = 0;
        gbc.gridy = 0;
        JLabel lblName = new JLabel("Full Name:");
        lblName.setFont(UITheme.FONT_BOLD);
        form.add(lblName, gbc);

        gbc.gridx = 1;
        JTextField txtName = new JTextField(user.getName(), 18);
        txtName.setFont(UITheme.FONT_REGULAR);
        form.add(txtName, gbc);

        gbc.gridx = 0;
        gbc.gridy = 1;
        JLabel lblContact = new JLabel("Contact / Location:");
        lblContact.setFont(UITheme.FONT_BOLD);
        form.add(lblContact, gbc);

        gbc.gridx = 1;
        JTextField txtContact = new JTextField(user.getContactInfo() != null ? user.getContactInfo() : "", 18);
        txtContact.setFont(UITheme.FONT_REGULAR);
        form.add(txtContact, gbc);

        JPanel btnBar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 10));
        btnBar.setBackground(UITheme.COLOR_CARD_BG);

        JButton btnCancel = UITheme.createSecondaryButton("Cancel");
        btnCancel.addActionListener(e -> dialog.dispose());
        btnBar.add(btnCancel);

        JButton btnSave = UITheme.createPrimaryButton("Save Changes");
        btnSave.addActionListener(e -> {
            String newName = txtName.getText();
            String newContact = txtContact.getText();

            try {
                // Service persists changes directly to MySQL
                authService.updateProfile(user, newName, newContact);

                // Update UI state
                valName.setText(user.getName());
                valContact.setText(user.getContactInfo());

                JOptionPane.showMessageDialog(dialog,
                        "Profile updated successfully! Changes have been saved to the database.",
                        "Profile Saved",
                        JOptionPane.INFORMATION_MESSAGE);

                if (onProfileUpdatedCallback != null) {
                    onProfileUpdatedCallback.run();
                }

                dialog.dispose();

            } catch (ValidationException | AuthenticationException ex) {
                JOptionPane.showMessageDialog(dialog, ex.getMessage(), "Update Error", JOptionPane.ERROR_MESSAGE);
            }
        });
        btnBar.add(btnSave);

        dialog.add(form, BorderLayout.CENTER);
        dialog.add(btnBar, BorderLayout.SOUTH);
        dialog.setVisible(true);
    }

    // MODAL DIALOG: Change Password flow with current password verification
    private void showChangePasswordDialog() {
        Frame parentFrame = (Frame) SwingUtilities.getWindowAncestor(this);
        JDialog dialog = new JDialog(parentFrame, "Change Account Password", true);
        dialog.setSize(440, 290);
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
        form.add(new JLabel("Current Password:"), gbc);
        gbc.gridx = 1;
        JPasswordField txtCurrent = new JPasswordField(15);
        form.add(txtCurrent, gbc);

        gbc.gridx = 0;
        gbc.gridy = 1;
        form.add(new JLabel("New Password:"), gbc);
        gbc.gridx = 1;
        JPasswordField txtNew = new JPasswordField(15);
        form.add(txtNew, gbc);

        gbc.gridx = 0;
        gbc.gridy = 2;
        form.add(new JLabel("Confirm New Password:"), gbc);
        gbc.gridx = 1;
        JPasswordField txtConfirm = new JPasswordField(15);
        form.add(txtConfirm, gbc);

        JPanel btnBar = new JPanel(new FlowLayout(FlowLayout.RIGHT, 10, 10));
        btnBar.setBackground(UITheme.COLOR_CARD_BG);

        JButton btnCancel = UITheme.createSecondaryButton("Cancel");
        btnCancel.addActionListener(e -> dialog.dispose());
        btnBar.add(btnCancel);

        JButton btnSubmit = UITheme.createPrimaryButton("Update Password");
        btnSubmit.addActionListener(e -> {
            String current = new String(txtCurrent.getPassword());
            String newPass = new String(txtNew.getPassword());
            String confirmPass = new String(txtConfirm.getPassword());

            try {
                authService.changePassword(user.getUserId(), current, newPass, confirmPass);
                JOptionPane.showMessageDialog(dialog,
                        "Password changed successfully! Please use your new password for future logins.",
                        "Password Updated",
                        JOptionPane.INFORMATION_MESSAGE);
                dialog.dispose();

            } catch (ValidationException | AuthenticationException ex) {
                JOptionPane.showMessageDialog(dialog, ex.getMessage(), "Password Error", JOptionPane.ERROR_MESSAGE);
            }
        });
        btnBar.add(btnSubmit);

        dialog.add(form, BorderLayout.CENTER);
        dialog.add(btnBar, BorderLayout.SOUTH);
        dialog.setVisible(true);
    }
}
