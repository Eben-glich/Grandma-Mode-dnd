#include <jni.h>
#include "dnd_manager.h"
#include <android/log.h>

#define LOG_TAG "GrandmaModeDND"
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO, LOG_TAG, __VA_ARGS__)
#define LOGE(...) __android_log_print(ANDROID_LOG_ERROR, LOG_TAG, __VA_ARGS__)

static DNDManager* g_dndManager = nullptr;

// Initialize the DND manager
extern "C" JNIEXPORT void JNICALL
Java_com_example_grandmamodednd_DNDNative_initDNDManager(JNIEnv* env, jobject obj) {
    if (g_dndManager == nullptr) {
        g_dndManager = new DNDManager();
        LOGI("DND Manager initialized");
    }
}

// Set DND with preset duration
extern "C" JNIEXPORT jboolean JNICALL
Java_com_example_grandmamodednd_DNDNative_setDNDPreset(JNIEnv* env, jobject obj, jint minutes) {
    if (g_dndManager == nullptr) {
        LOGE("DND Manager not initialized");
        return false;
    }
    
    bool result = g_dndManager->setDNDWithPreset(minutes);
    if (result) {
        LOGI("DND preset set for %d minutes", minutes);
    }
    return result;
}

// Set DND with custom duration
extern "C" JNIEXPORT jboolean JNICALL
Java_com_example_grandmamodednd_DNDNative_setDNDCustom(JNIEnv* env, jobject obj, jint minutes) {
    if (g_dndManager == nullptr) {
        LOGE("DND Manager not initialized");
        return false;
    }
    
    bool result = g_dndManager->setDNDCustom(minutes);
    if (result) {
        LOGI("DND custom set for %d minutes", minutes);
    }
    return result;
}

// Get preset options as array
extern "C" JNIEXPORT jintArray JNICALL
Java_com_example_grandmamodednd_DNDNative_getPresetOptions(JNIEnv* env, jobject obj) {
    if (g_dndManager == nullptr) {
        LOGE("DND Manager not initialized");
        return nullptr;
    }
    
    auto presets = g_dndManager->getPresetOptions();
    jintArray result = env->NewIntArray(presets.size());
    env->SetIntArrayRegion(result, 0, presets.size(), (jint*)presets.data());
    return result;
}

// Check if DND is active
extern "C" JNIEXPORT jboolean JNICALL
Java_com_example_grandmamodednd_DNDNative_isDNDActive(JNIEnv* env, jobject obj) {
    if (g_dndManager == nullptr) {
        return false;
    }
    return g_dndManager->isDNDActive();
}

// Get remaining DND time
extern "C" JNIEXPORT jint JNICALL
Java_com_example_grandmamodednd_DNDNative_getRemainingTime(JNIEnv* env, jobject obj) {
    if (g_dndManager == nullptr) {
        return 0;
    }
    return g_dndManager->getRemainingTime();
}

// Disable DND
extern "C" JNIEXPORT void JNICALL
Java_com_example_grandmamodednd_DNDNative_disableDND(JNIEnv* env, jobject obj) {
    if (g_dndManager != nullptr) {
        g_dndManager->disableDND();
        LOGI("DND disabled");
    }
}

// Cleanup
extern "C" JNIEXPORT void JNICALL
Java_com_example_grandmamodednd_DNDNative_cleanup(JNIEnv* env, jobject obj) {
    if (g_dndManager != nullptr) {
        delete g_dndManager;
        g_dndManager = nullptr;
        LOGI("DND Manager cleaned up");
    }
}
