package com.civicfix.app.ui.screens

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import androidx.compose.material.icons.automirrored.outlined.ExitToApp
import androidx.compose.material.icons.automirrored.outlined.HelpOutline
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.civicfix.app.ui.theme.CivicFixBlue
import com.civicfix.app.ui.theme.CivicFixBlueDark
import com.civicfix.app.ui.theme.CivicFixBlueLight
import com.google.firebase.auth.FirebaseAuth
import androidx.core.content.FileProvider
import java.io.File

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ProfileScreen(
    onBack: () -> Unit,
    onLogout: () -> Unit,
    onSettingsClick: () -> Unit,
    onAboutClick: () -> Unit,
    onHelpClick: () -> Unit,
    onPrivacyClick: () -> Unit
) {
    val context = LocalContext.current
    val firebaseUser = FirebaseAuth.getInstance().currentUser

    // User info from Firebase
    val userName = firebaseUser?.displayName
        ?: firebaseUser?.email?.substringBefore("@")
        ?: "My Account"
    val userEmail = firebaseUser?.email ?: ""

    // Profile photo state
    var profileImageUri by remember { mutableStateOf<Uri?>(firebaseUser?.photoUrl) }
    var showImagePickerDialog by remember { mutableStateOf(false) }

    // Gallery picker
    val galleryLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        if (uri != null) profileImageUri = uri
    }

    // Camera capture
    var cameraImageUri by remember { mutableStateOf<Uri?>(null) }
    val cameraLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.TakePicture()
    ) { success: Boolean ->
        if (success && cameraImageUri != null) {
            profileImageUri = cameraImageUri
        }
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Profile", fontWeight = FontWeight.Bold) },
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
            // Profile Header with gradient
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .background(
                        Brush.verticalGradient(
                            colors = listOf(CivicFixBlue, CivicFixBlueDark)
                        )
                    )
                    .padding(vertical = 32.dp),
                contentAlignment = Alignment.Center
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally) {
                    // Profile Avatar
                    Box(contentAlignment = Alignment.BottomEnd) {
                        Box(
                            modifier = Modifier
                                .size(100.dp)
                                .clip(CircleShape)
                                .background(Color.White.copy(alpha = 0.2f))
                                .border(3.dp, Color.White.copy(alpha = 0.5f), CircleShape)
                                .clickable { showImagePickerDialog = true },
                            contentAlignment = Alignment.Center
                        ) {
                            if (profileImageUri != null) {
                                AsyncImage(
                                    model = ImageRequest.Builder(context)
                                        .data(profileImageUri)
                                        .crossfade(true)
                                        .build(),
                                    contentDescription = "Profile photo",
                                    modifier = Modifier
                                        .fillMaxSize()
                                        .clip(CircleShape),
                                    contentScale = ContentScale.Crop
                                )
                            } else {
                                Icon(
                                    Icons.Outlined.Person,
                                    contentDescription = null,
                                    modifier = Modifier.size(50.dp),
                                    tint = Color.White
                                )
                            }
                        }
                        // Edit badge
                        Box(
                            modifier = Modifier
                                .size(30.dp)
                                .clip(CircleShape)
                                .background(Color.White)
                                .clickable { showImagePickerDialog = true },
                            contentAlignment = Alignment.Center
                        ) {
                            Icon(
                                Icons.Outlined.CameraAlt,
                                contentDescription = "Edit photo",
                                modifier = Modifier.size(16.dp),
                                tint = CivicFixBlue
                            )
                        }
                    }

                    Spacer(Modifier.height(14.dp))
                    Text(
                        userName,
                        fontSize = 22.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )
                    if (userEmail.isNotEmpty()) {
                        Spacer(Modifier.height(4.dp))
                        Text(
                            userEmail,
                            fontSize = 14.sp,
                            color = Color.White.copy(alpha = 0.8f)
                        )
                    }
                }
            }

            // Menu Items
            Column(modifier = Modifier.padding(horizontal = 20.dp, vertical = 16.dp)) {
                Text(
                    "GENERAL",
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF94A3B8),
                    modifier = Modifier.padding(start = 4.dp, bottom = 8.dp)
                )

                ProfileMenuItem(
                    icon = Icons.Outlined.Settings,
                    text = "Settings",
                    subtitle = "Twitter posting, preferences",
                    onClick = onSettingsClick
                )
                ProfileMenuItem(
                    icon = Icons.Outlined.Info,
                    text = "About CivicFix",
                    subtitle = "App info & developer details",
                    onClick = onAboutClick
                )

                Spacer(Modifier.height(16.dp))
                Text(
                    "SUPPORT",
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color(0xFF94A3B8),
                    modifier = Modifier.padding(start = 4.dp, bottom = 8.dp)
                )

                ProfileMenuItem(
                    icon = Icons.AutoMirrored.Outlined.HelpOutline,
                    text = "Help & Support",
                    subtitle = "FAQ, contact, bug reports",
                    onClick = onHelpClick
                )
                ProfileMenuItem(
                    icon = Icons.Outlined.PrivacyTip,
                    text = "Privacy Policy",
                    subtitle = "Data usage & your rights",
                    onClick = onPrivacyClick
                )

                Spacer(Modifier.height(16.dp))
                HorizontalDivider(color = Color(0xFFE2E8F0))
                Spacer(Modifier.height(16.dp))

                // Logout Button
                ProfileMenuItem(
                    icon = Icons.AutoMirrored.Outlined.ExitToApp,
                    text = "Logout",
                    onClick = onLogout,
                    isDestructive = true
                )
            }
        }
    }

    // Image Picker Dialog
    if (showImagePickerDialog) {
        AlertDialog(
            onDismissRequest = { showImagePickerDialog = false },
            title = { Text("Change Profile Photo", fontWeight = FontWeight.Bold) },
            text = { Text("Choose how you'd like to update your profile photo.") },
            confirmButton = {
                TextButton(onClick = {
                    showImagePickerDialog = false
                    galleryLauncher.launch("image/*")
                }) {
                    Text("📸 Gallery")
                }
            },
            dismissButton = {
                TextButton(onClick = {
                    showImagePickerDialog = false
                    try {
                        val imageFile = File(context.cacheDir, "profile_photo_${System.currentTimeMillis()}.jpg")
                        val uri = FileProvider.getUriForFile(
                            context,
                            "${context.packageName}.fileprovider",
                            imageFile
                        )
                        cameraImageUri = uri
                        cameraLauncher.launch(uri)
                    } catch (e: Exception) {
                        // Fallback to gallery if camera fails
                        galleryLauncher.launch("image/*")
                    }
                }) {
                    Text("📷 Camera")
                }
            }
        )
    }
}

@Composable
private fun ProfileMenuItem(
    icon: ImageVector,
    text: String,
    subtitle: String? = null,
    onClick: () -> Unit,
    isDestructive: Boolean = false
) {
    val contentColor = if (isDestructive) Color(0xFFEF4444) else Color(0xFF1A202C)

    Row(
        modifier = Modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .clickable(onClick = onClick)
            .padding(14.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier
                .size(40.dp)
                .clip(RoundedCornerShape(10.dp))
                .background(
                    if (isDestructive) Color(0xFFFEE2E2)
                    else CivicFixBlueLight
                ),
            contentAlignment = Alignment.Center
        ) {
            Icon(
                imageVector = icon,
                contentDescription = null,
                tint = contentColor,
                modifier = Modifier.size(20.dp)
            )
        }
        Spacer(Modifier.width(14.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = text,
                fontSize = 15.sp,
                fontWeight = FontWeight.Medium,
                color = contentColor
            )
            if (subtitle != null) {
                Text(
                    text = subtitle,
                    fontSize = 12.sp,
                    color = Color(0xFF94A3B8)
                )
            }
        }
        if (!isDestructive) {
            Icon(
                Icons.Outlined.ChevronRight,
                contentDescription = null,
                tint = Color(0xFFCBD5E1)
            )
        }
    }
}
