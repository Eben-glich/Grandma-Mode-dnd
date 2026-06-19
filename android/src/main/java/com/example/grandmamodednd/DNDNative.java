package com.example.grandmamodednd;

public class DNDNative {
    static {
        System.loadLibrary("grandma_dnd_native");
    }
    
    // Initialize the DND manager
    public static native void initDNDManager();
    
    // Set DND with preset duration (30min increments up to 2.5 hours)
    public static native boolean setDNDPreset(int minutes);
    
    // Set DND with custom duration (max 7 hours)
    public static native boolean setDNDCustom(int minutes);
    
    // Get available preset options
    public static native int[] getPresetOptions();
    
    // Check if DND is currently active
    public static native boolean isDNDActive();
    
    // Get remaining DND time in minutes
    public static native int getRemainingTime();
    
    // Disable DND
    public static native void disableDND();
    
    // Cleanup resources
    public static native void cleanup();
}
