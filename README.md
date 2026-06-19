# Grandma-Mode-dnd

Android Do Not Disturb (DND) Application built with C++ native code.

## Features

- **Preset DND Durations**: Quick select options in 30-minute increments (30min, 60min, 90min, 120min, 150min)
- **Custom DND Duration**: Set custom DND time up to 7 hours (420 minutes)
- **Real-time Status**: Shows remaining DND time on the main screen
- **Easy-to-use Interface**: Simple button click to access DND options
- **Disable Option**: Quickly turn off DND mode

## Architecture

The app is built with:
- **C++ Native Code**: Core DND manager logic using JNI (Java Native Interface)
- **Java Frontend**: Android UI and activity management
- **CMake Build System**: Cross-platform C++ compilation

## Project Structure

```
android/
├── src/main/cpp/
│   ├── include/
│   │   └── dnd_manager.h          # DND Manager header
│   ├── dnd_manager.cpp             # DND Manager implementation
│   └── native_interface.cpp        # JNI native interface
├── src/main/java/
│   └── com/example/grandmamodednd/
│       ├── DNDNative.java          # JNI wrapper
│       └── MainActivity.java       # Main UI activity
├── src/main/res/
│   └── layout/
│       └── activity_main.xml       # Main layout
├── AndroidManifest.xml             # App manifest
├── build.gradle                    # Build configuration
└── CMakeLists.txt                  # CMake configuration
```

## Building

### Prerequisites
- Android Studio 4.0 or higher
- NDK (Native Development Kit) installed
- CMake 3.10 or higher
- Target Android API Level 21 or higher

### Build Steps

1. Open the project in Android Studio
2. Ensure NDK is installed via SDK Manager
3. Build the project:
   ```
   ./gradlew build
   ```
4. To run on device:
   ```
   ./gradlew installDebug
   ```

## Permissions Required

- `android.permission.ACCESS_NOTIFICATION_POLICY` - Required to access DND settings
- `android.permission.MODIFY_AUDIO_SETTINGS` - For audio control

## Usage

1. **Enable DND**: Tap the "Enable DND" button
2. **Select Duration**: Choose from:
   - Preset: 30min, 60min, 90min, 120min, 150min
   - Custom: Enter 1-420 minutes (up to 7 hours)
3. **View Status**: Current DND status and remaining time displayed at top
4. **Disable DND**: Tap the button again and select "Disable"

## API Reference

### DNDNative Class

- `initDNDManager()` - Initialize the DND manager
- `setDNDPreset(int minutes)` - Set DND with preset duration
- `setDNDCustom(int minutes)` - Set DND with custom duration (max 7 hours)
- `getPresetOptions()` - Get array of preset options
- `isDNDActive()` - Check if DND is currently active
- `getRemainingTime()` - Get remaining DND time in minutes
- `disableDND()` - Disable DND mode
- `cleanup()` - Clean up resources

## Version

- **Version**: 1.0
- **API Level**: 21+
- **Target API**: 33
