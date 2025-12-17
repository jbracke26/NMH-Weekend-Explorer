import reflex as rx

from app.states.state import State
from app.layout import layout
from app.config import Config


_config = Config()
GOOGLE_CLIENT_ID = _config.GOOGLE_CLIENT_ID or ""
GOOGLE_MAPS_API_KEY = _config.GOOGLE_MAPS_API_KEY or ""


def index():
    return layout(
        rx.vstack(
            rx.box(
                rx.heading("My Activities", size="5", margin_bottom="3"),
                rx.cond(
                    State.is_authenticated,
                    rx.cond(
                        State.my_activities_list,
                        rx.hstack(
                            rx.foreach(
                                State.my_activities_list,
                                lambda activity: rx.link(
                                    rx.card(
                                        rx.vstack(
                                            rx.text(
                                                activity["title"],
                                                weight="bold",
                                                size="2",
                                            ),
                                            rx.text(activity["time"], size="1"),
                                            rx.badge(
                                                rx.cond(
                                                    activity["creator_id"]
                                                    == State.current_user_id,
                                                    "Created",
                                                    rx.cond(
                                                        activity.get("chaperone_id")
                                                        == State.current_user_id,
                                                        "Chaperoning",
                                                        "Joined",
                                                    ),
                                                ),
                                                color_scheme=rx.cond(
                                                    activity["creator_id"]
                                                    == State.current_user_id,
                                                    "green",
                                                    rx.cond(
                                                        activity.get("chaperone_id")
                                                        == State.current_user_id,
                                                        "purple",
                                                        "blue",
                                                    ),
                                                ),
                                                size="1",
                                            ),
                                            align_items="start",
                                            spacing="1",
                                        ),
                                        min_width="200px",
                                        height="100px",
                                        cursor="pointer",
                                        _hover={"box_shadow": "md"},
                                    ),
                                    href=f"/activity/{activity['id']}",
                                    text_decoration="none",
                                    color="inherit",
                                ),
                            ),
                            overflow_x="auto",
                            padding_bottom="4",
                            spacing="4",
                            width="100%",
                        ),
                        rx.text(
                            "No activities yet. Create one or join an upcoming activity!",
                            size="2",
                            color="gray",
                        ),
                    ),
                    rx.text(
                        "Please log in to see your activities.",
                        size="2",
                        color="gray",
                    ),
                ),
                width="100%",
                margin_bottom="6",
            ),
            rx.hstack(
                rx.box(
                    rx.cond(
                        GOOGLE_MAPS_API_KEY != "",
                        rx.fragment(
                            rx.script(
                                f"""
                                (function() {{
                                    // Map functions (inline) - same structure as map_page
                                    if (!window.homeMap) {{
                                        window.homeMap = null;
                                        window.homeMarkers = [];
                                        window.homeInfoWindows = [];
                                        
                                        window.initHomeMap = function() {{
                                            const mapContainer = document.getElementById('home_map');
                                            if (!mapContainer) return;
                                            
                                            // Check if google.maps is available
                                            if (!window.google || !window.google.maps) {{
                                                console.log('google.maps not available yet, retrying...');
                                                setTimeout(window.initHomeMap, 200);
                                                return;
                                            }}
                                            
                                            const defaultCenter = {{ lat: 42.5364, lng: -72.5278 }};
                                            
                                            window.homeMap = new window.google.maps.Map(mapContainer, {{
                                                zoom: 14,
                                                center: defaultCenter,
                                                mapTypeControl: true,
                                                streetViewControl: true,
                                                fullscreenControl: true,
                                            }});
                                            
                                            window.loadHomeMapActivities();
                                        }};
                                        
                                        window.loadHomeMapActivities = function() {{
                                            const activitiesData = window.homeActivitiesData || [];
                                            
                                            const isFirstLoad = !window.homeMapInitialized;
                                            
                                            const wasOpen = window.homeMap && window.homeMap.openInfoWindow && 
                                                window.homeMap.openInfoWindow.getMap() !== null;
                                            const openMarker = window.homeMap ? window.homeMap.openMarker : null;
                                            
                                            window.homeMarkers.forEach(marker => marker.setMap(null));
                                            window.homeInfoWindows.forEach(iw => iw.close());
                                            window.homeMarkers = [];
                                            window.homeInfoWindows = [];
                                            
                                            if (activitiesData.length === 0 || !window.homeMap) {{
                                                return;
                                            }}
                                            
                                            const geocoder = new window.google.maps.Geocoder();
                                            let geocodedCount = 0;
                                            
                                            activitiesData.forEach((activity, index) => {{
                                                // Priority: Use saved coordinates directly if available
                                                // This avoids unnecessary geocoding API calls
                                                // The location field is ignored when coordinates exist
                                                let position;
                                                if (activity.latitude && activity.longitude) {{
                                                    const lat = parseFloat(activity.latitude);
                                                    const lng = parseFloat(activity.longitude);
                                                    if (!isNaN(lat) && !isNaN(lng)) {{
                                                        position = {{ lat: lat, lng: lng }};
                                                        // Create marker directly with saved coordinates
                                                        const marker = new window.google.maps.Marker({{
                                                            position: position,
                                                            map: window.homeMap,
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
                                                        
                                                        marker.infoWindow = infoWindow;
                                                        marker.marker = marker;
                                                        
                                                        marker.addListener('click', () => {{
                                                            window.homeInfoWindows.forEach(iw => iw.close());
                                                            infoWindow.open(window.homeMap, marker);
                                                            window.homeMap.openInfoWindow = infoWindow;
                                                            window.homeMap.openMarker = marker;
                                                        }});
                                                        
                                                        window.homeMarkers.push(marker);
                                                        window.homeInfoWindows.push(infoWindow);
                                                        
                                                        geocodedCount++;
                                                        if (geocodedCount === activitiesData.length) {{
                                                            if (window.homeMarkers.length > 0) {{
                                                                // Only adjust map bounds on first load
                                                                if (isFirstLoad) {{
                                                                    const bounds = new window.google.maps.LatLngBounds();
                                                                    window.homeMarkers.forEach(m => bounds.extend(m.getPosition()));
                                                                    
                                                                    if (window.homeMarkers.length === 1) {{
                                                                        window.homeMap.setCenter(window.homeMarkers[0].getPosition());
                                                                        window.homeMap.setZoom(15);
                                                                    }} else {{
                                                                        window.homeMap.fitBounds(bounds);
                                                                    }}
                                                                    window.homeMapInitialized = true;
                                                                }}
                                                                
                                                                // If there was an open infoWindow before reload, try to reopen it
                                                                if (wasOpen && openMarker) {{
                                                                    // Find the marker that matches the previously open one
                                                                    const matchingMarker = window.homeMarkers.find(m => 
                                                                        m.getPosition().lat() === openMarker.getPosition().lat() &&
                                                                        m.getPosition().lng() === openMarker.getPosition().lng()
                                                                    );
                                                                    if (matchingMarker && matchingMarker.infoWindow) {{
                                                                        setTimeout(() => {{
                                                                            matchingMarker.infoWindow.open(window.homeMap, matchingMarker);
                                                                            window.homeMap.openInfoWindow = matchingMarker.infoWindow;
                                                                            window.homeMap.openMarker = matchingMarker;
                                                                        }}, 200);
                                                                    }}
                                                                }}
                                                            }}
                                                        }}
                                                        return;
                                                    }}
                                                }}
                                                
                                                // Fallback: Only use geocoding if no saved coordinates exist
                                                // If coordinates exist, we skip this entire block (early return above)
                                                const location = activity.location || '';
                                                if (!location) {{
                                                    // Skip if no location and no coordinates
                                                    geocodedCount++;
                                                    if (geocodedCount === activitiesData.length) {{
                                                        if (window.homeMarkers.length > 0) {{
                                                            const hasOpenInfoWindow = window.homeMap.openInfoWindow && 
                                                                window.homeMap.openInfoWindow.getMap() !== null;
                                                            
                                                            if (!hasOpenInfoWindow && !window.homeMapInitialized) {{
                                                                const bounds = new window.google.maps.LatLngBounds();
                                                                window.homeMarkers.forEach(m => bounds.extend(m.getPosition()));
                                                                if (window.homeMarkers.length === 1) {{
                                                                    window.homeMap.setCenter(window.homeMarkers[0].getPosition());
                                                                    window.homeMap.setZoom(15);
                                                                }} else {{
                                                                    window.homeMap.fitBounds(bounds);
                                                                }}
                                                                window.homeMapInitialized = true;
                                                            }}
                                                        }}
                                                    }}
                                                    return;
                                                }}
                                                
                                                geocoder.geocode({{ address: location + ', Northfield, MA' }}, (results, status) => {{
                                                    if (status === 'OK' && results[0]) {{
                                                        position = results[0].geometry.location;
                                                    }} else {{
                                                        position = {{ lat: 42.5364 + (index * 0.01), lng: -72.5278 + (index * 0.01) }};
                                                    }}
                                                    
                                                    const marker = new window.google.maps.Marker({{
                                                        position: position,
                                                        map: window.homeMap,
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
                                                        window.homeInfoWindows.forEach(iw => iw.close());
                                                        infoWindow.open(window.homeMap, marker);
                                                        // Store which infoWindow is currently open
                                                        window.homeMap.openInfoWindow = infoWindow;
                                                        window.homeMap.openMarker = marker;
                                                    }});
                                                    
                                                    window.homeMarkers.push(marker);
                                                    window.homeInfoWindows.push(infoWindow);
                                                    
                                                    geocodedCount++;
                                                    if (geocodedCount === activitiesData.length) {{
                                                        if (window.homeMarkers.length > 0) {{
                                                            // Only adjust map bounds on first load
                                                            if (isFirstLoad) {{
                                                                const bounds = new window.google.maps.LatLngBounds();
                                                                window.homeMarkers.forEach(m => bounds.extend(m.getPosition()));
                                                                
                                                                if (window.homeMarkers.length === 1) {{
                                                                    window.homeMap.setCenter(window.homeMarkers[0].getPosition());
                                                                    window.homeMap.setZoom(15);
                                                                }} else {{
                                                                    window.homeMap.fitBounds(bounds);
                                                                }}
                                                                window.homeMapInitialized = true;
                                                            }}
                                                            
                                                            // If there was an open infoWindow before reload, try to reopen it
                                                            if (wasOpen && openMarker) {{
                                                                // Find the marker that matches the previously open one
                                                                const matchingMarker = window.homeMarkers.find(m => 
                                                                    m.getPosition().lat() === openMarker.getPosition().lat() &&
                                                                    m.getPosition().lng() === openMarker.getPosition().lng()
                                                                );
                                                                if (matchingMarker && matchingMarker.infoWindow) {{
                                                                    setTimeout(() => {{
                                                                        matchingMarker.infoWindow.open(window.homeMap, matchingMarker);
                                                                        window.homeMap.openInfoWindow = matchingMarker.infoWindow;
                                                                        window.homeMap.openMarker = matchingMarker;
                                                                    }}, 200);
                                                                }}
                                                            }}
                                                        }}
                                                    }}
                                                }});
                                            }});
                                        }};
                                        
                                    }}
                                    
                                    function updateHomeActivitiesData() {{
                                        const activitiesInput = document.getElementById('home_activities_json_hidden');
                                        if (activitiesInput) {{
                                            try {{
                                                const newData = JSON.parse(activitiesInput.value || '[]');
                                                const currentData = window.homeActivitiesData || [];
                                                
                                                const dataChanged = JSON.stringify(newData) !== JSON.stringify(currentData);
                                                
                                                // Check if InfoWindow is open - if so, skip update completely
                                                const hasOpenInfoWindow = window.homeMap && window.homeMap.openInfoWindow && 
                                                    window.homeMap.openInfoWindow.getMap() !== null;
                                                
                                                if (hasOpenInfoWindow) {{
                                                    // InfoWindow is open, don't update to prevent instability
                                                    return;
                                                }}
                                                
                                                if (dataChanged && window.google && window.loadHomeMapActivities) {{
                                                    window.homeActivitiesData = newData;
                                                    window.loadHomeMapActivities();
                                                }} else if (dataChanged) {{
                                                    window.homeActivitiesData = newData;
                                                }}
                                            }} catch (e) {{
                                                console.error('Error parsing activities:', e);
                                                window.homeActivitiesData = [];
                                            }}
                                        }}
                                    }}
                                    
                                    function initializeHomeMap() {{
                                        const mapContainer = document.getElementById('home_map');
                                        if (!mapContainer) {{
                                            console.log('home_map container not found, retrying...');
                                            setTimeout(initializeHomeMap, 100);
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
                                                            if (window.initHomeMap) {{
                                                                window.initHomeMap();
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
                                            if (window.initHomeMap) {{
                                                setTimeout(function() {{
                                                    window.initHomeMap();
                                                }}, 100);
                                            }}
                                        }}
                                    }}
                                    
                                    // Wait for DOM to be ready
                                    if (document.readyState === 'loading') {{
                                        document.addEventListener('DOMContentLoaded', initializeHomeMap);
                                    }} else {{
                                        setTimeout(initializeHomeMap, 100);
                                    }}
                                    
                                    // Watch for changes in activities
                                    setInterval(updateHomeActivitiesData, 5000);
                                }})();
                                """
                            ),
                            rx.input(
                                id="home_activities_json_hidden",
                                type="hidden",
                                value=State.filtered_activities_json,
                                style={"display": "none"},
                            ),
                            rx.box(
                                id="home_map",
                                width="100%",
                                height="400px",
                                border_radius="12px",
                                border="1px solid var(--gray-6)",
                                background="var(--gray-2)",
                                display="block",
                            ),
                        ),
                        rx.center(
                            rx.vstack(
                                rx.icon("map", size=48, color="var(--gray-9)"),
                                rx.text("Map View", size="4", color="var(--gray-11)"),
                                rx.text(
                                    "Google Maps API Key not configured",
                                    size="2",
                                    color="var(--gray-10)",
                                ),
                                spacing="3",
                            ),
                            height="400px",
                        ),
                    ),
                    flex="2",
                ),
                rx.vstack(
                    rx.heading("Upcoming Activities", size="4", margin_bottom="3"),
                    rx.vstack(
                        rx.foreach(
                            State.upcoming_activities,
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
                                                activity["time"],
                                                size="2",
                                                color="var(--gray-11)",
                                            ),
                                            rx.text(
                                                f"{activity.get('participants_count', 0)} signed up",
                                                size="1",
                                                color="var(--gray-9)",
                                            ),
                                            rx.cond(
                                                activity.get("max_participants"),
                                                rx.text(
                                                    f"Limit: {activity['max_participants']}",
                                                    size="1",
                                                    color="var(--red-9)",
                                                ),
                                                None,
                                            ),
                                            spacing="2",
                                        ),
                                        rx.cond(
                                            activity["admin_signed_up"],
                                            rx.text(
                                                "Chaperone assigned",
                                                size="1",
                                                color="var(--green-9)",
                                            ),
                                            rx.cond(
                                                activity.get("needs_chaperone", False),
                                                rx.text(
                                                    "Needs chaperone",
                                                    size="1",
                                                    color="var(--red-9)",
                                                ),
                                                rx.fragment(),
                                            ),
                                        ),
                                        rx.text(
                                            f"Location: {activity['location']}",
                                            size="1",
                                            color="var(--gray-8)",
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
                                    width="100%",
                                ),
                                href=f"/activity/{activity['id']}",
                                text_decoration="none",
                                color="inherit",
                            ),
                        ),
                        spacing="2",
                        width="100%",
                    ),
                    rx.link(
                        rx.button(
                            "Create Activity",
                            size="3",
                            width="100%",
                            margin_top="4",
                        ),
                        href="/create",
                        width="100%",
                    ),
                    flex="1",
                ),
                spacing="4",
                width="100%",
            ),
            width="100%",
            spacing="0",
        ),
        on_mount=State.on_page_load,
    )
