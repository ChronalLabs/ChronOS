package com.civicfix.app.ui.screens

import android.Manifest
import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.location.Geocoder
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.Check
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import com.civicfix.app.ui.theme.CivicFixTheme
import com.google.android.gms.location.LocationServices
import com.google.android.gms.location.Priority
import com.google.android.gms.maps.model.CameraPosition
import com.google.android.gms.maps.model.LatLng
import com.google.maps.android.compose.*
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.util.Locale

class LocationPickerActivity : ComponentActivity() {

    private var onPermissionGranted: (() -> Unit)? = null
    private var onPermissionDenied: (() -> Unit)? = null

    private val locationPermissionRequest = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { permissions ->
        if (permissions.values.any { it }) {
            onPermissionGranted?.invoke()
        } else {
            onPermissionDenied?.invoke()
        }
    }

    @OptIn(ExperimentalMaterial3Api::class)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        setContent {
            CivicFixTheme {
                var selectedLatLng by remember { mutableStateOf<LatLng?>(null) }
                var selectedAddress by remember { mutableStateOf("Tap on the map to select a location") }
                val coroutineScope = rememberCoroutineScope()
                var cameraPositionState by remember { mutableStateOf<CameraPositionState?>(null) }
                var hasLocationPermission by remember {
                    mutableStateOf(
                        ContextCompat.checkSelfPermission(
                            this@LocationPickerActivity,
                            Manifest.permission.ACCESS_FINE_LOCATION
                        ) == PackageManager.PERMISSION_GRANTED
                    )
                }

                // Update permission state dynamically when camera state is set (after permission request)
                LaunchedEffect(cameraPositionState) {
                    hasLocationPermission = ContextCompat.checkSelfPermission(
                        this@LocationPickerActivity,
                        Manifest.permission.ACCESS_FINE_LOCATION
                    ) == PackageManager.PERMISSION_GRANTED
                }

                // Get initial position from intent or user's current location
                LaunchedEffect(Unit) {
                    val lat = intent.getDoubleExtra("LATITUDE", 0.0)
                    val lon = intent.getDoubleExtra("LONGITUDE", 0.0)

                    if (lat != 0.0 && lon != 0.0) {
                        // Use passed-in coordinates
                        val latLng = LatLng(lat, lon)
                        selectedLatLng = latLng
                        cameraPositionState = CameraPositionState(CameraPosition.fromLatLngZoom(latLng, 15f))
                        coroutineScope.launch(Dispatchers.IO) {
                            val addr = getAddress(lat, lon)
                            withContext(Dispatchers.Main) {
                                selectedAddress = addr
                            }
                        }
                    } else {
                        // Try to get user's current location
                        fetchCurrentLocation { userLat, userLon ->
                            val latLng = LatLng(userLat, userLon)
                            selectedLatLng = latLng
                            cameraPositionState = CameraPositionState(
                                CameraPosition.fromLatLngZoom(latLng, 15f)
                            )
                            coroutineScope.launch(Dispatchers.IO) {
                                val addr = getAddress(userLat, userLon)
                                withContext(Dispatchers.Main) {
                                    selectedAddress = addr
                                }
                            }
                        }
                    }
                }

                Scaffold(
                    topBar = {
                        TopAppBar(
                            title = { Text("Select Location", fontWeight = FontWeight.Bold) },
                            navigationIcon = {
                                IconButton(onClick = { finish() }) {
                                    Icon(Icons.Filled.ArrowBack, contentDescription = "Back")
                                }
                            },
                            colors = TopAppBarDefaults.topAppBarColors(
                                containerColor = Color.White,
                                titleContentColor = Color(0xFF1A202C)
                            )
                        )
                    },
                    bottomBar = {
                        Column(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(16.dp),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            Text(
                                text = selectedAddress,
                                fontSize = 14.sp,
                                modifier = Modifier.padding(bottom = 16.dp)
                            )
                            Button(
                                onClick = {
                                    selectedLatLng?.let {
                                        val data = Intent().apply {
                                            putExtra("LATITUDE", it.latitude)
                                            putExtra("LONGITUDE", it.longitude)
                                            putExtra("ADDRESS", selectedAddress)
                                        }
                                        setResult(Activity.RESULT_OK, data)
                                        finish()
                                    }
                                },
                                enabled = selectedLatLng != null,
                                modifier = Modifier.fillMaxWidth().height(48.dp),
                                shape = androidx.compose.foundation.shape.RoundedCornerShape(8.dp)
                            ) {
                                Icon(Icons.Filled.Check, contentDescription = null)
                                Spacer(modifier = Modifier.width(8.dp))
                                Text("Confirm Location")
                            }
                        }
                    }
                ) { innerPadding ->
                    Box(modifier = Modifier.fillMaxSize().padding(innerPadding)) {
                        if (cameraPositionState != null) {
                            GoogleMap(
                                modifier = Modifier.fillMaxSize(),
                                cameraPositionState = cameraPositionState!!,
                                properties = MapProperties(
                                    isMyLocationEnabled = hasLocationPermission
                                ),
                                onMapClick = { latLng ->
                                    selectedLatLng = latLng
                                    coroutineScope.launch(Dispatchers.IO) {
                                        val addr = getAddress(latLng.latitude, latLng.longitude)
                                        withContext(Dispatchers.Main) {
                                            selectedAddress = addr
                                        }
                                    }
                                },
                                onPOIClick = { poi ->
                                    selectedLatLng = poi.latLng
                                    coroutineScope.launch(Dispatchers.IO) {
                                        val addr = getAddress(poi.latLng.latitude, poi.latLng.longitude)
                                        withContext(Dispatchers.Main) {
                                            selectedAddress = poi.name + " - " + addr
                                        }
                                    }
                                }
                            ) {
                                selectedLatLng?.let {
                                    Marker(
                                        state = MarkerState(position = it),
                                        title = "Selected Location",
                                        snippet = selectedAddress
                                    )
                                }
                            }
                        } else {
                            // Loading state while getting location
                            Column(
                                modifier = Modifier.fillMaxSize(),
                                horizontalAlignment = Alignment.CenterHorizontally,
                                verticalArrangement = Arrangement.Center
                            ) {
                                CircularProgressIndicator()
                                Spacer(Modifier.height(16.dp))
                                Text("Getting your location...")
                            }
                        }
                    }
                }
            }
        }
    }

    @Suppress("MissingPermission")
    private fun fetchCurrentLocation(onResult: (Double, Double) -> Unit) {
        val hasPermission = ContextCompat.checkSelfPermission(
            this, Manifest.permission.ACCESS_FINE_LOCATION
        ) == PackageManager.PERMISSION_GRANTED

        if (!hasPermission) {
            // Request permission, then retry
            onPermissionGranted = { fetchCurrentLocation(onResult) }
            onPermissionDenied = {
                android.widget.Toast.makeText(
                    this,
                    "Location permission denied. Map opened at default location.",
                    android.widget.Toast.LENGTH_LONG
                ).show()
                // Default to a central India location as fallback
                onResult(20.5937, 78.9629)
            }
            locationPermissionRequest.launch(
                arrayOf(
                    Manifest.permission.ACCESS_FINE_LOCATION,
                    Manifest.permission.ACCESS_COARSE_LOCATION
                )
            )
            return
        }

        val fusedClient = LocationServices.getFusedLocationProviderClient(this)

        // Try lastLocation first (fast)
        fusedClient.lastLocation.addOnSuccessListener { location ->
            if (location != null) {
                onResult(location.latitude, location.longitude)
            } else {
                // Request a fresh location fix
                fusedClient.getCurrentLocation(Priority.PRIORITY_HIGH_ACCURACY, null)
                    .addOnSuccessListener { freshLocation ->
                        if (freshLocation != null) {
                            onResult(freshLocation.latitude, freshLocation.longitude)
                        } else {
                            // Default to a central India location as fallback
                            // (user is in India based on timezone IST +05:30)
                            onResult(20.5937, 78.9629)
                        }
                    }
                    .addOnFailureListener {
                        onResult(20.5937, 78.9629)
                    }
            }
        }.addOnFailureListener {
            onResult(20.5937, 78.9629)
        }
    }

    private fun getAddress(lat: Double, lon: Double): String {
        return try {
            val geocoder = Geocoder(this, Locale.getDefault())
            val addresses = geocoder.getFromLocation(lat, lon, 1)
            if (!addresses.isNullOrEmpty()) {
                val address = addresses[0]
                val maxLine = address.maxAddressLineIndex
                if (maxLine >= 0) {
                    address.getAddressLine(0)
                } else {
                    "${address.locality ?: ""}, ${address.adminArea ?: ""}".trim(',', ' ')
                }
            } else {
                "Lat: ${lat.format(4)}, Lon: ${lon.format(4)}"
            }
        } catch (e: Exception) {
            "Lat: ${lat.format(4)}, Lon: ${lon.format(4)}"
        }
    }

    private fun Double.format(digits: Int) = "%.${digits}f".format(this)
}
