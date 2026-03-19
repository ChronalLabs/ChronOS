package com.civicfix.app.data.models

import com.google.gson.annotations.SerializedName

// --- Auth ---
data class LoginRequest(
    val email: String,
    val password: String
)

data class SignupRequest(
    val email: String,
    val password: String,
    @SerializedName("display_name") val displayName: String? = null
)

data class FirebaseLoginRequest(
    @SerializedName("firebase_token") val firebaseToken: String
)

data class OTPRequest(
    val email: String
)

data class OTPVerifyRequest(
    val email: String,
    val code: String,
    val password: String,
    @SerializedName("display_name") val displayName: String? = null
)

data class OTPRequestResponse(
    val message: String,
    @SerializedName("expires_in") val expiresIn: Int
)

data class TokenResponse(
    @SerializedName("access_token") val accessToken: String,
    @SerializedName("token_type") val tokenType: String,
    @SerializedName("user_id") val userId: String,
    @SerializedName("display_name") val displayName: String?,
    val role: String
)

data class UserResponse(
    val id: String,
    val email: String,
    @SerializedName("display_name") val displayName: String?,
    val role: String
)

// --- Reports ---
data class ReportCreateResponse(
    @SerializedName("report_id") val reportId: String,
    @SerializedName("complaint_text") val complaintText: String,
    @SerializedName("image_url") val imageUrl: String?,
    val address: String?
)

data class ReportResponse(
    val id: String,
    @SerializedName("user_id") val userId: String?,
    @SerializedName("issue_type") val issueType: String,
    val description: String,
    val latitude: Double,
    val longitude: Double,
    val address: String?,
    @SerializedName("image_url") val imageUrl: String?,
    @SerializedName("thumbnail_url") val thumbnailUrl: String?,
    val status: String,
    @SerializedName("complaint_text") val complaintText: String?,
    @SerializedName("posted_to_x") val postedToX: Boolean,
    @SerializedName("created_at") val createdAt: String,
    @SerializedName("updated_at") val updatedAt: String
)

data class ReportListResponse(
    val reports: List<ReportResponse>,
    val total: Int,
    val page: Int,
    @SerializedName("page_size") val pageSize: Int
)

// --- Settings ---
data class SettingsResponse(
    @SerializedName("x_auto_post_enabled") val xAutoPostEnabled: Boolean,
    @SerializedName("x_api_connected") val xApiConnected: Boolean,
    @SerializedName("x_bearer_configured") val xBearerConfigured: Boolean
)

data class SettingsUpdateRequest(
    @SerializedName("x_auto_post_enabled") val xAutoPostEnabled: Boolean
)

// --- Health ---
data class HealthResponse(
    val status: String,
    val version: String,
    @SerializedName("mock_mode") val mockMode: Boolean
)

// --- Issue Types ---
enum class IssueType(val displayName: String) {
    POTHOLE("Pothole"),
    GARBAGE("Garbage"),
    BROKEN_STREETLIGHT("Broken streetlight"),
    WATER_LEAKAGE("Water leakage"),
    OTHER("Other");

    companion object {
        fun all() = values().toList()
    }
}
