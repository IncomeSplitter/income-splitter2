package com.incomesplitter.app

import android.graphics.Color
import android.os.Bundle
import androidx.browser.trusted.TrustedWebActivityIntentBuilder
import androidx.browser.trusted.TrustedWebActivityLauncherActivity
import androidx.core.content.ContextCompat

class LauncherActivity : TrustedWebActivityLauncherActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Use the color defined in colors.xml OR fallback to literal
        val themeColor = try {
            ContextCompat.getColor(this, R.color.theme_color) 
        } catch (e: Exception) {
            Color.parseColor("#0F1117")
        }

        // Build the Trusted Web Activity intent
        val builder = TrustedWebActivityIntentBuilder("https://yourwebsite.com/income-splitter2/")
            .setToolbarColor(themeColor)
            .setStartAnimations(this, android.R.anim.fade_in, android.R.anim.fade_out)
            .setExitAnimations(this, android.R.anim.fade_in, android.R.anim.fade_out)

        // Launch the TWA
        launchTwa(builder)
    }
}
