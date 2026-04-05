import os
import shutil
import urllib.request

# Create directory structure
dirs = [
    'twa/app/src/main/res/mipmap-mdpi',
    'twa/app/src/main/res/mipmap-hdpi',
    'twa/app/src/main/res/mipmap-xhdpi',
    'twa/app/src/main/res/mipmap-xxhdpi',
    'twa/app/src/main/res/mipmap-xxxhdpi',
    'twa/app/src/main/res/values',
    'twa/gradle/wrapper',
]
for d in dirs:
    os.makedirs(d, exist_ok=True)

# Download icon
icon_url = 'https://incomesplitter.github.io/income-splitter2/icon-512.png'
try:
    urllib.request.urlretrieve(icon_url, '/tmp/icon.png')
    for d in ['mipmap-mdpi','mipmap-hdpi','mipmap-xhdpi','mipmap-xxhdpi','mipmap-xxxhdpi']:
        shutil.copy('/tmp/icon.png', f'twa/app/src/main/res/{d}/ic_launcher.png')
    print("Icon downloaded successfully")
except Exception as e:
    print(f"Icon download failed: {e}")

# Copy keystore
shutil.copy('app.keystore', 'twa/app.keystore')

# Root build.gradle - Gradle 9 compatible
with open('twa/build.gradle', 'w') as f:
    f.write("""plugins {
    id 'com.android.application' version '8.5.2' apply false
}
""")

# settings.gradle - Gradle 9 compatible
with open('twa/settings.gradle', 'w') as f:
    f.write("""pluginManagement {
    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}
dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        google()
        mavenCentral()
    }
}
rootProject.name = 'IncomeSplitter'
include ':app'
""")

# App build.gradle
with open('twa/app/build.gradle', 'w') as f:
    f.write("""plugins {
    id 'com.android.application'
}
android {
    namespace 'com.incomesplitter.app'
    compileSdkVersion 34
    defaultConfig {
        applicationId 'com.incomesplitter.app'
        minSdkVersion 21
        targetSdkVersion 34
        versionCode 1
        versionName '1.0'
    }
    signingConfigs {
        release {
            storeFile file('app.keystore')
            storePassword 'android123'
            keyAlias 'incomesplitter'
            keyPassword 'android123'
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled false
        }
    }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_17
        targetCompatibility JavaVersion.VERSION_17
    }
}
dependencies {
    implementation 'com.google.androidbrowserhelper:androidbrowserhelper:2.5.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
}
""")

# gradle.properties
with open('twa/gradle.properties', 'w') as f:
    f.write("""android.useAndroidX=true
android.enableJetifier=true
org.gradle.jvmargs=-Xmx2048m
""")

# gradle-wrapper.properties
with open('twa/gradle/wrapper/gradle-wrapper.properties', 'w') as f:
    f.write("""distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\\://services.gradle.org/distributions/gradle-8.9-bin.zip
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
""")

# gradlew script
with open('twa/gradlew', 'w') as f:
    f.write("""#!/bin/sh
APP_HOME="$(cd "$(dirname "$0")" && pwd)"
exec "$APP_HOME/gradle/wrapper/gradle-wrapper.jar" "$@" 2>/dev/null || exec gradle "$@"
""")
os.chmod('twa/gradlew', 0o755)

# Download gradle wrapper jar
try:
    jar_url = 'https://raw.githubusercontent.com/gradle/gradle/v8.9.0/gradle/wrapper/gradle-wrapper.jar'
    urllib.request.urlretrieve(jar_url, 'twa/gradle/wrapper/gradle-wrapper.jar')
    print("Gradle wrapper jar downloaded")
except Exception as e:
    print(f"Wrapper jar download failed: {e} - will use system gradle")

# AndroidManifest.xml
with open('twa/app/src/main/AndroidManifest.xml', 'w') as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <queries>
        <intent>
            <action android:name="android.intent.action.VIEW" />
            <category android:name="android.intent.category.BROWSABLE" />
            <data android:scheme="https" />
        </intent>
    </queries>
    <application
        android:label="Income Splitter"
        android:icon="@mipmap/ic_launcher"
        android:allowBackup="true">
        <activity
            android:name="com.google.androidbrowserhelper.trusted.LauncherActivity"
            android:exported="true">
            <meta-data
                android:name="android.support.customtabs.trusted.DEFAULT_URL"
                android:value="https://incomesplitter.github.io/income-splitter2/" />
            <meta-data
                android:name="android.support.customtabs.trusted.STATUS_BAR_COLOR"
                android:value="@color/colorPrimary" />
            <meta-data
                android:name="android.support.customtabs.trusted.SPLASH_SCREEN_BACKGROUND_COLOR"
                android:value="@color/colorPrimary" />
            <meta-data
                android:name="android.support.customtabs.trusted.FALLBACK_STRATEGY"
                android:value="customtabs" />
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <intent-filter android:autoVerify="true">
                <action android:name="android.intent.action.VIEW" />
                <category android:name="android.intent.category.DEFAULT" />
                <category android:name="android.intent.category.BROWSABLE" />
                <data android:scheme="https"
                      android:host="incomesplitter.github.io"
                      android:pathPrefix="/income-splitter2" />
            </intent-filter>
        </activity>
        <service
            android:name="com.google.androidbrowserhelper.trusted.DelegationService"
            android:exported="true"
            android:enabled="true">
            <intent-filter>
                <action android:name="android.support.customtabs.trusted.TRUSTED_WEB_ACTIVITY_SERVICE" />
                <category android:name="android.intent.category.DEFAULT" />
            </intent-filter>
        </service>
    </application>
</manifest>
""")

# colors.xml
with open('twa/app/src/main/res/values/colors.xml', 'w') as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="colorPrimary">#0f1117</color>
</resources>
""")

# styles.xml
with open('twa/app/src/main/res/values/styles.xml', 'w') as f:
    f.write("""<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="Theme.AppCompat.NoActionBar">
        <item name="android:windowBackground">@color/colorPrimary</item>
        <item name="android:statusBarColor">@color/colorPrimary</item>
    </style>
</resources>
""")

print("All project files created successfully")
import subprocess
result = subprocess.run(['find', 'twa', '-type', 'f'], capture_output=True, text=True)
print(result.stdout)
