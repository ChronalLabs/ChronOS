package com.civicfix.app.data.api

import com.civicfix.app.data.models.*
import okhttp3.MultipartBody
import okhttp3.RequestBody
import retrofit2.http.*

interface CivicFixApi {

    // --- Auth ---
    @POST("api/v1/auth/login")
    suspend fun login(@Body request: LoginRequest): TokenResponse

    @POST("api/v1/auth/signup")
    suspend fun signup(@Body request: SignupRequest): TokenResponse

    @POST("api/v1/auth/firebase-login")
    suspend fun firebaseLogin(@Body request: FirebaseLoginRequest): TokenResponse

    @POST("api/v1/auth/request-otp")
    suspend fun requestOtp(@Body request: OTPRequest): OTPRequestResponse

    @POST("api/v1/auth/verify-otp")
    suspend fun verifyOtp(@Body request: OTPVerifyRequest): TokenResponse

    @GET("api/v1/auth/me")
    suspend fun getMe(@Header("Authorization") token: String): UserResponse

    // --- Reports ---
    @Multipart
    @POST("api/v1/report")
    suspend fun createReport(
        @Header("Authorization") token: String,
        @Part image: MultipartBody.Part,
        @Part("issue_type") issueType: RequestBody,
        @Part("description") description: RequestBody,
        @Part("latitude") latitude: RequestBody,
        @Part("longitude") longitude: RequestBody,
        @Part("timestamp") timestamp: RequestBody? = null,
        @Part("device_id") deviceId: RequestBody? = null,
    ): ReportCreateResponse

    @GET("api/v1/reports")
    suspend fun getReports(
        @Header("Authorization") token: String,
        @Query("page") page: Int = 1,
        @Query("page_size") pageSize: Int = 20,
    ): ReportListResponse

    @GET("api/v1/reports/{id}")
    suspend fun getReport(
        @Header("Authorization") token: String,
        @Path("id") id: String,
    ): ReportResponse

    // --- Settings ---
    @GET("api/v1/settings")
    suspend fun getSettings(
        @Header("Authorization") token: String
    ): SettingsResponse

    @PUT("api/v1/settings")
    suspend fun updateSettings(
        @Header("Authorization") token: String,
        @Body request: SettingsUpdateRequest
    ): SettingsResponse

    // --- Health ---
    @GET("api/v1/health")
    suspend fun health(): HealthResponse
}
