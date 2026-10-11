package yieldgrid.util;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.security.SecureRandom;
import java.security.spec.InvalidKeySpecException;
import java.util.Base64;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;

/**
 * Security Utility:
 * Salted PBKDF2 password hashing with HMAC-SHA256, constant-time comparison,
 * and transparent migration for legacy accounts.
 */
public class PasswordUtil {

    private static final String PBKDF2_PREFIX = "pbkdf2$";
    private static final String LEGACY_SHA256_PREFIX = "sha256$";
    private static final String ALGORITHM = "PBKDF2WithHmacSHA256";
    private static final int ITERATIONS = 10000;
    private static final int SALT_BYTES = 16;
    private static final int KEY_LENGTH_BITS = 256;
    private static final SecureRandom SECURE_RANDOM = new SecureRandom();

    private PasswordUtil() {
    }

    /**
     * Hashes plaintext password using salted PBKDF2.
     */
    public static String hashPassword(String plaintext) {
        if (plaintext == null || plaintext.isEmpty()) {
            throw new IllegalArgumentException("Password cannot be null or empty.");
        }
        byte[] salt = new byte[SALT_BYTES];
        SECURE_RANDOM.nextBytes(salt);
        byte[] hash = derivePbkdf2Key(plaintext.toCharArray(), salt, ITERATIONS, KEY_LENGTH_BITS);
        return PBKDF2_PREFIX + ITERATIONS + "$" + Base64.getEncoder().encodeToString(salt) + "$" + Base64.getEncoder().encodeToString(hash);
    }

    /**
     * Verifies candidate password against stored hash with legacy fallback.
     */
    public static boolean verifyPassword(String plaintext, String stored) {
        if (plaintext == null || stored == null) {
            return false;
        }

        if (stored.startsWith(PBKDF2_PREFIX)) {
            String[] parts = stored.split("\\$");
            if (parts.length != 4) {
                return false;
            }
            try {
                int iterations = Integer.parseInt(parts[1]);
                byte[] salt = Base64.getDecoder().decode(parts[2]);
                byte[] expectedHash = Base64.getDecoder().decode(parts[3]);
                byte[] candidateHash = derivePbkdf2Key(plaintext.toCharArray(), salt, iterations, expectedHash.length * 8);
                return MessageDigest.isEqual(expectedHash, candidateHash);
            } catch (Exception e) {
                return false;
            }
        } else if (stored.startsWith(LEGACY_SHA256_PREFIX)) {
            String legacyHash = computeLegacySha256(plaintext);
            return MessageDigest.isEqual(stored.getBytes(StandardCharsets.UTF_8), legacyHash.getBytes(StandardCharsets.UTF_8));
        } else {
            return MessageDigest.isEqual(stored.getBytes(StandardCharsets.UTF_8), plaintext.getBytes(StandardCharsets.UTF_8));
        }
    }

    /**
     * Checks if password string is already formatted as a hash.
     */
    public static boolean isHashed(String password) {
        return password != null && (password.startsWith(PBKDF2_PREFIX) || password.startsWith(LEGACY_SHA256_PREFIX));
    }

    /**
     * Indicates whether an account needs upgrade to salted PBKDF2.
     */
    public static boolean needsMigration(String stored) {
        return stored == null || !stored.startsWith(PBKDF2_PREFIX);
    }

    private static byte[] derivePbkdf2Key(char[] password, byte[] salt, int iterations, int keyLengthBits) {
        try {
            PBEKeySpec spec = new PBEKeySpec(password, salt, iterations, keyLengthBits);
            return SecretKeyFactory.getInstance(ALGORITHM).generateSecret(spec).getEncoded();
        } catch (NoSuchAlgorithmException | InvalidKeySpecException e) {
            throw new RuntimeException("PBKDF2 derivation failed", e);
        }
    }

    private static String computeLegacySha256(String plaintext) {
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-256");
            byte[] hashBytes = md.digest(plaintext.getBytes(StandardCharsets.UTF_8));
            StringBuilder sb = new StringBuilder();
            for (byte b : hashBytes) {
                sb.append(String.format("%02x", b));
            }
            return LEGACY_SHA256_PREFIX + sb.toString();
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("SHA-256 not available", e);
        }
    }
}
