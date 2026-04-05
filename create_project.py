import os
import shutil
import urllib.request
import stat

for d in [
    'twa/app/src/main/res/mipmap-mdpi',
    'twa/app/src/main/res/mipmap-hdpi',
    'twa/app/src/main/res/mipmap-xhdpi',
    'twa/app/src/main/res/mipmap-xxhdpi',
    'twa/app/src/main/res/mipmap-xxxhdpi',
    'twa/app/src/main/res/values',
    'twa/gradle/wrapper',
]:
    os.makedirs(d, exist_ok=True)

try:
    urllib.request.urlretrieve('https://incomesplitter.github.io/income-splitter2/icon-512.png', '/tmp/icon.png')
    for d in ['mipmap-mdpi','mipmap-hdpi','mipmap-xhdpi','mipmap-xxhdpi','mipmap-xxxhdpi']:
        shutil.copy('/tmp/icon.png', f'twa/app/src/main/res/{d}/ic_launcher.png')
    print("Icon downloaded")
except Exception as e:
    print(f"Icon failed: {e}")

shutil.copy('app.keystore', 'twa/app.keystore')

try:
    urllib.request.urlretrieve(
        'https://raw.githubusercontent.com/gradle/gradle/v8.7.0/gradle/wrapper/gradle-wrapper.jar',
        'twa/gradle/wrapper/gradle-wrapper.jar'
    )
    print("Wrapper jar downloaded")
except Exception as e:
    print(f"Wrapper jar failed: {e}")

gradlew = '#!/usr/bin/env sh\nAPP_HOME="$(cd "$(dirname "$0")" && pwd)"\nexec java -classpath "$APP_HOME/gradle/wrapper/gradle-wrapper.jar" org.gradle.wrapper.GradleWrapperMain "$@"\n'
with open('twa/gradlew', 'w') as f:
    f.write(gradlew)
os.chmod('twa/gradlew', stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)

with open('twa/gradle/wrapper/gradle-wrapper.properties', 'w') as f:
    f.write('distributionBase=GRADLE_USER_HOME\ndistributionPath=wrapper/dists\ndistributionUrl=https\\://services.gradle.org/distributions/gradle-8.7-bin.zip\nzipStoreBase=GRADLE_USER_HOME\nzipStorePath=wrapper/dists\n')

with open('twa/settings.gradle', 'w') as f:
    f.write('pluginManagement {\n    repositories {\n        google()\n        mavenCentral()\n        gradlePluginPortal()\n    }\n}\ndependencyResolutionManagement {\n    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)\n    repositories {\n        google()\n        mavenCentral()\n    }\n}\nrootProject.name = \'IncomeSplitter\'\ninclude \':app\'\n')

with open('twa/build.gradle', 'w') as f:
    f.write('plugins {\n    id \'com.android.application\' version \'8.5.2\' apply false\n}\n')

with open('twa/app/build.gradle', 'w') as f:
    f.write('plugins {\n    id \'com.android.application\'\n}\nandroid {\n    namespace \'com.incomesplitter.app\'\n    compileSdk 34\n    defaultConfig {\n        applicationId \'com.incomesplitter.app\'\n        minSdk 21\n        targetSdk 34\n        versionCode 1\n        versionName \'1.0\'\n    }\n    signingConfigs {\n        release {\n            storeFile file(\'app.keystore\')\n            storePassword \'android123\'\n            keyAlias \'incomesplitter\'\n            keyPassword \'android123\'\n        }\n    }\n    buildTypes {\n        release {\n            signingConfig signingConfigs.release\n            minifyEnabled false\n        }\n    }\n    compileOptions {\n        sourceCompatibility JavaVersion.VERSION_17\n        targetCompatibility JavaVersion.VERSION_17\n    }\n}\ndependencies {\n    implementation \'com.google.androidbrowserhelper:androidbrowserhelper:2.5.0\'\n    implementation \'androidx.appcompat:appcompat:1.6.1\'\n}\n')

with open('twa/gradle.properties', 'w') as f:
    f.write('android.useAndroidX=true\nandroid.enableJetifier=true\norg.gradle.jvmargs=-Xmx2048m\n')

with open('twa/app/src/main/AndroidManifest.xml', 'w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<manifest xmlns:android="http://schemas.android.com/apk/res/android">\n    <queries>\n        <intent>\n            <action android:name="android.intent.action.VIEW" />\n            <category android:name="android.intent.category.BROWSABLE" />\n            <data android:scheme="https" />\n        </intent>\n    </queries>\n    <application\n        android:label="Income Splitter"\n        android:icon="@mipmap/ic_launcher"\n        android:allowBackup="true">\n        <activity\n            android:name="com.google.androidbrowserhelper.trusted.LauncherActivity"\n            android:exported="true">\n            <meta-data android:name="android.support.customtabs.trusted.DEFAULT_URL" android:value="https://incomesplitter.github.io/income-splitter2/" />\n            <meta-data android:name="android.support.customtabs.trusted.STATUS_BAR_COLOR" android:value="@color/colorPrimary" />\n            <meta-data android:name="android.support.customtabs.trusted.SPLASH_SCREEN_BACKGROUND_COLOR" android:value="@color/colorPrimary" />\n            <meta-data android:name="android.support.customtabs.trusted.FALLBACK_STRATEGY" android:value="customtabs" />\n            <intent-filter>\n                <action android:name="android.intent.action.MAIN" />\n                <category android:name="android.intent.category.LAUNCHER" />\n            </intent-filter>\n            <intent-filter android:autoVerify="true">\n                <action android:name="android.intent.action.VIEW" />\n                <category android:name="android.intent.category.DEFAULT" />\n                <category android:name="android.intent.category.BROWSABLE" />\n                <data android:scheme="https" android:host="incomesplitter.github.io" android:pathPrefix="/income-splitter2" />\n            </intent-filter>\n        </activity>\n        <service android:name="com.google.androidbrowserhelper.trusted.DelegationService" android:exported="true" android:enabled="true">\n            <intent-filter>\n                <action android:name="android.support.customtabs.trusted.TRUSTED_WEB_ACTIVITY_SERVICE" />\n                <category android:name="android.intent.category.DEFAULT" />\n            </intent-filter>\n        </service>\n    </application>\n</manifest>\n')

with open('twa/app/src/main/res/values/colors.xml', 'w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="colorPrimary">#0f1117</color>\n</resources>\n')

with open('twa/app/src/main/res/values/styles.xml', 'w') as f:
    f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <style name="AppTheme" parent="Theme.AppCompat.NoActionBar">\n        <item name="android:windowBackground">@color/colorPrimary</item>\n        <item name="android:statusBarColor">@color/colorPrimary</item>\n    </style>\n</resources>\n')

print("All files created successfully")
import subprocess
print(subprocess.run(['find', 'twa', '-type', 'f'], capture_output=True, text=True).stdout)
