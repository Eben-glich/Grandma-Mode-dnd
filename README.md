# Grandma Mode - DND (Do Not Disturb) Manager

A comprehensive system that allows up to 7 authorized remote devices to temporarily disable Do Not Disturb mode on the main device for emergency situations. Perfect for family members who need to reach Grandma in case of emergencies.

## Features

✨ **Main Application (Grandma's Phone/Computer)**
- First-time setup GUI to register up to 7 remote devices
- Auto-generates 8-digit numeric access codes for each device
- Real-time GPS/Network location tracking for all devices
- View device locations within meters accuracy
- Activity logging with timestamps and locations
- DND status monitoring
- Automatic 10-minute deactivation timer after each request

✨ **Remote Device Application (Family Members)**
- Clean, intuitive interface with light blue icon and white "G" logo
- Secure 8-digit code authentication
- One-touch emergency DND deactivation
- Automatic location tracking and transmission
- Server connection configuration
- Help guide and settings panel
- Activity history

## System Requirements

### Main Application (main_app.py)
- Python 3.6+
- tkinter (usually pre-installed with Python)
- sqlite3 (built-in)
- socket library (built-in)
- threading (built-in)
- pathlib (built-in)

### Remote Device App (remote_device_app.py)
- Python 3.6+
- tkinter (usually pre-installed with Python)
- Pillow (PIL) - for icon generation
- requests or geocoder - for location services (optional but recommended)

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Eben-glich/Grandma-Mode-dnd.git
cd Grandma-Mode-dnd
```

### Step 2: Install Dependencies

#### For Main App (minimal requirements):
```bash
# Most requirements are built-in. Only tkinter might need installation on Linux:
sudo apt-get install python3-tk  # Ubuntu/Debian
sudo pacman -S tk                 # Arch Linux
brew install python-tk            # macOS (if using Homebrew)
```

#### For Remote App (full features):
```bash
pip install Pillow geocoder requests
```

#### Optional - For Enhanced Location Services:
```bash
pip install geolite2 geocoder
```

## Quick Start Guide

### First Time Setup - Main Application

1. **Run the main app:**
   ```bash
   python3 main_app.py
   ```

2. **On first launch**, you'll see the setup screen:
   - Enter names for up to 7 devices (e.g., "Mom's iPhone", "Dad's Android", "Sister's Phone")
   - Click "Save Devices"
   - **IMPORTANT**: Save the generated 8-digit access codes somewhere secure

3. **Access Codes Display:**
   - Each device gets a unique 8-digit numeric code (e.g., `12345678`)
   - Codes are displayed after setup completes
   - You can view them anytime in Settings → View Access Codes

4. **Main Interface Features:**
   - **DND Status**: Shows current Do Not Disturb state
   - **Registered Devices & Locations**: Lists all devices with their GPS locations
   - **View Activity Log**: See history of all DND deactivation requests
   - **View Device Locations**: Detailed map coordinates and accuracy
   - **Settings**: Reset devices or clear logs

### First Time Setup - Remote Device App

1. **Run the remote app:**
   ```bash
   python3 remote_device_app.py
   ```

2. **On first launch**, you'll see login screen:
   - **Server IP**: Enter the IP address of Grandma's computer
     - Local network: Use the computer's local IP (e.g., `192.168.1.100`)
     - Remote connection: Use Grandma's public IP (requires port forwarding)
   - **Server Port**: Default is `5555` (must match main app)
   - **Access Code**: Enter the 8-digit code provided by Grandma

3. **Login**:
   - Click "Login" or press Enter
   - You'll see the main control interface

4. **Emergency Deactivation**:
   - Press the large red "DISABLE DND FOR 10 MINUTES" button
   - Confirm the action
   - The system will:
     - Send your location to Grandma's phone
     - Disable DND for 10 minutes
     - Log the request with timestamp and location

## Configuration

### Network Setup

#### Local Network (Same WiFi):
```
Main App PC IP: 192.168.1.100
Remote Device App: Server IP = 192.168.1.100, Port = 5555
```

#### Remote Network (Different Networks):
1. **Port Forwarding** (on main app's router):
   - Forward external port 5555 → internal port 5555 on main PC
   - Note the public IP address

2. **Remote Device App Configuration**:
   - Server IP = Grandma's public IP address (from whatismyipaddress.com)
   - Port = 5555

### Server Port Configuration

To change the default port from 5555:

**Main App (main_app.py)** - Line 314:
```python
server_socket.bind(('0.0.0.0', 5555))  # Change 5555 to your port
```

**Remote App (remote_device_app.py)** - Line 24:
```python
self.server_port = 5555  # Change to match main app
```

## File Structure

```
Grandma-Mode-dnd/
├── main_app.py              # Main application (Grandma's phone/computer)
├── remote_device_app.py     # Remote device app (Family members)
├── README.md                # This file
└── .grandma_mode_dnd/       # Created on first run (hidden folder)
    ├── grandma_mode.db      # SQLite database with all data
    ├── config.json          # App configuration
    └── first_launch_complete # First launch marker
```

## Database Structure

The app stores data in SQLite with these tables:

### devices
- `id`: Unique device identifier
- `name`: Device name
- `access_code`: 8-digit code
- `latitude`, `longitude`: Last known location
- `location_accuracy_meters`: GPS/network accuracy
- `last_location_update`: Timestamp of last location update

### dnd_status
- `is_active`: Current DND state (1=active, 0=inactive)
- `deactivated_until`: When DND will reactivate
- `deactivated_by`: Which device disabled it
- `last_modified`: Last change timestamp

### activity_log
- `timestamp`: When action occurred
- `device_name`: Which device made the request
- `action`: What action was performed
- `latitude`, `longitude`: Location at time of request
- `location_accuracy_meters`: Accuracy of location

## Security Considerations

⚠️ **Important Security Notes:**

1. **Access Codes**: Each code is unique and 8-digit numeric
   - Only share with trusted family members
   - Treat like passwords
   - Change them by resetting devices if compromised

2. **Network Security**:
   - Only use on trusted networks
   - Avoid using on public WiFi
   - For remote access, use VPN when possible

3. **Location Privacy**:
   - Locations are recorded and stored locally
   - Only visible on Grandma's main device
   - Each request logs device location

4. **Server Security**:
   - Server runs on port 5555 by default
   - Only accessible from configured devices
   - Verify access codes before processing requests

## Troubleshooting

### Connection Issues

**"Could not reach Grandma's phone"**
- Verify server IP address is correct
- Check both devices are on same network (for local setup)
- Ensure main app is running
- Test connection with: `ping <server-ip>`

**Port Already in Use**
- Change port in both files to an unused port (e.g., 5556, 5557)
- Check what's using the port: `netstat -tulpn | grep 5555`

### Access Code Issues

**"Invalid access code"**
- Verify you entered exactly 8 digits
- All digits must be numbers (0-9)
- Check the code hasn't been changed

**Lost Access Codes**
- In Settings → View Access Codes (main app)
- Or reset all devices and regenerate in Settings

### Location Issues

**"Location not yet detected"**
- Location detection uses network/GPS
- May take 10-30 seconds on first use
- Ensure location services are enabled on remote device
- Check geocoder package is installed: `pip install geocoder`

### Performance Issues

**Slow Response Time**
- Check network connection speed
- Reduce distance between devices if using local network
- Try restarting both applications

## Usage Examples

### Example 1: Emergency Situation - Local Network

```
Grandma sets up main_app.py on home computer (192.168.1.100)
Daughter runs remote_device_app.py on her phone at work

Daughter enters:
- Server IP: 192.168.1.100
- Port: 5555
- Code: 45782931

She presses "DISABLE DND FOR 10 MINUTES"
Grandma's phone DND is disabled for 10 minutes
Grandma can receive calls/messages
Activity log shows: "Daughter - Disabled DND for 10 minutes" with location
```

### Example 2: Setup with Multiple Family Members

```
1. Grandma creates 7 devices:
   - Mom's iPhone (Code: 12345678)
   - Dad's Android (Code: 23456789)
   - Sister's Phone (Code: 34567890)
   - Brother's Phone (Code: 45678901)
   - Cousin's Phone (Code: 56789012)
   - Aunt's Phone (Code: 67890123)
   - Uncle's Phone (Code: 78901234)

2. Each family member installs remote_device_app.py
   Enters their unique access code
   Can now help in emergencies
```

## Advanced Features

### Viewing Activity History

1. Open main app
2. Click "View Activity Log"
3. See last 50 requests with:
   - Timestamp
   - Device name
   - Action performed
   - Device location (if available)
   - Location accuracy

### Viewing Device Locations

1. Open main app
2. Click "View Device Locations"
3. See all registered devices with:
   - Current coordinates (latitude/longitude)
   - Location accuracy in meters
   - Last update timestamp

## Future Enhancements

Possible improvements for future versions:
- Web-based interface
- Cloud-based backup
- SMS notifications
- Real-time notifications on main device
- Device health status
- Geofencing triggers
- Emergency call integration
- Multi-language support
- Dark mode UI

## Troubleshooting Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "ModuleNotFoundError: No module named 'PIL'" | Pillow not installed | `pip install Pillow` |
| "Connection refused" | Main app not running | Start main_app.py |
| "Invalid access code" | Wrong 8-digit code | Verify code in Settings |
| "Could not reach server" | Wrong IP/Port | Check network settings |
| Port 5555 in use | Another app using port | Use different port |

## Support & Contact

For issues, questions, or contributions:
- GitHub: [Eben-glich/Grandma-Mode-dnd](https://github.com/Eben-glich/Grandma-Mode-dnd)
- Email: eprogrammerglich@gmail.com

## License

This project is open source and available under the MIT License.

## Changelog

### Version 1.0 (Initial Release)
- ✅ Main DND manager application
- ✅ Remote device control app
- ✅ 8-digit numeric access codes
- ✅ GPS/Network location tracking
- ✅ Activity logging with locations
- ✅ SQLite database
- ✅ Multi-device support (up to 7)
- ✅ Light blue icon with white G
- ✅ 10-minute DND deactivation timer

## Disclaimer

This application is designed for emergency family communication. Users should:
- Respect privacy of all parties
- Use location data responsibly
- Only share access codes with trusted family members
- Not use for unauthorized access
- Follow all local laws regarding GPS tracking

---

**Developed with ❤️ by Eben-glich**

Stay safe and keep your family connected! 📱👨‍👩‍👧‍👦
