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
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.civicfix.app.ui.theme.CivicFixBlue
import com.civicfix.app.ui.theme.CivicFixBlueDark
import com.civicfix.app.ui.theme.CivicFixBlueLight

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AboutScreen(onBack: () -> Unit) {
    val context = LocalContext.current

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("About CivicFix", fontWeight = FontWeight.Bold) },
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
        ) {
            // Hero Header
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(
                        Brush.verticalGradient(
                            colors = listOf(CivicFixBlue, CivicFixBlueDark)
                        )
                    )
                    .padding(vertical = 40.dp, horizontal = 24.dp),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    Box(
                        modifier = Modifier
                            .size(80.dp)
                            .clip(CircleShape)
                            .background(Color.White.copy(alpha = 0.2f)),
                        contentAlignment = Alignment.Center
                    ) {
                        Icon(
                            Icons.Outlined.AccountBalance,
                            contentDescription = null,
                            modifier = Modifier.size(40.dp),
                            tint = Color.White
                        )
                    }
                    Spacer(Modifier.height(16.dp))
                    Text(
                        "CivicFix",
                        fontSize = 28.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )
                    Text(
                        "v1.0.0",
                        fontSize = 14.sp,
                        color = Color.White.copy(alpha = 0.7f)
                    )
                    Spacer(Modifier.height(8.dp))
                    Text(
                        "Empowering Citizens, Fixing Communities",
                        fontSize = 15.sp,
                        color = Color.White.copy(alpha = 0.9f),
                        textAlign = TextAlign.Center
                    )
                }
            }

            Column(modifier = Modifier.padding(20.dp)) {
                // What CivicFix Does
                AboutSectionCard(
                    title = "What CivicFix Does",
                    icon = Icons.Outlined.Lightbulb
                ) {
                    Text(
                        "CivicFix is a civic issue reporting platform that connects citizens with local authorities. " +
                                "Report potholes, broken streetlights, garbage dumps, water leakages, and other " +
                                "infrastructure problems in your community with just a photo and location.",
                        fontSize = 14.sp,
                        color = Color(0xFF4A5568),
                        lineHeight = 22.sp
                    )
                    Spacer(Modifier.height(12.dp))
                    FeatureRow("📸", "Submit reports with photo evidence & GPS location")
                    FeatureRow("🔐", "Secure OTP-based email authentication")
                    FeatureRow("📍", "Automatic location detection & map selection")
                    FeatureRow("📊", "Track your report status in real-time")
                    FeatureRow("🐦", "Public issue visibility via X/Twitter integration")
                    FeatureRow("🏛️", "Direct escalation to local authorities")
                }

                Spacer(Modifier.height(16.dp))

                // Why This App Exists
                AboutSectionCard(
                    title = "Why CivicFix Exists",
                    icon = Icons.Outlined.EmojiObjects
                ) {
                    Text(
                        "Too many civic issues go unreported because the process is complicated or people don't know " +
                                "who to contact. CivicFix removes these barriers by providing a simple, photo-based " +
                                "reporting system that automatically routes complaints to the right authorities.\n\n" +
                                "Our mission is to make every citizen a stakeholder in their community's well-being " +
                                "and to hold local bodies accountable through transparent, public issue tracking.",
                        fontSize = 14.sp,
                        color = Color(0xFF4A5568),
                        lineHeight = 22.sp
                    )
                }

                Spacer(Modifier.height(16.dp))

                // Developers Section
                AboutSectionCard(
                    title = "Meet the Developers",
                    icon = Icons.Outlined.Code
                ) {
                    DeveloperCard(
                        name = "Priyanjal Paliwal",
                        role = "Full-Stack Developer",
                        email = "paliwalpriyanjal@gmail.com",
                        linkedInUrl = "https://www.linkedin.com/in/priyanjal-paliwal-806534331",
                        githubUrl = "https://github.com/paliwalpriyanjal-hash",
                        context = context
                    )
                    Spacer(Modifier.height(12.dp))
                    HorizontalDivider(color = Color(0xFFE2E8F0))
                    Spacer(Modifier.height(12.dp))
                    DeveloperCard(
                        name = "Sarvesh Baghel",
                        role = "Full-Stack Developer",
                        email = "sarveshsingh8462@gmail.com",
                        linkedInUrl = "https://www.linkedin.com/in/sarvesh-baghel-b3a726274",
                        githubUrl = "https://github.com/sarveshbaghel",
                        context = context
                    )
                }

                Spacer(Modifier.height(16.dp))

                // Tech Stack
                AboutSectionCard(
                    title = "Built With",
                    icon = Icons.Outlined.Build
                ) {
                    FeatureRow("📱", "Kotlin & Jetpack Compose")
                    FeatureRow("⚡", "FastAPI Backend")
                    FeatureRow("🔥", "Firebase Authentication")
                    FeatureRow("🗺️", "Google Maps SDK")
                    FeatureRow("🐦", "X/Twitter API Integration")
                }

                Spacer(Modifier.height(24.dp))

                Text(
                    "Made with ❤\uFE0F in Gwalior, India",
                    fontSize = 13.sp,
                    color = Color(0xFF94A3B8),
                    modifier = Modifier.fillMaxWidth(),
                    textAlign = TextAlign.Center
                )
                Spacer(Modifier.height(8.dp))
                Text(
                    "© 2026 CivicFix. All rights reserved.",
                    fontSize = 12.sp,
                    color = Color(0xFFBDC3CB),
                    modifier = Modifier.fillMaxWidth(),
                    textAlign = TextAlign.Center
                )
                Spacer(Modifier.height(24.dp))
            }
        }
    }
}

@Composable
private fun AboutSectionCard(
    title: String,
    icon: ImageVector,
    content: @Composable ColumnScope.() -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(modifier = Modifier.padding(20.dp)) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Box(
                    modifier = Modifier
                        .size(36.dp)
                        .clip(RoundedCornerShape(10.dp))
                        .background(CivicFixBlueLight),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(icon, contentDescription = null, tint = CivicFixBlue, modifier = Modifier.size(20.dp))
                }
                Spacer(Modifier.width(12.dp))
                Text(title, fontSize = 18.sp, fontWeight = FontWeight.Bold, color = Color(0xFF1A202C))
            }
            Spacer(Modifier.height(16.dp))
            content()
        }
    }
}

@Composable
private fun FeatureRow(emoji: String, text: String) {
    Row(
        modifier = Modifier.padding(vertical = 4.dp),
        verticalAlignment = Alignment.Top
    ) {
        Text(emoji, fontSize = 14.sp)
        Spacer(Modifier.width(10.dp))
        Text(text, fontSize = 14.sp, color = Color(0xFF4A5568), lineHeight = 20.sp)
    }
}

@Composable
private fun DeveloperCard(
    name: String,
    role: String,
    email: String,
    linkedInUrl: String,
    githubUrl: String,
    context: android.content.Context
) {
    Column {
        Row(verticalAlignment = Alignment.CenterVertically) {
            Box(
                modifier = Modifier
                    .size(48.dp)
                    .clip(CircleShape)
                    .background(CivicFixBlue.copy(alpha = 0.1f)),
                contentAlignment = Alignment.Center
            ) {
                Text(
                    name.split(" ").map { it.first() }.joinToString(""),
                    fontSize = 16.sp,
                    fontWeight = FontWeight.Bold,
                    color = CivicFixBlue
                )
            }
            Spacer(Modifier.width(14.dp))
            Column {
                Text(name, fontSize = 16.sp, fontWeight = FontWeight.SemiBold, color = Color(0xFF1A202C))
                Text(role, fontSize = 13.sp, color = Color(0xFF64748B))
            }
        }
        Spacer(Modifier.height(10.dp))
        Row(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
            SocialChip(
                label = "LinkedIn",
                icon = Icons.Outlined.Person,
                onClick = {
                    context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(linkedInUrl)))
                }
            )
            SocialChip(
                label = "GitHub",
                icon = Icons.Outlined.Code,
                onClick = {
                    context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(githubUrl)))
                }
            )
            SocialChip(
                label = "Email",
                icon = Icons.Outlined.Email,
                onClick = {
                    context.startActivity(Intent(Intent.ACTION_SENDTO, Uri.parse("mailto:$email")))
                }
            )
        }
    }
}

@Composable
private fun SocialChip(label: String, icon: ImageVector, onClick: () -> Unit) {
    Surface(
        modifier = Modifier
            .clip(RoundedCornerShape(20.dp))
            .clickable(onClick = onClick),
        color = CivicFixBlueLight,
        shape = RoundedCornerShape(20.dp)
    ) {
        Row(
            modifier = Modifier.padding(horizontal = 12.dp, vertical = 6.dp),
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(icon, contentDescription = null, modifier = Modifier.size(14.dp), tint = CivicFixBlue)
            Spacer(Modifier.width(4.dp))
            Text(label, fontSize = 12.sp, color = CivicFixBlue, fontWeight = FontWeight.Medium)
        }
    }
}
