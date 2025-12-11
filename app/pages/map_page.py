import reflex as rx
import json
from app.states.state import State
from app.layout import layout
from app.config import Config


_config = Config()
GOOGLE_MAPS_API_KEY = _config.GOOGLE_MAPS_API_KEY or ""


def map_page():
    """Map page showing activities on a map and in a list."""
    return layout(
        rx.vstack(
            rx.heading("Activity Map", size="7", margin_bottom="5"),
            # Map and List Container
            rx.hstack(
                # Google Maps (Left 2/3)
                rx.box(
                    rx.cond(
                        GOOGLE_MAPS_API_KEY != "",
                        rx.fragment(
                            rx.script(
                                f"""
                                (function() {{
                                    // Map functions (inline)
                                    if (!window.map) {{
                                        window.map = null;
                                        window.markers = [];
                                        window.infoWindows = [];
                                        
                                        window.initMap = function() {{
                                            const mapContainer = document.getElementById('map');
                                            if (!mapContainer) return;
                                            
                                            // Check if google.maps is available
                                            if (!window.google || !window.google.maps) {{
                                                console.log('google.maps not available yet, retrying...');
                                                setTimeout(window.initMap, 200);
                                                return;
                                            }}
                                            
                                            const defaultCenter = {{ lat: 42.5364, lng: -72.5278 }};
                                            
                                            window.map = new window.google.maps.Map(mapContainer, {{
                                                zoom: 14,
                                                center: defaultCenter,
                                                mapTypeControl: true,
                                                streetViewControl: true,
                                                fullscreenControl: true,
                                            }});
                                            
                                            window.loadActivities();
                                        }};
                                        
                                        window.loadActivities = function() {{
                                            const activitiesData = window.activitiesData || [];
                                            
                                            // Check if this is the first load
                                            const isFirstLoad = !window.mapInitialized;
                                            
                                            // Store currently open infoWindow before clearing
                                            const wasOpen = window.map && window.map.openInfoWindow && 
                                                window.map.openInfoWindow.getMap() !== null;
                                            const openMarker = window.map ? window.map.openMarker : null;
                                            
                                            // Clear existing markers
                                            window.markers.forEach(marker => marker.setMap(null));
                                            window.infoWindows.forEach(iw => iw.close());
                                            window.markers = [];
                                            window.infoWindows = [];
                                            
                                            if (activitiesData.length === 0 || !window.map) {{
                                                return;
                                            }}
                                            
                                            const geocoder = new window.google.maps.Geocoder();
                                            let geocodedCount = 0;
                                            
                                            activitiesData.forEach((activity, index) => {{
                                                const location = activity.location || '';
                                                if (!location) return;
                                                
                                                geocoder.geocode({{ address: location + ', Northfield, MA' }}, (results, status) => {{
                                                    let position;
                                                    if (status === 'OK' && results[0]) {{
                                                        position = results[0].geometry.location;
                                                    }} else {{
                                                        position = {{ lat: 42.5364 + (index * 0.01), lng: -72.5278 + (index * 0.01) }};
                                                    }}
                                                    
                                                    const marker = new window.google.maps.Marker({{
                                                        position: position,
                                                        map: window.map,
                                                        title: activity.title,
                                                        icon: {{
                                                            url: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                                                            scaledSize: new window.google.maps.Size(32, 32)
                                                        }}
                                                    }});
                                                    
                                                    const infoWindow = new window.google.maps.InfoWindow({{
                                                        content: `
                                                            <div style="padding: 8px; min-width: 200px;">
                                                                <h3 style="margin: 0 0 8px 0; font-size: 16px; font-weight: bold;">${{activity.title}}</h3>
                                                                <p style="margin: 4px 0; color: #666; font-size: 12px;"><strong>Category:</strong> ${{activity.category || 'Other'}}</p>
                                                                <p style="margin: 4px 0; color: #666; font-size: 12px;"><strong>Location:</strong> ${{activity.location || 'N/A'}}</p>
                                                                <p style="margin: 4px 0; color: #666; font-size: 12px;"><strong>Time:</strong> ${{activity.time || 'N/A'}}</p>
                                                                <a href="/activity/${{activity.id}}" style="display: inline-block; margin-top: 8px; padding: 6px 12px; background: #007bff; color: white; text-decoration: none; border-radius: 4px; font-size: 12px;">View Details</a>
                                                            </div>
                                                        `
                                                    }});
                                                    
                                                    // Store reference to marker and infoWindow
                                                    marker.infoWindow = infoWindow;
                                                    marker.marker = marker;
                                                    
                                                    marker.addListener('click', () => {{
                                                        window.infoWindows.forEach(iw => iw.close());
                                                        infoWindow.open(window.map, marker);
                                                        // Store which infoWindow is currently open
                                                        window.map.openInfoWindow = infoWindow;
                                                        window.map.openMarker = marker;
                                                    }});
                                                    
                                                    window.markers.push(marker);
                                                    window.infoWindows.push(infoWindow);
                                                    
                                                    geocodedCount++;
                                                    if (geocodedCount === activitiesData.length) {{
                                                        if (window.markers.length > 0) {{
                                                            // Only adjust map bounds on first load
                                                            if (isFirstLoad) {{
                                                                const bounds = new window.google.maps.LatLngBounds();
                                                                window.markers.forEach(m => bounds.extend(m.getPosition()));
                                                                
                                                                if (window.markers.length === 1) {{
                                                                    window.map.setCenter(window.markers[0].getPosition());
                                                                    window.map.setZoom(15);
                                                                }} else {{
                                                                    window.map.fitBounds(bounds);
                                                                }}
                                                                window.mapInitialized = true;
                                                            }}
                                                            
                                                            // If there was an open infoWindow before reload, try to reopen it
                                                            if (wasOpen && openMarker) {{
                                                                // Find the marker that matches the previously open one
                                                                const matchingMarker = window.markers.find(m => 
                                                                    m.getPosition().lat() === openMarker.getPosition().lat() &&
                                                                    m.getPosition().lng() === openMarker.getPosition().lng()
                                                                );
                                                                if (matchingMarker && matchingMarker.infoWindow) {{
                                                                    setTimeout(() => {{
                                                                        matchingMarker.infoWindow.open(window.map, matchingMarker);
                                                                        window.map.openInfoWindow = matchingMarker.infoWindow;
                                                                        window.map.openMarker = matchingMarker;
                                                                    }}, 200);
                                                                }}
                                                            }}
                                                        }}
                                                    }}
                                                }});
                                            }});
                                        }};
                                    }}
                                    
                                    function updateActivitiesData() {{
                                        const activitiesInput = document.getElementById('activities_json_hidden');
                                        if (activitiesInput) {{
                                            try {{
                                                const newData = JSON.parse(activitiesInput.value || '[]');
                                                const currentData = window.activitiesData || [];
                                                
                                                // Check if data actually changed
                                                const dataChanged = JSON.stringify(newData) !== JSON.stringify(currentData);
                                                
                                                // Don't reload if infoWindow is open or data hasn't changed
                                                const hasOpenInfoWindow = window.map && window.map.openInfoWindow && 
                                                    window.map.openInfoWindow.getMap() !== null;
                                                
                                                if (dataChanged && !hasOpenInfoWindow && window.google && window.loadActivities) {{
                                                    window.activitiesData = newData;
                                                    window.loadActivities();
                                                }} else if (dataChanged && !hasOpenInfoWindow) {{
                                                    window.activitiesData = newData;
                                                }}
                                            }} catch (e) {{
                                                console.error('Error parsing activities:', e);
                                                window.activitiesData = [];
                                            }}
                                        }}
                                    }}
                                    
                                    function initializeMap() {{
                                        const mapContainer = document.getElementById('map');
                                        if (!mapContainer) {{
                                            console.log('Map container not found, retrying...');
                                            setTimeout(initializeMap, 100);
                                            return;
                                        }}
                                        
                                        if (!window.google || !window.google.maps) {{
                                            console.log('Google Maps API not loaded yet, loading...');
                                            const gmapsScript = document.createElement('script');
                                            gmapsScript.src = 'https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&loading=async';
                                            gmapsScript.async = true;
                                            gmapsScript.defer = true;
                                            gmapsScript.onload = function() {{
                                                console.log('Google Maps API script loaded, waiting for maps object...');
                                                // Wait for google.maps to be fully initialized
                                                function waitForMaps() {{
                                                    if (window.google && window.google.maps && window.google.maps.Map) {{
                                                        console.log('Google Maps API fully loaded');
                                                        setTimeout(function() {{
                                                            if (window.initMap) {{
                                                                window.initMap();
                                                            }}
                                                        }}, 100);
                                                    }} else {{
                                                        console.log('Waiting for google.maps...');
                                                        setTimeout(waitForMaps, 100);
                                                    }}
                                                }}
                                                waitForMaps();
                                            }};
                                            gmapsScript.onerror = function() {{
                                                console.error('Failed to load Google Maps API. Check your API key in .env file.');
                                            }};
                                            document.head.appendChild(gmapsScript);
                                        }} else {{
                                            console.log('Google Maps API already loaded');
                                            if (window.initMap) {{
                                                setTimeout(function() {{
                                                    window.initMap();
                                                }}, 100);
                                            }}
                                        }}
                                    }}
                                    
                                    // Wait for DOM to be ready
                                    if (document.readyState === 'loading') {{
                                        document.addEventListener('DOMContentLoaded', initializeMap);
                                    }} else {{
                                        setTimeout(initializeMap, 100);
                                    }}
                                    
                                    // Watch for changes in activities
                                    setInterval(updateActivitiesData, 1000);
                                }})();
                                """
                            ),
                            rx.input(
                                id="activities_json_hidden",
                                type="hidden",
                                value=State.filtered_activities_json,
                            ),
                            rx.box(
                                id="map",
                                width="100%",
                                height="500px",
                                border_radius="12px",
                                border="1px solid var(--gray-6)",
                                background="var(--gray-2)",
                            ),
                        ),
                        rx.center(
                            rx.vstack(
                                rx.icon("map-pin", size=48, color="var(--gray-9)"),
                                rx.text(
                                    "Google Maps API Key not configured",
                                    size="4",
                                    color="var(--gray-11)",
                                ),
                                rx.text(
                                    "Please set GOOGLE_MAPS_API_KEY in your .env file",
                                    size="2",
                                    color="var(--gray-10)",
                                ),
                                spacing="3",
                            ),
                            height="500px",
                        ),
                    ),
                    flex="2",
                ),
                # Activities List (Right 1/3)
                rx.vstack(
                    rx.heading("All Activities", size="4", margin_bottom="3"),
                    rx.box(
                        rx.vstack(
                            rx.foreach(
                                State.filtered_activities,
                                lambda activity: rx.link(
                                    rx.box(
                                        rx.vstack(
                                            rx.text(
                                                activity["title"],
                                                weight="bold",
                                                size="3",
                                            ),
                                            rx.hstack(
                                                rx.badge(
                                                    activity["category"],
                                                    size="1",
                                                    variant="soft",
                                                ),
                                                rx.text(
                                                    activity["location"],
                                                    size="2",
                                                    color="var(--gray-11)",
                                                ),
                                                spacing="2",
                                            ),
                                            rx.text(
                                                activity["time"],
                                                size="2",
                                                color="var(--gray-10)",
                                            ),
                                            align_items="start",
                                            spacing="2",
                                        ),
                                        padding="3",
                                        border_radius="8px",
                                        border="1px solid var(--gray-6)",
                                        background="var(--color-background)",
                                        _hover={
                                            "background": "var(--gray-3)",
                                            "border_color": "var(--gray-7)",
                                        },
                                        transition="all 0.2s ease",
                                        width="calc(100%)",  
                                        margin="5px",  
                                    ),
                                    href=f"/activity/{activity['id']}",
                                    text_decoration="none",
                                    color="inherit",
                                ),
                            ),
                            spacing="2",
                            width="100%",
                        ),
                        height="500px",
                        overflow_y="auto",
                        width="100%",
                    ),
                    flex="1",
                ),
                spacing="4",
                width="100%",
                align_items="start",
            ),
            width="100%",
            spacing="5",
        ),
        on_mount=State.load_activities,
    )
