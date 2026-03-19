package com.civicfix.app.ui.screens

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.civicfix.app.ui.theme.CivicFixBlue
import com.civicfix.app.ui.theme.CivicFixBlueLight

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HelpSupportScreen(onBack: () -> Unit) {
    val context = LocalContext.current

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Help & Support", fontWeight = FontWeight.Bold) },
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
            // Header
            Card(
                modifier = Modifier.fillMaxWidth(),
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(containerColor = CivicFixBlueLight)
            ) {
                Column(
                    modifier = Modifier.padding(24.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Box(
                        modifier = Modifier
                            .size(56.dp)
                            .clip(CircleShape)
                            .background(CivicFixBlue),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            Icons.Outlined.SupportAgent,
                            contentDescription = null,
                            tint = Color.White,
                            modifier = Modifier.size(28.dp)
                        )
                    }
                    Spacer(Modifier.height(12.dp))
                    Text(
                        "How can we help you?",
                        fontSize = 20.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color(0xFF1A202C)
                    )
                    Spacer(Modifier.height(4.dp))
                    Text(
                        "We're here to assist you with any questions or issues.",
                        fontSize = 14.sp,
                        color = Color(0xFF64748B)
                    )
                }
            }

            Spacer(Modifier.height(20.dp))

            // Support Options
            SupportOptionCard(
                icon = Icons.Outlined.Email,
                title = "Contact Support",
                description = "Reach our support team via email",
                onClick = {
                    val intent = Intent(Intent.ACTION_SENDTO).apply {
                        data = Uri.parse("mailto:support@civicfix.app")
                        putExtra(Intent.EXTRA_SUBJECT, "CivicFix Support Request")
                    }
                    context.startActivity(intent)
                }
            )

            Spacer(Modifier.height(12.dp))

            SupportOptionCard(
                icon = Icons.Outlined.BugReport,
                title = "Report a Bug",
                description = "Found something broken? Let us know",
                onClick = {
                    val intent = Intent(Intent.ACTION_SENDTO).apply {
                        data = Uri.parse("mailto:bugs@civicfix.app")
                        putExtra(Intent.EXTRA_SUBJECT, "CivicFix Bug Report")
                        putExtra(Intent.EXTRA_TEXT, "Device: \nAndroid Version: \nBug Description: \n\n")
                    }
                    context.startActivity(intent)
                }
            )

            Spacer(Modifier.height(12.dp))

            SupportOptionCard(
                icon = Icons.Outlined.TipsAndUpdates,
                title = "Suggest a Feature",
                description = "Have an idea? We'd love to hear it",
                onClick = {
                    val intent = Intent(Intent.ACTION_SENDTO).apply {
                        data = Uri.parse("mailto:feedback@civicfix.app")
                        putExtra(Intent.EXTRA_SUBJECT, "CivicFix Feature Suggestion")
                    }
                    context.startActivity(intent)
                }
            )

            Spacer(Modifier.height(24.dp))

            // FAQ Section
            Text(
                "Frequently Asked Questions",
                fontSize = 18.sp,
                fontWeight = FontWeight.Bold,
                color = Color(0xFF1A202C)
            )
            Spacer(Modifier.height(12.dp))

            FaqItem(
                question = "How do I report a civic issue?",
                answer = "Tap the 'Report Issue' button on the home screen, take a photo of the problem, " +
                        "select the issue type, add a description, and your GPS location will be automatically captured. " +
                        "Then simply submit your report."
            )
            FaqItem(
                question = "How do I track my report status?",
                answer = "Go to 'My Reports' from the home screen to see all your submitted reports. " +
                        "Each report shows its current status: pending, approved, or resolved."
            )
            FaqItem(
                question = "What is the X/Twitter posting feature?",
                answer = "When enabled in Settings, your reports can be shared on X (Twitter) for public " +
                        "visibility and to draw attention from local authorities."
            )
            FaqItem(
                question = "Is my data secure?",
                answer = "Yes. We use encrypted connections, secure OTP authentication, and your data is " +
                        "only used for civic issue reporting. Read our Privacy Policy for more details."
            )
            FaqItem(
                question = "Can I choose my location on the map?",
                answer = "Yes! When creating a report, you can use your live GPS location or tap " +
                        "'Select from Map' to manually choose the location of the issue."
            )

            Spacer(Modifier.height(24.dp))
        }
    }
}

@Composable
private fun SupportOptionCard(
    icon: ImageVector,
    title: String,
    description: String,
    onClick: () -> Unit
) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(14.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 1.dp)
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Box(
                modifier = Modifier
                    .size(44.dp)
                    .clip(RoundedCornerShape(12.dp))
                    .background(CivicFixBlueLight),
                contentAlignment = Alignment.Center
            ) {
                Icon(icon, contentDescription = null, tint = CivicFixBlue, modifier = Modifier.size(22.dp))
            }
            Spacer(Modifier.width(14.dp))
            Column(modifier = Modifier.weight(1f)) {
                Text(title, fontSize = 15.sp, fontWeight = FontWeight.SemiBold, color = Color(0xFF1A202C))
                Text(description, fontSize = 13.sp, color = Color(0xFF94A3B8))
            }
            Icon(Icons.Outlined.ChevronRight, contentDescription = null, tint = Color(0xFFCBD5E1))
        }
    }
}

@Composable
private fun FaqItem(question: String, answer: String) {
    Card(
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 4.dp),
        shape = RoundedCornerShape(12.dp),
        colors = CardDefaults.cardColors(containerColor = Color(0xFFF8FAFC)),
        elevation = CardDefaults.cardElevation(defaultElevation = 0.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                "Q: $question",
                fontSize = 14.sp,
                fontWeight = FontWeight.SemiBold,
                color = Color(0xFF1A202C)
            )
            Spacer(Modifier.height(6.dp))
            Text(
                answer,
                fontSize = 13.sp,
                color = Color(0xFF64748B),
                lineHeight = 20.sp
            )
        }
    }
}
