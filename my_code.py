import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.*;
import java.util.ArrayList;
import java.util.List;

public class FriendsBookApp {
    private JFrame frame;
    private DefaultListModel<Friend> listModel;
    private JList<Friend> friendList;
    private List<Friend> friendsList;

    public FriendsBookApp() {
        friendsList = new ArrayList<>();
        listModel = new DefaultListModel<>();
        friendList = new JList<>(listModel);

        frame = new JFrame("Friends Book");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 400);
        frame.setLayout(new BorderLayout());

        JPanel inputPanel = new JPanel();
        inputPanel.setLayout(new GridLayout(3, 2));

        JLabel nameLabel = new JLabel("Name:");
        JTextField nameField = new JTextField();
        JLabel ageLabel = new JLabel("Age:");
        JTextField ageField = new JTextField();
        JLabel contactLabel = new JLabel("Contact:");
        JTextField contactField = new JTextField();

        inputPanel.add(nameLabel);
        inputPanel.add(nameField);
        inputPanel.add(ageLabel);
        inputPanel.add(ageField);
        inputPanel.add(contactLabel);
        inputPanel.add(contactField);

        JButton addButton = new JButton("Add Friend");
        addButton.addActionListener(e -> {
            String name = nameField.getText();
            String ageText = ageField.getText();
            String contact = contactField.getText();

            // Error handling for age input
            int age;
            try {
                age = Integer.parseInt(ageText);
                if (age <= 0) throw new NumberFormatException();
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(frame, "Invalid age. Please enter a positive number.");
                return;
            }

            Friend friend = new Friend(name, age, contact);
            friendsList.add(friend);
            listModel.addElement(friend);

            nameField.setText("");
            ageField.setText("");
            contactField.setText("");
        });

        JButton removeButton = new JButton("Remove Friend");
        removeButton.addActionListener(e -> {
            int selectedIndex = friendList.getSelectedIndex();
            if (selectedIndex != -1) {
                friendsList.remove(selectedIndex);
                listModel.remove(selectedIndex);
            }
        });

        JButton saveButton = new JButton("Save Friends");
        saveButton.addActionListener(e -> {
            String filename = chooseFile(true);
            if (filename != null) saveFriendsToFile(filename);
        });

        JButton loadButton = new JButton("Load Friends");
        loadButton.addActionListener(e -> {
            String filename = chooseFile(false);
            if (filename != null) loadFriendsFromFile(filename);
        });

        JPanel buttonPanel = new JPanel();
        buttonPanel.add(addButton);
        buttonPanel.add(removeButton);
        buttonPanel.add(saveButton);
        buttonPanel.add(loadButton);

        frame.add(inputPanel, BorderLayout.NORTH);
        frame.add(new JScrollPane(friendList), BorderLayout.CENTER);
        frame.add(buttonPanel, BorderLayout.SOUTH);

        frame.setVisible(true);
    }

    // Method to save friends to a file
    private void saveFriendsToFile(String filename) {
        try (PrintWriter writer = new PrintWriter(new FileWriter(filename))) {
            for (Friend friend : friendsList) {
                writer.println(friend.toFileString());
            }
            JOptionPane.showMessageDialog(frame, "Friends saved successfully!");
        } catch (IOException e) {
            JOptionPane.showMessageDialog(frame, "Error saving file: " + e.getMessage());
        }
    }

    // Method to load friends from a file
    private void loadFriendsFromFile(String filename) {
        friendsList.clear();
        listModel.clear();
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            while ((line = reader.readLine()) != null) {
                friendsList.add(Friend.fromFileString(line));
            }
            for (Friend f : friendsList) {
                listModel.addElement(f);
            }
            JOptionPane.showMessageDialog(frame, "Friends loaded successfully!");
        } catch (IOException e) {
            JOptionPane.showMessageDialog(frame, "Error loading file: " + e.getMessage());
        }
    }

    // Method to choose a file
    private String chooseFile(boolean saveMode) {
        JFileChooser fileChooser = new JFileChooser();
        int option;
        if (saveMode) {
            option = fileChooser.showSaveDialog(frame);
        } else {
            option = fileChooser.showOpenDialog(frame);
        }
        if (option == JFileChooser.APPROVE_OPTION) {
            return fileChooser.getSelectedFile().getAbsolutePath();
        }
        return null;
    }

    // Friend class inside the same file
    private static class Friend {
        private String name;
        private int age;
        private String contact;

        public Friend(String name, int age, String contact) {
            this.name = name;
            this.age = age;
            this.contact = contact;
        }

        public String toFileString() {
            return name + "," + age + "," + contact;
        }

        public static Friend fromFileString(String line) {
            String[] parts = line.split(",");
            return new Friend(parts[0], Integer.parseInt(parts[1]), parts[2]);
        }

        @Override
        public String toString() {
            return name + " (Age: " + age + ")";
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(FriendsBookApp::new);
    }
}
