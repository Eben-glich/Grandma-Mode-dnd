package com.example.grandmamodednd;

import android.app.NotificationManager;
import android.content.Context;
import android.os.Build;
import android.os.Bundle;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AlertDialog;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    private TextView statusTextView;
    private Button dndButton;
    private ListView presetListView;
    private EditText customDurationEditText;
    private NotificationManager notificationManager;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        
        // Initialize UI components
        statusTextView = findViewById(R.id.status_text);
        dndButton = findViewById(R.id.dnd_button);
        presetListView = findViewById(R.id.preset_list);
        customDurationEditText = findViewById(R.id.custom_duration);
        
        notificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        
        // Initialize native DND manager
        DNDNative.initDNDManager();
        
        // Set up DND button click listener
        dndButton.setOnClickListener(v -> showDNDOptions());
        
        // Update status periodically
        updateStatus();
    }
    
    private void showDNDOptions() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Do Not Disturb Settings")
               .setMessage("Select a duration or set a custom time")
               .setPositiveButton("Presets", (dialog, id) -> showPresetOptions())
               .setNegativeButton("Custom", (dialog, id) -> showCustomDurationDialog())
               .setNeutralButton("Disable", (dialog, id) -> disableDND())
               .show();
    }
    
    private void showPresetOptions() {
        int[] presets = DNDNative.getPresetOptions();
        String[] presetLabels = new String[presets.length];
        
        for (int i = 0; i < presets.length; i++) {
            presetLabels[i] = formatMinutes(presets[i]);
        }
        
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Select DND Duration")
               .setItems(presetLabels, (dialog, which) -> {
                   boolean success = DNDNative.setDNDPreset(presets[which]);
                   if (success) {
                       Toast.makeText(MainActivity.this, 
                           "DND set for " + presetLabels[which], 
                           Toast.LENGTH_SHORT).show();
                       enableDoNotDisturb();
                       updateStatus();
                   } else {
                       Toast.makeText(MainActivity.this, 
                           "Failed to set DND", 
                           Toast.LENGTH_SHORT).show();
                   }
               })
               .show();
    }
    
    private void showCustomDurationDialog() {
        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Custom DND Duration (max 7 hours)")
               .setMessage("Enter duration in minutes (1-420):")
               .setView(customDurationEditText)
               .setPositiveButton("Apply", (dialog, id) -> {
                   String input = customDurationEditText.getText().toString();
                   try {
                       int minutes = Integer.parseInt(input);
                       boolean success = DNDNative.setDNDCustom(minutes);
                       if (success) {
                           Toast.makeText(MainActivity.this, 
                               "DND set for " + formatMinutes(minutes), 
                               Toast.LENGTH_SHORT).show();
                           enableDoNotDisturb();
                           customDurationEditText.setText("");
                           updateStatus();
                       } else {
                           Toast.makeText(MainActivity.this, 
                               "Invalid duration. Max is 7 hours (420 minutes).", 
                               Toast.LENGTH_SHORT).show();
                       }
                   } catch (NumberFormatException e) {
                       Toast.makeText(MainActivity.this, 
                           "Please enter a valid number", 
                           Toast.LENGTH_SHORT).show();
                   }
               })
               .setNegativeButton("Cancel", null)
               .show();
    }
    
    private void enableDoNotDisturb() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (notificationManager.isNotificationPolicyAccessGranted()) {
                notificationManager.setInterruptionFilter(
                    NotificationManager.INTERRUPTION_FILTER_NONE);
            }
        }
    }
    
    private void disableDND() {
        DNDNative.disableDND();
        
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (notificationManager.isNotificationPolicyAccessGranted()) {
                notificationManager.setInterruptionFilter(
                    NotificationManager.INTERRUPTION_FILTER_ALL);
            }
        }
        
        Toast.makeText(this, "DND disabled", Toast.LENGTH_SHORT).show();
        updateStatus();
    }
    
    private void updateStatus() {
        if (DNDNative.isDNDActive()) {
            int remainingMinutes = DNDNative.getRemainingTime();
            statusTextView.setText("DND Active - " + formatMinutes(remainingMinutes) + " remaining");
        } else {
            statusTextView.setText("DND Inactive");
        }
    }
    
    private String formatMinutes(int minutes) {
        if (minutes < 60) {
            return minutes + " min";
        } else {
            int hours = minutes / 60;
            int mins = minutes % 60;
            if (mins == 0) {
                return hours + " hr";
            } else {
                return hours + " hr " + mins + " min";
            }
        }
    }
    
    @Override
    protected void onDestroy() {
        super.onDestroy();
        DNDNative.cleanup();
    }
}
