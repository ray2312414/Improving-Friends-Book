public class Friend {
    private String name;
    private int age;
    private String contact;

    // Constructor
    public Friend(String name, int age, String contact) {
        this.name = name;
        this.age = age;
        this.contact = contact;
    }

    // Getters
    public String getName() { return name; }
    public int getAge() { return age; }
    public String getContact() { return contact; }

    // Converts Friend object to a string for saving to a file
    public String toFileString() {
        return name + "," + age + "," + contact;
    }

    // Creates a Friend object from a string (for loading)
    public static Friend fromFileString(String line) {
        String[] parts = line.split(",");
        return new Friend(parts[0], Integer.parseInt(parts[1]), parts[2]);
    }

    @Override
    public String toString() {
        return name + " (Age: " + age + ")";
    }
}
