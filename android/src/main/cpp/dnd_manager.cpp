#include "dnd_manager.h"
#include <ctime>
#include <algorithm>

DNDManager::DNDManager()
    : dndStartTime(0), dndDurationMinutes(0), isActive(false),
      muteNotifications(false), muteVibration(false) {}

DNDManager::~DNDManager() {}

bool DNDManager::setDNDWithPreset(int durationMinutes) {
    // Validate preset duration (30min increments up to 2.5 hours)
    if (durationMinutes <= 0 || durationMinutes % 30 != 0 || 
        durationMinutes > MAX_PRESET_DURATION) {
        return false;
    }
    
    dndStartTime = time(nullptr);
    dndDurationMinutes = durationMinutes;
    isActive = true;
    muteNotifications = true;
    muteVibration = true;
    
    return true;
}

bool DNDManager::setDNDCustom(int durationMinutes) {
    // Validate custom duration (max 7 hours)
    if (durationMinutes <= 0 || durationMinutes > MAX_CUSTOM_DURATION) {
        return false;
    }
    
    dndStartTime = time(nullptr);
    dndDurationMinutes = durationMinutes;
    isActive = true;
    muteNotifications = true;
    muteVibration = true;
    
    return true;
}

std::vector<int> DNDManager::getPresetOptions() const {
    // Return available preset options: 30, 60, 90, 120, 150 minutes
    return {30, 60, 90, 120, 150};
}

bool DNDManager::isDNDActive() const {
    if (!isActive) {
        return false;
    }
    
    time_t currentTime = time(nullptr);
    long elapsedSeconds = difftime(currentTime, dndStartTime);
    long durationSeconds = dndDurationMinutes * 60;
    
    return elapsedSeconds < durationSeconds;
}

int DNDManager::getRemainingTime() const {
    if (!isActive) {
        return 0;
    }
    
    time_t currentTime = time(nullptr);
    long elapsedSeconds = difftime(currentTime, dndStartTime);
    long durationSeconds = dndDurationMinutes * 60;
    long remainingSeconds = durationSeconds - elapsedSeconds;
    
    if (remainingSeconds <= 0) {
        return 0;
    }
    
    return (remainingSeconds + 59) / 60; // Round up to nearest minute
}

void DNDManager::disableDND() {
    isActive = false;
    dndStartTime = 0;
    dndDurationMinutes = 0;
    muteNotifications = false;
    muteVibration = false;
}

void DNDManager::setMuteNotifications(bool mute) {
    muteNotifications = mute;
}

void DNDManager::setMuteVibration(bool mute) {
    muteVibration = mute;
}
