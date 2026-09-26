package com.generated.webviewapp

import android.annotation.SuppressLint
import android.os.Bundle
import android.view.View
import android.view.WindowManager
import android.webkit.WebChromeClient
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import com.generated.webviewapp.databinding.ActivityMainBinding

class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding

    private val runtimePermissions: Array<String> by lazy {
        val declared = try {
            packageManager.getPackageInfo(packageName, android.content.pm.PackageManager.GET_PERMISSIONS)
                .requestedPermissions ?: emptyArray()
        } catch (e: Exception) { emptyArray() }

        val dangerous = setOf(
            "android.permission.ACCESS_FINE_LOCATION", "android.permission.ACCESS_COARSE_LOCATION",
            "android.permission.ACCESS_BACKGROUND_LOCATION", "android.permission.CAMERA",
            "android.permission.RECORD_AUDIO", "android.permission.READ_CONTACTS",
            "android.permission.WRITE_CONTACTS", "android.permission.READ_CALL_LOG",
            "android.permission.WRITE_CALL_LOG", "android.permission.CALL_PHONE",
            "android.permission.ANSWER_PHONE_CALLS", "android.permission.READ_PHONE_STATE",
            "android.permission.READ_PHONE_NUMBERS", "android.permission.SEND_SMS",
            "android.permission.RECEIVE_SMS", "android.permission.READ_SMS",
            "android.permission.RECEIVE_MMS", "android.permission.READ_CALENDAR",
            "android.permission.WRITE_CALENDAR", "android.permission.BODY_SENSORS",
            "android.permission.ACTIVITY_RECOGNITION", "android.permission.POST_NOTIFICATIONS",
            "android.permission.BLUETOOTH_CONNECT", "android.permission.BLUETOOTH_SCAN",
            "android.permission.BLUETOOTH_ADVERTISE", "android.permission.READ_MEDIA_IMAGES",
            "android.permission.READ_MEDIA_VIDEO", "android.permission.READ_MEDIA_AUDIO"
        )
        declared.filter { it in dangerous }.toTypedArray()
    }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        if (GeneratedConfig.FULLSCREEN) applyFullscreen()
        if (GeneratedConfig.KEEP_SCREEN_AWAKE) {
            window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        }

        if (runtimePermissions.isNotEmpty()) {
            ActivityCompat.requestPermissions(this, runtimePermissions, 1001)
        }

        setupWebView()
    }

    private fun applyFullscreen() {
        @Suppress("DEPRECATION")
        window.decorView.systemUiVisibility = (
            View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                or View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                or View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                or View.SYSTEM_UI_FLAG_FULLSCREEN
                or View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
            )
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun setupWebView() {
        val webView = binding.webView
        val settings: WebSettings = webView.settings

        settings.javaScriptEnabled = GeneratedConfig.JAVASCRIPT_ENABLED
        settings.domStorageEnabled = GeneratedConfig.DOM_STORAGE_ENABLED
        settings.setSupportZoom(GeneratedConfig.ZOOM_CONTROLS)
        settings.builtInZoomControls = GeneratedConfig.ZOOM_CONTROLS
        settings.displayZoomControls = false
        settings.loadWithOverviewMode = true
        settings.useWideViewPort = true

        if (GeneratedConfig.CUSTOM_USER_AGENT.isNotBlank()) {
            settings.userAgentString = GeneratedConfig.CUSTOM_USER_AGENT
        }

        settings.cacheMode = when (GeneratedConfig.CACHE_MODE) {
            "LOAD_NO_CACHE" -> WebSettings.LOAD_NO_CACHE
            "LOAD_CACHE_ELSE_NETWORK" -> WebSettings.LOAD_CACHE_ELSE_NETWORK
            else -> WebSettings.LOAD_DEFAULT
        }

        if (GeneratedConfig.ALLOW_MIXED_CONTENT) {
            settings.mixedContentMode = WebSettings.MIXED_CONTENT_ALWAYS_ALLOW
        }

        webView.webChromeClient = WebChromeClient()
        webView.webViewClient = object : WebViewClient() {
            override fun onPageFinished(view: WebView?, url: String?) {
                super.onPageFinished(view, url)
            }
        }

        webView.loadUrl(resolveStartUrl())
    }

    private fun resolveStartUrl(): String =
        if (GeneratedConfig.REMOTE_URL.isNotBlank()) {
            GeneratedConfig.REMOTE_URL
        } else {
            "file:///android_asset/www/index.html"
        }

    override fun onDestroy() {
        if (GeneratedConfig.CLEAR_DATA_ON_EXIT) {
            binding.webView.clearCache(true)
            binding.webView.clearHistory()
            android.webkit.CookieManager.getInstance().removeAllCookies(null)
            android.webkit.WebStorage.getInstance().deleteAllData()
        }
        super.onDestroy()
    }

    override fun onBackPressed() {
        if (binding.webView.canGoBack()) binding.webView.goBack() else super.onBackPressed()
    }
}
