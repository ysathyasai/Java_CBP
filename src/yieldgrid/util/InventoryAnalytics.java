package yieldgrid.util;

import java.util.List;
import yieldgrid.model.Crop;

/**
 * UNIT-I Academic Demonstration:
 * Demonstrates Recursion and Method Overloading in Java.
 */
public class InventoryAnalytics {

    private InventoryAnalytics() {
    }

    /**
     * Recursively calculates total inventory units across a crop list.
     * Base case: list is null or index is out of bounds -> returns 0.
     * Recursive step: current quantity + recursive call for remaining elements.
     */
    public static int calculateRecursiveStockUnits(List<Crop> crops, int index) {
        if (crops == null || index < 0 || index >= crops.size()) {
            return 0;
        }
        Crop crop = crops.get(index);
        int quantity = (crop != null) ? crop.getQuantity() : 0;
        return quantity + calculateRecursiveStockUnits(crops, index + 1);
    }

    /**
     * Overloaded entry method starting recursive calculation from index 0.
     */
    public static int calculateRecursiveStockUnits(List<Crop> crops) {
        return calculateRecursiveStockUnits(crops, 0);
    }
}
