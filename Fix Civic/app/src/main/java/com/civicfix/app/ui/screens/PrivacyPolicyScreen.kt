package com.civicfix.app.ui.screens

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.civicfix.app.ui.theme.CivicFixBlue

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PrivacyPolicyScreen(onBack: () -> Unit) {
    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Privacy Policy", fontWeight = FontWeight.Bold) },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Outlined.ArrowBack, contentDescription = "Back")
                    }
                },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = Color.White,
                    titleContentColor = Color(0xFF1A202C)
                )
            )
        }
    ) { padding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(rememberScrollState())
                .padding(20.dp)
        ) {
            Text(
                "CivicFix Privacy Policy",
                fontSize = 22.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF1A202C)
            )
            Text(
                "Last updated: March 2026",
                fontSize = 13.sp,
                color = Color(0xFF94A3B8),
                modifier = Modifier.padding(top = 4.dp, bottom = 20.dp)
            )

            PolicySection(
                title = "1. Information We Collect",
                content = "When you use CivicFix, we collect the following information:\n\n" +
                        "• Account Data: Your email address and display name when you create an account or sign in using Google.\n\n" +
                        "• Profile Data: Your profile photo if you choose to upload one.\n\n" +
                        "• Report Data: Photos, descriptions, issue types, and any other information you provide when submitting civic issue reports.\n\n" +
                        "• Location Data: GPS coordinates when you submit a report, either through automatic location detection or manual map selection. Location is only used for report accuracy.\n\n" +
                        "• Device Information: Basic device identifiers for rate limiting and security purposes."
            )

            PolicySection(
                title = "2. How We Use Your Information",
                content = "Your information is used to:\n\n" +
                        "• Process and display your civic issue reports to authorities\n" +
                        "• Authenticate your identity securely via OTP or Google Sign-In\n" +
                        "• Reverse geocode report locations to human-readable addresses\n" +
                        "• Communicate report status updates\n" +
                        "• Post reports to X/Twitter when you enable this feature in Settings\n" +
                        "• Improve the CivicFix platform and user experience"
            )

            PolicySection(
                title = "3. Authentication & Security",
                content = "CivicFix offers multiple secure sign-in methods:\n\n" +
                        "• OTP (One-Time Password): A 6-digit code is sent to your email. Codes expire after 5 minutes and are never stored in plain text.\n\n" +
                        "• Google Sign-In: We use Firebase Authentication to verify your Google account. We only receive your email and display name.\n\n" +
                        "• Passwords: If you use email/password login, your password is securely hashed using bcrypt and never stored in plaintext.\n\n" +
                        "• JWT Tokens: Session tokens are used for API authentication and expire after 24 hours."
            )

            PolicySection(
                title = "4. Location Data",
                content = "CivicFix uses your device location only when you actively submit a report. " +
                        "We never track your location in the background. You can also choose to " +
                        "select a location manually from the map instead of using GPS.\n\n" +
                        "Location data is attached to reports to help authorities identify and resolve issues at the correct location."
            )

            PolicySection(
                title = "5. Photos & Uploaded Images",
                content = "Photos you upload as evidence for reports are stored securely on our servers. " +
                        "Original evidence photos are never deleted or modified. " +
                        "Resolution photos uploaded by administrators are stored separately.\n\n" +
                        "Images are only used for civic issue documentation and are not shared with third parties except when posted to X/Twitter with your explicit consent."
            )

            PolicySection(
                title = "6. X/Twitter Sharing",
                content = "If the X/Twitter posting feature is enabled in Settings:\n\n" +
                        "• Your reports may be posted to X (Twitter) for public visibility.\n" +
                        "• Only the report description, location, and photo are shared — never your personal details.\n" +
                        "• You can disable this feature at any time from the Settings screen.\n" +
                        "• When an administrator resolves a report, a resolution tweet may be generated and posted."
            )

            PolicySection(
                title = "7. Data Retention",
                content = "Your account data is retained as long as your account is active. " +
                        "Report data is retained indefinitely to maintain civic records. " +
                        "You may request deletion of your account and associated data by contacting our support team."
            )

            PolicySection(
                title = "8. Data Protection",
                content = "We implement industry-standard security measures:\n\n" +
                        "• All data is transmitted over encrypted HTTPS connections\n" +
                        "• Passwords are hashed using bcrypt\n" +
                        "• Database access is restricted and monitored\n" +
                        "• API requests are rate-limited to prevent abuse\n" +
                        "• Authentication tokens expire automatically"
            )

            PolicySection(
                title = "9. Your Rights",
                content = "You have the right to:\n\n" +
                        "• Access your personal data\n" +
                        "• Correct inaccurate information\n" +
                        "• Request deletion of your account\n" +
                        "• Opt out of X/Twitter posting\n" +
                        "• Withdraw consent at any time"
            )

            PolicySection(
                title = "10. Contact Us",
                content = "If you have any questions about this Privacy Policy or our data practices, " +
                        "please contact us at:\n\n" +
                        "📧 Email: privacy@civicfix.app\n" +
                        "🌐 Website: https://civicfix.app"
            )

            Spacer(Modifier.height(24.dp))
        }
    }
}

@Composable
private fun PolicySection(title: String, content: String) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 6.dp),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFF8FAFC)),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                title,
                fontSize = 16.sp,
                fontWeight = FontWeight.Bold,
                color = CivicFixBlue
            )
            Spacer(Modifier.height(8.dp))
            Text(
                content,
                fontSize = 14.sp,
                color = Color(0xFF4A5568),
                lineHeight = 22.sp
            )
        }
    }
}
