package yieldgrid.ui;

import java.awt.Color;
import java.awt.Cursor;
import java.awt.Dimension;
import java.awt.Font;
import javax.swing.BorderFactory;
import javax.swing.JButton;
import javax.swing.JLabel;
import javax.swing.JPanel;
import javax.swing.JTable;
import javax.swing.table.DefaultTableCellRenderer;

/*
 * COURSE CONCEPT:
 * Java Swing, AWT Color, Font, Component Styling & Reusability
 *
 * PURPOSE:
 * UITheme encapsulates the visual styling and aesthetic palette for YieldGrid.
 * Implements the required restrained agricultural visual identity:
 * - Cream / warm off-white background
 * - Muted dark green primary accents
 * - Dark earthy brown text
 * - Warm gold / amber accent highlights
 */

public class UITheme {

    // AWT COLOR PALETTE:
    public static final Color COLOR_PRIMARY = new Color(46, 125, 50);       // Forest Green
    public static final Color COLOR_PRIMARY_DARK = new Color(27, 94, 32);  // Deep Foliage Green
    public static final Color COLOR_ACCENT = new Color(188, 108, 37);      // Earthy Amber / Gold
    public static final Color COLOR_BG = new Color(250, 247, 238);         // Warm Cream Background
    public static final Color COLOR_CARD_BG = new Color(255, 255, 255);    // Clean Card White
    public static final Color COLOR_TEXT_DARK = new Color(50, 35, 25);     // Dark Earth Brown Text
    public static final Color COLOR_TEXT_MUTED = new Color(110, 100, 90);  // Subtle Gray-Brown
    public static final Color COLOR_BORDER = new Color(225, 220, 210);     // Light Tan Border
    public static final Color COLOR_SUCCESS = new Color(46, 125, 50);
    public static final Color COLOR_DANGER = new Color(198, 40, 40);

    // FONTS:
    public static final Font FONT_TITLE = new Font("Segoe UI", Font.BOLD, 20);
    public static final Font FONT_SUBTITLE = new Font("Segoe UI", Font.BOLD, 15);
    public static final Font FONT_BOLD = new Font("Segoe UI", Font.BOLD, 13);
    public static final Font FONT_REGULAR = new Font("Segoe UI", Font.PLAIN, 13);
    public static final Font FONT_SMALL = new Font("Segoe UI", Font.PLAIN, 11);

    // BUTTON UI DELEGATES FOR LOOK-AND-FEEL INDEPENDENCE:
    public static final StyledButtonUI PRIMARY_BUTTON_UI = new StyledButtonUI(
            COLOR_PRIMARY, new Color(56, 142, 60), new Color(27, 94, 32), new Color(235, 235, 235),
            Color.WHITE, new Color(130, 130, 130), new Color(36, 105, 40), new Color(210, 205, 195));

    public static final StyledButtonUI SECONDARY_BUTTON_UI = new StyledButtonUI(
            new Color(255, 255, 255), new Color(245, 242, 235), new Color(235, 230, 220), new Color(245, 245, 245),
            COLOR_TEXT_DARK, new Color(150, 150, 150), new Color(185, 175, 160), new Color(220, 220, 220));

    public static final StyledButtonUI ACCENT_BUTTON_UI = new StyledButtonUI(
            COLOR_ACCENT, new Color(205, 120, 45), new Color(155, 85, 25), new Color(235, 235, 235),
            Color.WHITE, new Color(130, 130, 130), new Color(165, 95, 30), new Color(210, 205, 195));

    public static final StyledButtonUI DANGER_BUTTON_UI = new StyledButtonUI(
            COLOR_DANGER, new Color(216, 48, 48), new Color(160, 25, 25), new Color(240, 230, 230),
            Color.WHITE, new Color(150, 120, 120), new Color(175, 30, 30), new Color(220, 205, 205));

    // HELPER: Style primary action button (Dark Green with White text)
    public static JButton createPrimaryButton(String text) {
        JButton button = new JButton(text);
        stylePrimaryButton(button);
        return button;
    }

    public static void stylePrimaryButton(JButton button) {
        button.setFont(FONT_BOLD);
        button.setUI(PRIMARY_BUTTON_UI);
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));
        button.setBorder(BorderFactory.createEmptyBorder(7, 14, 7, 14));
    }

    // HELPER: Style secondary action button (White / Light with Dark text and visible border)
    public static JButton createSecondaryButton(String text) {
        JButton button = new JButton(text);
        styleSecondaryButton(button);
        return button;
    }

    public static void styleSecondaryButton(JButton button) {
        button.setFont(FONT_BOLD);
        button.setUI(SECONDARY_BUTTON_UI);
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));
        button.setBorder(BorderFactory.createEmptyBorder(7, 14, 7, 14));
    }

    // HELPER: Style accent button (Warm Amber with White text)
    public static JButton createAccentButton(String text) {
        JButton button = new JButton(text);
        styleAccentButton(button);
        return button;
    }

    public static void styleAccentButton(JButton button) {
        button.setFont(FONT_BOLD);
        button.setUI(ACCENT_BUTTON_UI);
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));
        button.setBorder(BorderFactory.createEmptyBorder(7, 14, 7, 14));
    }

    // HELPER: Style danger / destructive action button (Crimson Red with White text)
    public static JButton createDangerButton(String text) {
        JButton button = new JButton(text);
        styleDangerButton(button);
        return button;
    }

    public static void styleDangerButton(JButton button) {
        button.setFont(FONT_BOLD);
        button.setUI(DANGER_BUTTON_UI);
        button.setCursor(new Cursor(Cursor.HAND_CURSOR));
        button.setBorder(BorderFactory.createEmptyBorder(7, 14, 7, 14));
    }

    // CUSTOM BUTTON UI:
    // Ensures background and foreground colors are rendered correctly across all Look and Feels
    // including WindowsLookAndFeel, with distinct hover, pressed, and disabled states.
    public static class StyledButtonUI extends javax.swing.plaf.basic.BasicButtonUI {
        private final Color normalBg;
        private final Color hoverBg;
        private final Color pressedBg;
        private final Color disabledBg;
        private final Color normalFg;
        private final Color disabledFg;
        private final Color borderColor;
        private final Color disabledBorderColor;

        public StyledButtonUI(Color normalBg, Color hoverBg, Color pressedBg, Color disabledBg,
                              Color normalFg, Color disabledFg, Color borderColor, Color disabledBorderColor) {
            this.normalBg = normalBg;
            this.hoverBg = hoverBg;
            this.pressedBg = pressedBg;
            this.disabledBg = disabledBg;
            this.normalFg = normalFg;
            this.disabledFg = disabledFg;
            this.borderColor = borderColor;
            this.disabledBorderColor = disabledBorderColor;
        }

        @Override
        public void installUI(javax.swing.JComponent c) {
            super.installUI(c);
            javax.swing.AbstractButton b = (javax.swing.AbstractButton) c;
            b.setOpaque(false);
            b.setContentAreaFilled(false);
            b.setFocusPainted(false);
            b.setRolloverEnabled(true);
        }

        @Override
        public void paint(java.awt.Graphics g, javax.swing.JComponent c) {
            javax.swing.AbstractButton b = (javax.swing.AbstractButton) c;
            javax.swing.ButtonModel model = b.getModel();
            java.awt.Graphics2D g2 = (java.awt.Graphics2D) g.create();
            g2.setRenderingHint(java.awt.RenderingHints.KEY_ANTIALIASING, java.awt.RenderingHints.VALUE_ANTIALIAS_ON);

            int width = b.getWidth();
            int height = b.getHeight();

            Color bg;
            Color border;
            if (!model.isEnabled()) {
                bg = disabledBg;
                border = disabledBorderColor;
            } else if (model.isPressed()) {
                bg = pressedBg;
                border = borderColor;
            } else if (model.isRollover()) {
                bg = hoverBg;
                border = borderColor;
            } else {
                bg = normalBg;
                border = borderColor;
            }

            g2.setColor(bg);
            g2.fillRoundRect(0, 0, width, height, 6, 6);

            if (border != null) {
                g2.setColor(border);
                g2.drawRoundRect(0, 0, width - 1, height - 1, 6, 6);
            }

            if (model.isEnabled() && b.hasFocus()) {
                g2.setColor(new Color(255, 255, 255, 140));
                g2.drawRoundRect(1, 1, width - 3, height - 3, 4, 4);
            }

            g2.dispose();
            super.paint(g, c);
        }

        @Override
        protected void paintText(java.awt.Graphics g, javax.swing.AbstractButton b, java.awt.Rectangle textRect, String text) {
            java.awt.Graphics2D g2 = (java.awt.Graphics2D) g.create();
            g2.setRenderingHint(java.awt.RenderingHints.KEY_TEXT_ANTIALIASING, java.awt.RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
            java.awt.FontMetrics fm = g2.getFontMetrics(b.getFont());

            Color textColor = b.getModel().isEnabled() ? normalFg : disabledFg;
            g2.setColor(textColor);
            g2.setFont(b.getFont());

            int textX = textRect.x;
            int textY = textRect.y + fm.getAscent();
            g2.drawString(text, textX, textY);
            g2.dispose();
        }

        @Override
        protected void paintText(java.awt.Graphics g, javax.swing.JComponent c, java.awt.Rectangle textRect, String text) {
            paintText(g, (javax.swing.AbstractButton) c, textRect, text);
        }
    }

    // HELPER: Create standard padded card panel
    public static JPanel createCardPanel() {
        JPanel card = new JPanel();
        card.setBackground(COLOR_CARD_BG);
        card.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(COLOR_BORDER, 1),
            BorderFactory.createEmptyBorder(12, 16, 12, 16)
        ));
        return card;
    }

    // HELPER: Style JTable header and row appearance
    public static void formatTable(JTable table) {
        table.setFont(FONT_REGULAR);
        table.setRowHeight(28);
        table.setGridColor(COLOR_BORDER);
        table.setSelectionBackground(new Color(220, 237, 200));
        table.setSelectionForeground(COLOR_TEXT_DARK);
        table.getTableHeader().setFont(FONT_BOLD);
        table.getTableHeader().setBackground(new Color(238, 234, 222));
        table.getTableHeader().setForeground(COLOR_TEXT_DARK);
        table.getTableHeader().setPreferredSize(new Dimension(100, 32));

        DefaultTableCellRenderer centerRenderer = new DefaultTableCellRenderer();
        centerRenderer.setHorizontalAlignment(JLabel.CENTER);
    }
}
