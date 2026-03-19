package com.civicfix.app.ui.screens

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.outlined.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.foundation.BorderStroke
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.civicfix.app.data.api.RetrofitClient
import com.civicfix.app.data.models.FirebaseLoginRequest
import com.civicfix.app.data.models.OTPRequest
import com.civicfix.app.data.models.OTPVerifyRequest
import com.civicfix.app.ui.theme.CivicFixBlue
import com.civicfix.app.ui.theme.CivicFixBlueDark
import kotlinx.coroutines.launch
import kotlinx.coroutines.tasks.await
import android.util.Log
import android.app.Activity
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.ui.platform.LocalContext
import com.civicfix.app.R
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.android.gms.common.api.ApiException
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.GoogleAuthProvider

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SignupScreen(
    onSignupSuccess: (String) -> Unit,
    onNavigateToLogin: () -> Unit
) {
    var name by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var otp by remember { mutableStateOf("") }
    var isOtpSent by remember { mutableStateOf(false) }
    var loading by remember { mutableStateOf(false) }
    var error by remember { mutableStateOf<String?>(null) }
    var successMessage by remember { mutableStateOf<String?>(null) }
    val scope = rememberCoroutineScope()
    val context = LocalContext.current

    val googleSignInLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.StartActivityForResult()
    ) { result ->
        if (result.resultCode == Activity.RESULT_OK) {
            val task = GoogleSignIn.getSignedInAccountFromIntent(result.data)
            try {
                val account = task.getResult(ApiException::class.java)
                val idToken = account?.idToken
                if (idToken != null) {
                    scope.launch {
                        loading = true
                        error = null
                        val auth = FirebaseAuth.getInstance()
                        try {
                            val credential = GoogleAuthProvider.getCredential(idToken, null)
                            val authResult = auth.signInWithCredential(credential).await()
                            val user = authResult.user
                            
                            if (user != null) {
                                // Validations
                                if (user.email?.endsWith("@gmail.com") == true) {
                                    if (user.isEmailVerified) {
                                        val isGoogle = user.providerData.any { it.providerId == GoogleAuthProvider.PROVIDER_ID }
                                        if (isGoogle) {
                                            // Success Flow
                                            val firebaseToken = user.getIdToken(true).await().token
                                            if (firebaseToken != null) {
                                                val response = RetrofitClient.api.firebaseLogin(
                                                    com.civicfix.app.data.models.FirebaseLoginRequest(firebaseToken = firebaseToken)
                                                )
                                                Log.i("SignupScreen", "Google Login successful")
                                                onSignupSuccess(response.accessToken)
                                            } else {
                                                throw Exception("Failed to get Firebase token")
                                            }
                                        } else {
                                            auth.signOut()
                                            error = "Please sign in with Google."
                                        }
                                    } else {
                                        auth.signOut()
                                        error = "Email is not verified."
                                    }
                                } else {
                                    auth.signOut()
                                    error = "Only Gmail accounts are allowed."
                                }
                            } else {
                                throw Exception("User is null after sign in")
                            }
                        } catch (e: Exception) {
                            Log.e("SignupScreen", "Google Sign in failed", e)
                            error = "Google Sign in failed: ${e.message ?: e.localizedMessage}"
                            auth.signOut()
                        } finally {
                            loading = false
                        }
                    }
                } else {
                    error = "Google Sign in failed: Missing ID token"
                }
            } catch (e: ApiException) {
                Log.e("SignupScreen", "Google Sign-In Intent failed", e)
                error = "Google Sign in failed: ${e.message}"
                loading = false
            }
        } else {
            error = "Google Sign in cancelled."
            loading = false
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(
                Brush.linearGradient(
                    colors = listOf(CivicFixBlue, CivicFixBlueDark, Color(0xFF0A3D6B))
                )
            ),
        contentAlignment = Alignment.Center
    ) {
        Card(
            modifier = Modifier
                .widthIn(max = 400.dp)
                .padding(24.dp),
            shape = RoundedCornerShape(16.dp),
            colors = CardDefaults.cardColors(containerColor = Color.White),
            elevation = CardDefaults.cardElevation(defaultElevation = 12.dp)
        ) {
            Column(
                modifier = Modifier.padding(36.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text("Create Account", fontSize = 24.sp, fontWeight = FontWeight.Bold, color = CivicFixBlue)
                Text("Join CivicFix today", fontSize = 14.sp, color = Color(0xFF94A3B8))
                Spacer(Modifier.height(24.dp))

                error?.let {
                    Card(colors = CardDefaults.cardColors(containerColor = Color(0xFFFEF2F2)), shape = RoundedCornerShape(8.dp)) {
                        Text(it, color = Color(0xFFEF4444), fontSize = 13.sp, modifier = Modifier.padding(12.dp))
                    }
                    Spacer(Modifier.height(16.dp))
                }

                successMessage?.let {
                    Card(colors = CardDefaults.cardColors(containerColor = Color(0xFFD4EDDA)), shape = RoundedCornerShape(8.dp)) {
                        Text(it, color = Color(0xFF155724), fontSize = 13.sp, modifier = Modifier.padding(12.dp))
                    }
                    Spacer(Modifier.height(16.dp))
                }

                OutlinedTextField(
                    value = name, onValueChange = { name = it },
                    label = { Text("Display Name") },
                    leadingIcon = { Icon(Icons.Outlined.Person, null) },
                    modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(8.dp), singleLine = true
                )
                Spacer(Modifier.height(12.dp))

                OutlinedTextField(
                    value = email, onValueChange = { email = it },
                    label = { Text("Email") },
                    leadingIcon = { Icon(Icons.Outlined.Email, null) },
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email),
                    modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(8.dp), singleLine = true
                )
                Spacer(Modifier.height(12.dp))

                OutlinedTextField(
                    value = password, onValueChange = { password = it },
                    label = { Text("Password") },
                    leadingIcon = { Icon(Icons.Outlined.Lock, null) },
                    visualTransformation = PasswordVisualTransformation(),
                    keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Password),
                    modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(8.dp), singleLine = true
                )
                Spacer(Modifier.height(12.dp))

                if (isOtpSent) {
                    OutlinedTextField(
                        value = otp, onValueChange = { otp = it.take(6) },
                        label = { Text("6-Digit Code") },
                        leadingIcon = { Icon(Icons.Outlined.Lock, null) },
                        keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                        modifier = Modifier.fillMaxWidth(), shape = RoundedCornerShape(8.dp), singleLine = true
                    )
                    Spacer(Modifier.height(24.dp))
                }

                Button(
                    onClick = {
                        val trimmedName = name.trim()
                        val trimmedEmail = email.trim()
                        val trimmedPassword = password.trim()

                        if (trimmedName.isEmpty() || trimmedEmail.isEmpty() || trimmedPassword.isEmpty()) {
                            error = "All fields are required"
                            return@Button
                        }

                        if (trimmedPassword.length < 6) {
                            error = "Password must be at least 6 characters"
                            return@Button
                        }

                        scope.launch {
                            loading = true
                            error = null
                            successMessage = null
                            
                            if (!isOtpSent) {
                                try {
                                    RetrofitClient.api.requestOtp(OTPRequest(trimmedEmail))
                                    isOtpSent = true
                                    successMessage = "Code sent! Check your email."
                                } catch (e: Exception) {
                                    error = "Failed to send code: ${e.message}"
                                } finally {
                                    loading = false
                                }
                            } else {
                                if (otp.length < 6) {
                                    error = "Please enter the 6-digit code"
                                    loading = false
                                    return@launch
                                }
                                try {
                                    val response = RetrofitClient.api.verifyOtp(OTPVerifyRequest(trimmedEmail, otp, trimmedPassword, trimmedName))
                                    Log.i("SignupScreen", "Signup successful for $trimmedEmail")
                                    onSignupSuccess(response.accessToken)
                                } catch (e: retrofit2.HttpException) {
                                    error = if (e.code() == 400 || e.code() == 401) "Invalid or expired code." else "Signup failed: ${e.message()}"
                                } catch (e: java.io.IOException) {
                                    error = "Network error. Please check your connection."
                                } catch (e: Exception) {
                                    error = "Signup failed: ${e.localizedMessage}"
                                } finally {
                                    loading = false
                                }
                            }
                        }
                    },
                    enabled = !loading,
                    modifier = Modifier.fillMaxWidth().height(48.dp),
                    shape = RoundedCornerShape(8.dp),
                    colors = ButtonDefaults.buttonColors(containerColor = CivicFixBlue)
                ) {
                    if (loading) {
                        CircularProgressIndicator(Modifier.size(20.dp), Color.White, strokeWidth = 2.dp)
                        Spacer(Modifier.width(8.dp)); Text(if (isOtpSent) "Verifying..." else "Sending...")
                    } else {
                        Text(if (isOtpSent) "Verify & Create Account" else "Send Login Code", fontWeight = FontWeight.SemiBold)
                    }
                }

                Spacer(Modifier.height(16.dp))

                Text(
                    text = "OR",
                    color = Color(0xFF94A3B8),
                    fontSize = 12.sp,
                    fontWeight = FontWeight.Medium
                )

                Spacer(Modifier.height(16.dp))
                
                // Google Sign-In Button
                OutlinedButton(
                    onClick = {
                        loading = true
                        try {
                            val gso = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                                .requestIdToken(context.getString(R.string.default_web_client_id))
                                .requestEmail()
                                .build()
                            val googleSignInClient = GoogleSignIn.getClient(context, gso)
                            // Sign out first to always show account picker
                            googleSignInClient.signOut().addOnCompleteListener {
                                googleSignInLauncher.launch(googleSignInClient.signInIntent)
                            }
                        } catch (e: Exception) {
                            Log.e("SignupScreen", "Failed to launch Google Sign In", e)
                            error = "Failed to launch Google Sign-In."
                            loading = false
                        }
                    },
                    modifier = Modifier
                        .fillMaxWidth()
                        .height(48.dp),
                    shape = RoundedCornerShape(8.dp),
                    colors = ButtonDefaults.outlinedButtonColors(containerColor = Color.White),
                    border = BorderStroke(1.dp, Color(0xFFE2E8F0)),
                    enabled = !loading
                ) {
                    Icon(
                        painter = painterResource(id = R.drawable.ic_google_logo),
                        contentDescription = "Google Logo",
                        modifier = Modifier.size(24.dp),
                        tint = Color.Unspecified
                    )
                    Spacer(Modifier.width(12.dp))
                    Text(
                        "Sign in with Google",
                        fontWeight = FontWeight.Medium,
                        fontSize = 15.sp,
                        color = Color(0xFF334155)
                    )
                }

                Spacer(Modifier.height(16.dp))
                TextButton(onClick = onNavigateToLogin) {
                    Text("Already have an account? Sign in", color = CivicFixBlue, fontSize = 14.sp)
                }
            }
        }
    }
}
