package yieldgrid.util;

import java.util.LinkedList;
import java.util.Queue;

/**
 * UNIT-III Multithreading Demonstration (Academic Teaching Example):
 * Demonstrates thread creation (Runnable and Thread subclass), Thread Groups,
 * Daemon threads, Thread priorities, Synchronization, and Inter-thread communication (wait/notifyAll).
 */
public class MultithreadingDemo {

    // Monitor-synchronized bounded buffer for inter-thread communication
    static class BoundedBuffer {
        private final Queue<String> queue = new LinkedList<>();
        private final int capacity;

        BoundedBuffer(int capacity) {
            this.capacity = capacity;
        }

        public synchronized void put(String item) throws InterruptedException {
            while (queue.size() >= capacity) {
                wait();
            }
            queue.add(item);
            notifyAll();
        }

        public synchronized String take() throws InterruptedException {
            while (queue.isEmpty()) {
                wait();
            }
            String item = queue.poll();
            notifyAll();
            return item;
        }
    }

    // Thread creation via Runnable interface
    static class Producer implements Runnable {
        private final BoundedBuffer buffer;
        private final int total;

        Producer(BoundedBuffer buffer, int total) {
            this.buffer = buffer;
            this.total = total;
        }

        @Override
        public void run() {
            try {
                for (int i = 1; i <= total; i++) {
                    buffer.put("Item-" + i);
                    Thread.sleep(15);
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }

    // Thread creation via extending Thread class
    static class ConsumerThread extends Thread {
        private final BoundedBuffer buffer;
        private final int total;
        private int processed = 0;

        ConsumerThread(ThreadGroup group, String name, BoundedBuffer buffer, int total) {
            super(group, name);
            this.buffer = buffer;
            this.total = total;
        }

        @Override
        public void run() {
            try {
                while (processed < total) {
                    buffer.take();
                    processed++;
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        public int getProcessed() {
            return processed;
        }
    }

    /**
     * Executes the producer-consumer simulation and returns processed item count.
     */
    public static int runSimulation(int itemCount) {
        BoundedBuffer buffer = new BoundedBuffer(2);
        ThreadGroup group = new ThreadGroup("YieldGrid-Threads");

        Thread producer = new Thread(group, new Producer(buffer, itemCount), "Producer");
        ConsumerThread consumer = new ConsumerThread(group, "Consumer", buffer, itemCount);

        // Daemon thread and thread priority configuration
        consumer.setDaemon(true);
        consumer.setPriority(Thread.NORM_PRIORITY - 1);
        producer.setPriority(Thread.NORM_PRIORITY);

        consumer.start();
        producer.start();

        try {
            producer.join(2000);
            consumer.join(2000);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }

        return consumer.getProcessed();
    }

    public static void main(String[] args) {
        System.out.println("=== YieldGrid Multithreading Demo (UNIT-III) ===");
        int count = 3;
        System.out.println("Running bounded producer-consumer simulation with " + count + " items...");
        int result = runSimulation(count);
        System.out.println("Simulation complete. Items processed: " + result);
    }
}
