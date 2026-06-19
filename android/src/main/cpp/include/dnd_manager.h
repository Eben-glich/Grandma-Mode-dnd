#ifndef DND_MANAGER_H
#define DND_MANAGER_H

#include <string>
#include <ctime>
#include <vector>

class DNDManager {
public:
    DNDManager();
    ~DNDManager();
    
    // Set DND with predefined 30-minute increments (up to 2.5 hours)
    bool setDNDWithPreset(int durationMinutes);
    
    // Set custom DND duration (max 7 hours / 420 minutes)
    bool setDNDCustom(int durationMinutes);
    
    // Get available preset options (30min, 60min, 90min, 120min, 150min)
    std::vector<int> getPresetOptions() const;
    
    // Get current DND status
    bool isDNDActive() const;
    
    // Get remaining DND time in minutes
    int getRemainingTime() const;
    
    // Disable DND
    void disableDND();
    
    // Enable/Disable sound
    void setMuteNotifications(bool mute);
    
    // Enable/Disable vibration
    void setMuteVibration(bool mute);
    
private:
    time_t dndStartTime;
    int dndDurationMinutes;
    bool isActive;
    bool muteNotifications;
    bool muteVibration;
    
    const int MAX_CUSTOM_DURATION = 420; // 7 hours in minutes
    const int MAX_PRESET_DURATION = 150; // 2.5 hours in minutes
};

#endif // DND_MANAGER_H
