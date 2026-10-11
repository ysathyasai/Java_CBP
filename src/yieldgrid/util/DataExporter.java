package yieldgrid.util;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.List;
import yieldgrid.model.Order;
import yieldgrid.model.OrderItem;
import yieldgrid.model.User;

/**
 * java.io Demonstration & Utility:
 * Exports user and order datasets to CSV using PrintWriter, BufferedWriter, and FileWriter,
 * and reads file records using BufferedReader and FileReader.
 */
public class DataExporter {

    private DataExporter() {
    }

    /**
     * Escapes CSV fields to prevent delimiter corruption and spreadsheet formula injection.
     */
    public static String escapeCsvField(String input) {
        if (input == null) {
            return "";
        }
        String field = input;
        if (!field.isEmpty()) {
            char first = field.charAt(0);
            if (first == '=' || first == '+' || first == '-' || first == '@' || first == '\t' || first == '\r') {
                field = "'" + field;
            }
        }
        field = field.replace("\r\n", " ").replace("\r", " ").replace("\n", " ");
        return field.replace("\"", "\"\"");
    }

    /**
     * Exports user accounts to a CSV file.
     */
    public static File exportUsersToCSV(List<User> users, File targetFile) throws IOException {
        if (targetFile == null) {
            targetFile = new File("yieldgrid_users_export.csv");
        }
        ensureParentDirectory(targetFile);

        try (PrintWriter writer = new PrintWriter(new BufferedWriter(new FileWriter(targetFile)))) {
            writer.println("User ID,Full Name,Username,Role,Account Status,Contact Information");
            if (users != null) {
                for (User u : users) {
                    if (u != null) {
                        writer.printf("%d,\"%s\",\"%s\",\"%s\",\"%s\",\"%s\"%n",
                                u.getUserId(),
                                escapeCsvField(u.getName()),
                                escapeCsvField(u.getUsername()),
                                escapeCsvField(u.getRole() != null ? u.getRole() : ""),
                                u.isActive() ? "ACTIVE" : "INACTIVE",
                                escapeCsvField(u.getContactInfo() != null ? u.getContactInfo() : ""));
                    }
                }
            }
        }
        return targetFile;
    }

    /**
     * Exports orders and item summaries to a CSV file.
     */
    public static File exportOrdersToCSV(List<Order> orders, File targetFile) throws IOException {
        if (targetFile == null) {
            targetFile = new File("yieldgrid_orders_export.csv");
        }
        ensureParentDirectory(targetFile);

        try (PrintWriter writer = new PrintWriter(new BufferedWriter(new FileWriter(targetFile)))) {
            writer.println("Order ID,Customer ID,Customer Name,Farmer ID,Farmer Name,Order Date,Total Amount (INR),Status,Items Summary");
            if (orders != null) {
                for (Order o : orders) {
                    if (o != null) {
                        StringBuilder items = new StringBuilder();
                        if (o.getItems() != null) {
                            for (OrderItem item : o.getItems()) {
                                if (item != null) {
                                    if (items.length() > 0) items.append("; ");
                                    items.append(item.getCropName()).append(" x").append(item.getQuantity());
                                }
                            }
                        }
                        writer.printf("%d,%d,\"%s\",%d,\"%s\",\"%s\",%.2f,\"%s\",\"%s\"%n",
                                o.getOrderId(),
                                o.getCustomerId(),
                                escapeCsvField(o.getCustomerName()),
                                o.getFarmerId(),
                                escapeCsvField(o.getFarmerName()),
                                o.getOrderDate() != null ? o.getOrderDate().toString() : "N/A",
                                o.getTotalAmount(),
                                o.getStatus() != null ? o.getStatus().name() : "UNKNOWN",
                                escapeCsvField(items.toString()));
                    }
                }
            }
        }
        return targetFile;
    }

    /**
     * Reads a CSV file using BufferedReader and counts the total lines.
     */
    public static int countCsvLines(File csvFile) throws IOException {
        if (csvFile == null || !csvFile.exists()) {
            return 0;
        }
        int count = 0;
        try (BufferedReader reader = new BufferedReader(new FileReader(csvFile))) {
            while (reader.readLine() != null) {
                count++;
            }
        }
        return count;
    }

    private static void ensureParentDirectory(File file) {
        if (file != null && file.getParentFile() != null && !file.getParentFile().exists()) {
            file.getParentFile().mkdirs();
        }
    }
}
