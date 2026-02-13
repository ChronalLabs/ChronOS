/// <reference types="google.maps" />
import { useEffect, useRef, useState, useCallback } from "react"
import { Loader } from "@googlemaps/js-api-loader"
import { ZoomIn, ZoomOut, AlertTriangle } from "lucide-react"

declare global {
  interface Window {
    google?: typeof google
  }
}

/* ---------------- TYPES ---------------- */

export interface MapZone {
  id: string
  name: string
  type: "construction" | "traffic" | "residential" | "commercial" | "industrial"
  center: { lat: number; lng: number }
  radius: number
  impact: "low" | "medium" | "high"
  description?: string
}

export interface GoogleMapProps {
  zones?: MapZone[]
  center?: { lat: number; lng: number }
  zoom?: number
  height?: string
  simulationActive?: boolean
  impactLevel?: "low" | "medium" | "high"
}

/* ---------------- LOADER SINGLETON ---------------- */
let loaderInstance: Loader | null = null

const getLoader = (apiKey: string) => {
  if (!loaderInstance) {
    loaderInstance = new Loader({
      apiKey,
      version: 'weekly',
      libraries: ['visualization'],
    })
  }
  return loaderInstance
}

/* ---------------- COMPONENT ---------------- */

const GoogleMapComponent: React.FC<GoogleMapProps> = ({
  zones = [],
  center = { lat: 28.6139, lng: 77.209 },
  zoom = 13,
  height = "500px",
  simulationActive = false,
  impactLevel = "medium",
}) => {
  const mapDivRef = useRef<HTMLDivElement | null>(null)
  const mapRef = useRef<google.maps.Map | null>(null)
  const heatmapRef = useRef<google.maps.visualization.HeatmapLayer | null>(null)

  const [mapZoom, setMapZoom] = useState(zoom)
  const [mapError, setMapError] = useState<string | null>(null)
  const [mapLoaded, setMapLoaded] = useState(false)

  /* ---------------- MAP INIT ---------------- */

  useEffect(() => {
    let mounted = true

    const apiKey = import.meta.env.VITE_GOOGLE_MAPS_KEY
    if (!apiKey) {
      setMapError('Missing Google Maps API key. Add VITE_GOOGLE_MAPS_KEY to .env')
      return
    }

    const loader = getLoader(apiKey)

    loader
      .load()
      .then((google) => {
        if (!mounted || !mapDivRef.current) return
        mapRef.current = new google.maps.Map(mapDivRef.current, {
          center,
          zoom,
          mapTypeId: 'roadmap',
          disableDefaultUI: true,
        })
        setMapLoaded(true)
        setMapError(null)
      })
      .catch((err) => {
        console.error('Google Maps failed to load', err)
        setMapError('Google Maps failed to load. Check API key & billing.')
      })

    return () => {
      mounted = false
    }
  }, [])

  /* ---------------- HEATMAP ---------------- */

  useEffect(() => {
    if (!mapRef.current || !mapLoaded || !window.google) return

    const heatmapData = zones.map((z) => ({
      location: new google.maps.LatLng(z.center.lat, z.center.lng),
      weight:
        z.impact === "high" ? 3 : z.impact === "medium" ? 2 : 1,
    }))

    if (!heatmapRef.current) {
      heatmapRef.current = new google.maps.visualization.HeatmapLayer({
        data: heatmapData,
        map: mapRef.current,
        radius: 35,
        opacity: 0.7,
      })
    } else {
      heatmapRef.current.setData(heatmapData)
    }
  }, [zones, mapLoaded])

  /* ---------------- ZOOM CONTROLS ---------------- */

  const zoomIn = useCallback(() => {
    if (!mapRef.current) return
    const newZoom = Math.min(mapZoom + 1, 20)
    mapRef.current.setZoom(newZoom)
    setMapZoom(newZoom)
  }, [mapZoom])

  const zoomOut = useCallback(() => {
    if (!mapRef.current) return
    const newZoom = Math.max(mapZoom - 1, 5)
    mapRef.current.setZoom(newZoom)
    setMapZoom(newZoom)
  }, [mapZoom])

  /* ---------------- UI ---------------- */

  return (
    <div
      style={{
        position: "relative",
        width: "100%",
        height,
        borderRadius: "20px",
        overflow: "hidden",
      }}
    >
      {/* MAP */}
      <div
        ref={mapDivRef}
        style={{ width: "100%", height: "100%" }}
      />

      {mapError && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            background: "rgba(15,23,42,0.7)",
            color: "white",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            padding: "1rem",
            textAlign: "center",
          }}
        >
          {mapError}
        </div>
      )}

      {/* SIMULATION OVERLAY */}
      {simulationActive && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            background:
              impactLevel === "high"
                ? "rgba(239,68,68,0.15)"
                : impactLevel === "medium"
                ? "rgba(245,158,11,0.15)"
                : "rgba(16,185,129,0.15)",
            pointerEvents: "none",
          }}
        />
      )}

      {/* ZOOM CONTROLS */}
      <div
        style={{
          position: "absolute",
          top: "1rem",
          right: "1rem",
          background: "white",
          borderRadius: "12px",
          padding: "0.25rem",
          boxShadow: "0 4px 20px rgba(0,0,0,0.15)",
        }}
      >
        <button onClick={zoomIn}><ZoomIn /></button>
        <button onClick={zoomOut}><ZoomOut /></button>
      </div>

      {/* SIMULATION BADGE */}
      {simulationActive && (
        <div
          style={{
            position: "absolute",
            top: "1rem",
            left: "50%",
            transform: "translateX(-50%)",
            background: "#ef4444",
            color: "white",
            padding: "0.5rem 1rem",
            borderRadius: "999px",
            fontWeight: 700,
            display: "flex",
            alignItems: "center",
            gap: "0.5rem",
          }}
        >
          <AlertTriangle size={14} />
          SIMULATION ACTIVE
        </div>
      )}
    </div>
  )
}

export default GoogleMapComponent