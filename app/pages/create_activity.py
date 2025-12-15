import reflex as rx
from app.states.state import State
from app.layout import layout
from app.config import Config
from reflex_google_auth import google_login, google_oauth_provider

_config = Config()
GOOGLE_CLIENT_ID = _config.GOOGLE_CLIENT_ID or ""
GOOGLE_MAPS_API_KEY = _config.GOOGLE_MAPS_API_KEY or ""


def create_activity() -> rx.Component:
    return layout(
        rx.box(
            rx.cond(
                GOOGLE_MAPS_API_KEY != "",
                rx.script(
                    f"""
                    (function() {{
                        console.log('=== Create Activity Map Script Loaded (Always) ===');
                        
                        if (!window.createActivityMapFunctions) {{
                            window.createActivityMap = null;
                            window.createActivityMarker = null;
                            
                            window.initCreateActivityMap = function() {{
                                console.log('initCreateActivityMap called');
                                const mapContainer = document.getElementById('create_activity_map');
                                if (!mapContainer) {{
                                    console.log('create_activity_map container not found, retrying...');
                                    setTimeout(window.initCreateActivityMap, 200);
                                    return;
                                }}
                                console.log('create_activity_map container found, size:', mapContainer.offsetWidth, 'x', mapContainer.offsetHeight);
                                
                                if (window.createActivityMap) {{
                                    console.log('Create activity map already initialized');
                                    const mapDiv = window.createActivityMap.getDiv();
                                    if (mapDiv && mapDiv === mapContainer) {{
                                        console.log('Map is already attached to container');
                                        return;
                                    }}
                                    console.log('Map exists but not attached, reinitializing...');
                                    window.createActivityMap = null;
                                    if (window.createActivityMarker) {{
                                        window.createActivityMarker.setMap(null);
                                        window.createActivityMarker = null;
                                    }}
                                }}
                                
                                console.log('Initializing create activity map...');
                                
                                if (!window.google || !window.google.maps || !window.google.maps.Map) {{
                                    console.log('Google Maps API not available, loading...');
                                    
                                    // Check if script is already being loaded
                                    if (document.querySelector('script[src*="maps.googleapis.com"]')) {{
                                        console.log('Google Maps API script already exists, waiting...');
                                        setTimeout(window.initCreateActivityMap, 500);
                                        return;
                                    }}
                                    
                                    const script = document.createElement('script');
                                    script.src = 'https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&loading=async&callback=initCreateActivityMapCallback';
                                    script.async = true;
                                    script.defer = true;
                                    
                                    // Set up global callback
                                    window.initCreateActivityMapCallback = function() {{
                                        console.log('Google Maps API callback fired for create activity');
                                        setTimeout(function() {{
                                            if (window.google && window.google.maps && window.google.maps.Map) {{
                                                console.log('Google Maps API fully loaded via callback');
                                                if (window.initCreateActivityMap) {{
                                                    window.initCreateActivityMap();
                                                }}
                                            }} else {{
                                                console.log('Maps object still not available, retrying...');
                                                setTimeout(window.initCreateActivityMap, 200);
                                            }}
                                        }}, 100);
                                    }};
                                    
                                    script.onload = function() {{
                                        console.log('Google Maps API script loaded for create activity');
                                    }};
                                    
                                    script.onerror = function() {{
                                        console.error('Failed to load Google Maps API for create activity');
                                        delete window.initCreateActivityMapCallback;
                                    }};
                                    
                                    document.head.appendChild(script);
                                    return;
                                }}
                                
                                try {{
                                    if (mapContainer.style.display === 'none') {{
                                        mapContainer.style.display = 'block';
                                    }}
                                    
                                    const checkSize = function() {{
                                        const width = mapContainer.offsetWidth || mapContainer.clientWidth;
                                        const height = mapContainer.offsetHeight || mapContainer.clientHeight;
                                        
                                        if (width === 0 || height === 0) {{
                                            console.log('Map container has no size yet, waiting...', width, 'x', height);
                                            setTimeout(checkSize, 100);
                                            return;
                                        }}
                                        
                                        console.log('Initializing map with container size:', width, 'x', height);
                                        
                                        if (!mapContainer.style.width && width < 100) {{
                                            mapContainer.style.width = '100%';
                                        }}
                                        if (!mapContainer.style.height && height < 100) {{
                                            mapContainer.style.height = '400px';
                                        }}
                                        
                                        window.createActivityMap = new window.google.maps.Map(mapContainer, {{
                                            zoom: 14,
                                            center: {{ lat: 42.5364, lng: -72.5278 }},
                                            mapTypeControl: true,
                                            streetViewControl: true,
                                            fullscreenControl: true,
                                        }});
                                        
                                        console.log('Create activity map initialized successfully');
                                        
                                        setTimeout(function() {{
                                            if (window.google && window.google.maps && window.google.maps.event && window.createActivityMap) {{
                                                window.google.maps.event.trigger(window.createActivityMap, 'resize');
                                            }}
                                        }}, 100);
                                        
                                        window.createActivityMap.addListener('click', function(event) {{
                                            const lat = event.latLng.lat();
                                            const lng = event.latLng.lng();
                                            
                                            console.log('Map clicked at:', lat, lng);
                                            
                                            if (window.createActivityMarker) {{
                                                window.createActivityMarker.setPosition(event.latLng);
                                            }} else {{
                                                window.createActivityMarker = new window.google.maps.Marker({{
                                                    position: event.latLng,
                                                    map: window.createActivityMap,
                                                    draggable: true,
                                                    title: 'Activity Location'
                                                }});
                                                
                                                window.createActivityMarker.addListener('dragend', function(event) {{
                                                    const lat = event.latLng.lat();
                                                    const lng = event.latLng.lng();
                                                    console.log('Marker dragged to:', lat, lng);
                                                    updateLocationFromMap(lat, lng);
                                                }});
                                            }}
                                            
                                            updateLocationFromMap(lat, lng);
                                            
                                            const geocoder = new window.google.maps.Geocoder();
                                            geocoder.geocode({{ location: event.latLng }}, function(results, status) {{
                                                if (status === 'OK' && results[0]) {{
                                                    // Try to find the location input by its placeholder or other attributes
                                                    const locationInputs = document.querySelectorAll('input[placeholder*="Alumni Hall"], input[placeholder*="e.g.,"]');
                                                    if (locationInputs.length > 0) {{
                                                        const addressInput = locationInputs[0];
                                                        addressInput.value = results[0].formatted_address;
                                                        const inputEvent = new Event('input', {{ bubbles: true }});
                                                        addressInput.dispatchEvent(inputEvent);
                                                    }}
                                                }}
                                            }});
                                        }});
                                    }};
                                    
                                    checkSize();
                                }} catch (error) {{
                                    console.error('Error initializing create activity map:', error);
                                    setTimeout(window.initCreateActivityMap, 500);
                                }}
                            }};
                            
                            function updateLocationFromMap(lat, lng) {{
                                console.log('updateLocationFromMap called with:', lat, lng);
                                const latStr = lat.toString();
                                const lngStr = lng.toString();
                                
                                // Store coordinates in a way that Reflex can access
                                // Use window object to store values temporarily
                                window._tempLatitude = latStr;
                                window._tempLongitude = lngStr;
                                
                                // Try to update hidden inputs
                                const latInput = document.getElementById('activity_latitude_hidden');
                                const lngInput = document.getElementById('activity_longitude_hidden');
                                
                                if (latInput && lngInput) {{
                                    // Set value using setAttribute for hidden inputs
                                    latInput.setAttribute('value', latStr);
                                    lngInput.setAttribute('value', lngStr);
                                    latInput.value = latStr;
                                    lngInput.value = lngStr;
                                    
                                    console.log('Setting hidden inputs:', latInput.value, lngInput.value);
                                    
                                    // Create and dispatch change events with proper React/Reflex compatibility
                                    const createSyntheticEvent = function(input, value, eventType) {{
                                        const event = new Event(eventType, {{ 
                                            bubbles: true, 
                                            cancelable: true,
                                            composed: true
                                        }});
                                        
                                        // Set properties that React/Reflex expects
                                        Object.defineProperty(event, 'target', {{ 
                                            value: input, 
                                            enumerable: true,
                                            configurable: true,
                                            writable: false
                                        }});
                                        
                                        Object.defineProperty(event, 'currentTarget', {{ 
                                            value: input, 
                                            enumerable: true,
                                            configurable: true,
                                            writable: false
                                        }});
                                        
                                        // Set the value property on the target
                                        Object.defineProperty(input, 'value', {{
                                            value: value,
                                            writable: true,
                                            configurable: true,
                                            enumerable: true
                                        }});
                                        
                                        return event;
                                    }};
                                    
                                    // Dispatch both input and change events
                                    const latChangeEvent = createSyntheticEvent(latInput, latStr, 'change');
                                    const lngChangeEvent = createSyntheticEvent(lngInput, lngStr, 'change');
                                    const latInputEvent = createSyntheticEvent(latInput, latStr, 'input');
                                    const lngInputEvent = createSyntheticEvent(lngInput, lngStr, 'input');
                                    
                                    // Dispatch events in sequence
                                    latInput.dispatchEvent(latInputEvent);
                                    latInput.dispatchEvent(latChangeEvent);
                                    lngInput.dispatchEvent(lngInputEvent);
                                    lngInput.dispatchEvent(lngChangeEvent);
                                    
                                    console.log('Events dispatched, final values:', latInput.value, lngInput.value);
                                    
                                    // Additional verification after a short delay
                                    setTimeout(function() {{
                                        console.log('Verification - latInput.value:', latInput.value, 'lngInput.value:', lngInput.value);
                                        console.log('Window temp values - lat:', window._tempLatitude, 'lng:', window._tempLongitude);
                                    }}, 200);
                                }} else {{
                                    console.error('Hidden inputs not found! Storing in window object only.');
                                }}
                            }}
                            
                            window.cleanupCreateActivityMap = function() {{
                                if (window.createActivityMarker) {{
                                    window.createActivityMarker.setMap(null);
                                    window.createActivityMarker = null;
                                }}
                                if (window.createActivityMap) {{
                                    if (window.google && window.google.maps && window.google.maps.event) {{
                                        window.google.maps.event.clearInstanceListeners(window.createActivityMap);
                                    }}
                                    window.createActivityMap = null;
                                }}
                                console.log('Create activity map cleaned up');
                            }};
                            
                            function checkAndInitMap() {{
                                const mapContainer = document.getElementById('create_activity_map');
                                if (mapContainer) {{
                                    // Force display block if container exists
                                    const computedStyle = window.getComputedStyle(mapContainer);
                                    if (computedStyle.display === 'none' || mapContainer.style.display === 'none') {{
                                        mapContainer.style.display = 'block';
                                        console.log('Forced display block on map container');
                                    }}
                                    
                                    // Wait a bit for display to take effect, then check visibility
                                    setTimeout(function() {{
                                        const isVisible = mapContainer.offsetParent !== null && 
                                                         mapContainer.style.display !== 'none' &&
                                                         window.getComputedStyle(mapContainer).display !== 'none' &&
                                                         window.getComputedStyle(mapContainer).visibility !== 'hidden' &&
                                                         mapContainer.offsetWidth > 0 &&
                                                         mapContainer.offsetHeight > 0;
                                        
                                        console.log('checkAndInitMap - container found, visible:', isVisible, 'size:', mapContainer.offsetWidth, 'x', mapContainer.offsetHeight);
                                        
                                        if (isVisible) {{
                                            if (!window.createActivityMap) {{
                                                console.log('Map not initialized, calling initCreateActivityMap...');
                                                window.initCreateActivityMap();
                                            }} else {{
                                                try {{
                                                    const mapDiv = window.createActivityMap.getDiv();
                                                    if (!mapDiv || mapDiv !== mapContainer) {{
                                                        console.log('Map exists but not attached to container, reinitializing...');
                                                        window.cleanupCreateActivityMap();
                                                        setTimeout(function() {{
                                                            window.initCreateActivityMap();
                                                        }}, 100);
                                                    }} else {{
                                                        setTimeout(function() {{
                                                            if (window.google && window.google.maps && window.google.maps.event && window.createActivityMap) {{
                                                                window.google.maps.event.trigger(window.createActivityMap, 'resize');
                                                            }}
                                                        }}, 100);
                                                    }}
                                                }} catch (e) {{
                                                    console.error('Error checking map attachment:', e);
                                                    window.cleanupCreateActivityMap();
                                                    setTimeout(function() {{
                                                        window.initCreateActivityMap();
                                                    }}, 100);
                                                }}
                                            }}
                                        }} else {{
                                            if (window.createActivityMap) {{
                                                console.log('Container not visible, cleaning up map...');
                                                window.cleanupCreateActivityMap();
                                            }}
                                        }}
                                    }}, 50);
                                }} else {{
                                    if (window.createActivityMap) {{
                                        console.log('Container not found, cleaning up map...');
                                        window.cleanupCreateActivityMap();
                                    }}
                                }}
                            }}
                            
                            const observer = new MutationObserver(function(mutations) {{
                                const mapContainer = document.getElementById('create_activity_map');
                                if (mapContainer) {{
                                    console.log('MutationObserver detected change, checking map...');
                                    checkAndInitMap();
                                }}
                            }});
                            
                            observer.observe(document.body, {{
                                childList: true,
                                subtree: true,
                                attributes: true,
                                attributeFilter: ['style', 'class', 'display', 'id']
                            }});
                            
                            console.log('=== Starting create activity map initialization ===');
                            
                            // Initial check
                            setTimeout(function() {{
                                checkAndInitMap();
                            }}, 100);
                            
                            let checkCount = 0;
                            const checkInterval = setInterval(function() {{
                                checkCount++;
                                const mapContainer = document.getElementById('create_activity_map');
                                if (mapContainer) {{
                                    // Force display block
                                    const computedStyle = window.getComputedStyle(mapContainer);
                                    if (computedStyle.display === 'none' || mapContainer.style.display === 'none') {{
                                        mapContainer.style.display = 'block';
                                    }}
                                    
                                    // Check if container is visible and has size
                                    const isVisible = mapContainer.offsetParent !== null && 
                                                     mapContainer.offsetWidth > 0 && 
                                                     mapContainer.offsetHeight > 0;
                                    
                                    if (isVisible) {{
                                        checkAndInitMap();
                                        if (window.createActivityMap && checkCount > 5) {{
                                            clearInterval(checkInterval);
                                            console.log('Map initialized, stopping frequent checks');
                                        }}
                                    }} else if (checkCount % 10 === 0) {{
                                        console.log('Map container exists but not visible yet, check:', checkCount, 'size:', mapContainer.offsetWidth, 'x', mapContainer.offsetHeight);
                                    }}
                                }} else if (checkCount % 20 === 0) {{
                                    console.log('Map container not found yet, check:', checkCount);
                                }}
                                if (checkCount > 200) {{
                                    clearInterval(checkInterval);
                                    console.log('Stopped checking after', checkCount, 'attempts');
                                }}
                            }}, 300);
                            
                            if (document.readyState === 'loading') {{
                                document.addEventListener('DOMContentLoaded', function() {{
                                    setTimeout(checkAndInitMap, 500);
                                }});
                            }} else {{
                                setTimeout(checkAndInitMap, 500);
                            }}
                            
                            window.createActivityMapFunctions = true;
                        }}
                    }})();
                    """
                ),
            ),
            rx.cond(
                State.is_authenticated,
                rx.fragment(
                    rx.center(
                        rx.card(
                            rx.vstack(
                                rx.heading("Create New Activity", size="6", margin_bottom="4"),
                                rx.vstack(
                                rx.text(
                                    "Title", weight="bold", size="2", margin_bottom="1"
                                ),
                                rx.input(
                                    placeholder="e.g., Northampton Dinner Trip",
                                    value=State.activity_title,
                                    on_change=State.set_activity_title,
                                    width="100%",
                                ),
                                width="100%",
                                align_items="start",
                            ),
                        rx.vstack(
                            rx.text(
                                "Description",
                                weight="bold",
                                size="2",
                                margin_bottom="1",
                            ),
                            rx.text_area(
                                placeholder="Describe what you'll be doing...",
                                value=State.activity_description,
                                on_change=State.set_activity_description,
                                min_height="120px",
                                width="100%",
                            ),
                            width="100%",
                            align_items="start",
                        ),
                        rx.hstack(
                            rx.vstack(
                                rx.text(
                                    "Category",
                                    weight="bold",
                                    size="2",
                                    margin_bottom="1",
                                ),
                                rx.select(
                                    ["Outdoor", "Food", "Shopping", "Sports", "Other"],
                                    placeholder="Select Category",
                                    value=State.activity_category,
                                    on_change=State.set_activity_category,
                                    width="100%",
                                ),
                                width="100%",
                                align_items="start",
                            ),
                            rx.vstack(
                                rx.text(
                                    "Max Participants",
                                    weight="bold",
                                    size="2",
                                    margin_bottom="1",
                                ),
                                rx.input(
                                    placeholder="Optional",
                                    value=State.activity_max_participants,
                                    on_change=State.set_activity_max_participants,
                                    width="100%",
                                ),
                                width="100%",
                                align_items="start",
                            ),
                            width="100%",
                            spacing="4",
                        ),
                        rx.vstack(
                            rx.text(
                                "Location", weight="bold", size="2", margin_bottom="1"
                            ),
                            rx.input(
                                placeholder="e.g., Alumni Hall",
                                value=State.activity_location,
                                on_change=State.set_activity_location,
                                width="100%",
                            ),
                            width="100%",
                            align_items="start",
                        ),
                        rx.vstack(
                            rx.text(
                                "Log Location on Map?",
                                weight="bold",
                                size="2",
                                margin_bottom="1",
                            ),
                            rx.switch(
                                is_checked=State.activity_log_location,
                                on_change=State.set_activity_log_location,
                            ),
                            rx.cond(
                                State.use_map_for_location,
                                rx.fragment(
                                    rx.cond(
                                        GOOGLE_MAPS_API_KEY != "",
                                        rx.fragment(
                                            rx.input(
                                                id="activity_latitude_hidden",
                                                type="hidden",
                                                value=State.activity_latitude,
                                                on_change=State.set_activity_latitude,
                                            ),
                                            rx.input(
                                                id="activity_longitude_hidden",
                                                type="hidden",
                                                value=State.activity_longitude,
                                                on_change=State.set_activity_longitude,
                                            ),
                                            rx.box(
                                                id="create_activity_map",
                                                width="100%",
                                                height="400px",
                                                border_radius="8px",
                                                border="1px solid var(--gray-6)",
                                                margin_top="2",
                                                display="block",
                                            ),
                                            rx.text(
                                                "Click on the map to set the location. You can also drag the marker to adjust.",
                                                size="1",
                                                color="var(--gray-10)",
                                                margin_top="2",
                                            ),
                                        ),
                                        rx.center(
                                            rx.vstack(
                                                rx.icon("map", size=48, color="var(--gray-9)"),
                                                rx.text(
                                                    "Google Maps API Key not configured",
                                                    size="3",
                                                    color="var(--gray-11)",
                                                ),
                                                spacing="2",
                                            ),
                                            height="400px",
                                        ),
                                    ),
                                ),
                            ),
                            align_items="center",
                            width="100%",
                        ),
                        rx.cond(
                            State.activity_log_location,
                            rx.hstack(
                                rx.vstack(
                                    rx.text(
                                        "Latitude",
                                        weight="bold",
                                        size="2",
                                        margin_bottom="1",
                                    ),
                                    rx.input(
                                        placeholder="e.g., 42.667144",
                                        value=State.activity_latitude,
                                        on_change=State.set_activity_latitude,
                                        width="100%",
                                    ),
                                    width="100%",
                                    align_items="start",
                                ),
                                rx.vstack(
                                    rx.text(
                                        "Longitude",
                                        weight="bold",
                                        size="2",
                                        margin_bottom="1",
                                    ),
                                    rx.input(
                                        placeholder="e.g., -72.481655",
                                        value=State.activity_longitude,
                                        on_change=State.set_activity_longitude,
                                        width="100%",
                                    ),
                                    width="100%",
                                    align_items="start",
                                ),
                                spacing="4",
                                width="100%",
                            ),
                        ),
                        rx.vstack(
                            rx.text(
                                "Distance", weight="bold", size="2", margin_bottom="1"
                            ),
                            rx.input(
                                placeholder="e.g., 15 min walk",
                                value=State.activity_distance,
                                on_change=State.set_activity_distance,
                                width="100%",
                            ),
                            width="100%",
                            align_items="start",
                        ),
                        rx.hstack(
                            rx.vstack(
                                rx.text(
                                    "Date", weight="bold", size="2", margin_bottom="1"
                                ),
                                rx.input(
                                    type_="date",
                                    placeholder="YYYY-MM-DD",
                                    value=State.activity_date,
                                    on_change=State.set_activity_date,
                                    width="100%",
                                ),
                                width="100%",
                                align_items="start",
                            ),
                            rx.vstack(
                                rx.text(
                                    "Time", weight="bold", size="2", margin_bottom="1"
                                ),
                                rx.input(
                                    type_="time",
                                    placeholder="HH:MM",
                                    value=State.activity_time,
                                    on_change=State.set_activity_time,
                                    width="100%",
                                ),
                                width="100%",
                                align_items="start",
                            ),
                            spacing="4",
                            width="100%",
                        ),
                        rx.button(
                            "Create Activity",
                            on_click=State.create_activity,
                            size="3",
                            width="100%",
                            color_scheme="teal",
                            margin_top="6",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    width="100%",
                    max_width="600px",
                    padding="6",
                    box_shadow="lg",
                        ),
                        padding_y="8",
                        width="100%",
                    ),
                ),
                # Login Prompt if not authenticated
                rx.center(
                    rx.vstack(
                    rx.heading("Please Login", size="6"),
                    rx.text("You need to be logged in to create an activity."),
                    rx.cond(
                        GOOGLE_CLIENT_ID != "",
                        google_oauth_provider(
                            google_login(
                                on_success=State.on_google_login_success,
                            ),
                            client_id=GOOGLE_CLIENT_ID,
                        ),
                        rx.text("Google OAuth not configured.", color="red"),
                    ),
                        spacing="4",
                        align="center",
                    ),
                    padding="10",
                    width="100%",
                ),
            ),
        ),
        on_mount=State.clear_activity_form,
    )
