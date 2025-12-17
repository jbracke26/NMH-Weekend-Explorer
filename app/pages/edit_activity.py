import reflex as rx
from app.states.state import State
from app.layout import layout
from app.config import Config

_config = Config()
GOOGLE_MAPS_API_KEY = _config.GOOGLE_MAPS_API_KEY or ""


def edit_activity() -> rx.Component:
    return layout(
        rx.box(
            rx.cond(
                GOOGLE_MAPS_API_KEY != "",
                rx.script(
                    f"""
                    (function() {{
                        console.log('=== Edit Activity Map Script Loaded ===');
                        
                        // Ensure Google Maps API is loaded with callback
                        function ensureGoogleMapsApi(callback) {{
                            // Check if already loaded
                            if (window.google && window.google.maps && window.google.maps.Map) {{
                                console.log('Google Maps API already available');
                                if (callback) callback();
                                return;
                            }}
                            
                            // Check if script is already being loaded
                            const existingScript = document.querySelector('script[src*="maps.googleapis.com"]');
                            if (existingScript) {{
                                console.log('Google Maps API script already exists, waiting...');
                                // Wait for API to be ready
                                const checkApi = setInterval(function() {{
                                    if (window.google && window.google.maps && window.google.maps.Map) {{
                                        clearInterval(checkApi);
                                        console.log('Google Maps API ready');
                                        if (callback) callback();
                                    }}
                                }}, 100);
                                
                                // Timeout after 10 seconds
                                setTimeout(function() {{
                                    clearInterval(checkApi);
                                    if (!window.google || !window.google.maps || !window.google.maps.Map) {{
                                        console.error('Google Maps API failed to load within timeout');
                                    }}
                                }}, 10000);
                                return;
                            }}
                            
                            // Create callback function
                            window._editActivityMapApiCallback = function() {{
                                console.log('Google Maps API loaded via callback');
                                window.googleMapsApiLoaded = true;
                                delete window._editActivityMapApiCallback;
                                if (callback) {{
                                    // Small delay to ensure everything is ready
                                    setTimeout(callback, 100);
                                }}
                            }};
                            
                            // Load the script
                            const script = document.createElement('script');
                            script.src = 'https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&loading=async&callback=_editActivityMapApiCallback';
                            script.async = true;
                            script.defer = true;
                            script.onerror = function() {{
                                console.error('Failed to load Google Maps API');
                                delete window._editActivityMapApiCallback;
                            }};
                            document.head.appendChild(script);
                            console.log('Loading Google Maps API...');
                        }}
                        
                        if (!window.editActivityMapFunctions) {{
                            window.editActivityMap = null;
                            window.editActivityMarker = null;
                            window.editActivityMapInitialized = false;
                            
                            window.initEditActivityMap = function() {{
                                const mapContainer = document.getElementById('edit_activity_map');
                                if (!mapContainer) {{
                                    console.log('Map container not found');
                                    return;
                                }}
                                
                                // Check if container is visible
                                const isVisible = mapContainer.offsetParent !== null && 
                                                 mapContainer.offsetWidth > 0 && 
                                                 mapContainer.offsetHeight > 0;
                                
                                if (!isVisible) {{
                                    console.log('Map container not visible yet');
                                    setTimeout(window.initEditActivityMap, 200);
                                    return;
                                }}
                                
                                // Check if already initialized
                                if (window.editActivityMap && window.editActivityMapInitialized) {{
                                    console.log('Map already initialized');
                                    return;
                                }}
                                
                                // Ensure Google Maps API is loaded
                                if (!window.google || !window.google.maps || !window.google.maps.Map) {{
                                    console.log('Google Maps API not ready, loading...');
                                    ensureGoogleMapsApi(function() {{
                                        setTimeout(window.initEditActivityMap, 100);
                                    }});
                                    return;
                                }}
                                
                                try {{
                                    console.log('Initializing edit activity map...');
                                    
                                    // Get current coordinates from text boxes
                                    const latInput = document.getElementById('edit_activity_latitude_hidden');
                                    const lngInput = document.getElementById('edit_activity_longitude_hidden');
                                    
                                    let center = {{ lat: 42.5364, lng: -72.5278 }};
                                    if (latInput && lngInput && latInput.value && lngInput.value) {{
                                        try {{
                                            center = {{
                                                lat: parseFloat(latInput.value),
                                                lng: parseFloat(lngInput.value)
                                            }};
                                            console.log('Using existing coordinates for center:', center);
                                        }} catch (e) {{
                                            console.log('Invalid coordinates, using default center');
                                        }}
                                    }}
                                    
                                    // Initialize map
                                    window.editActivityMap = new window.google.maps.Map(mapContainer, {{
                                        zoom: 14,
                                        center: center,
                                        mapTypeControl: true,
                                        streetViewControl: true,
                                        fullscreenControl: true,
                                    }});
                                    
                                    // If coordinates exist, add marker
                                    if (latInput && lngInput && latInput.value && lngInput.value) {{
                                        try {{
                                            const lat = parseFloat(latInput.value);
                                            const lng = parseFloat(lngInput.value);
                                            window.editActivityMarker = new window.google.maps.Marker({{
                                                position: {{ lat: lat, lng: lng }},
                                                map: window.editActivityMap,
                                                draggable: true,
                                                title: 'Activity Location'
                                            }});
                                            
                                            window.editActivityMarker.addListener('dragend', function(event) {{
                                                const lat = event.latLng.lat();
                                                const lng = event.latLng.lng();
                                                updateLocationFromMap(lat, lng);
                                            }});
                                            
                                            console.log('Marker added at existing coordinates');
                                        }} catch (e) {{
                                            console.log('Error adding marker:', e);
                                        }}
                                    }}
                                    
                                    // Trigger resize after a short delay
                                    setTimeout(function() {{
                                        if (window.google && window.google.maps && window.google.maps.event && window.editActivityMap) {{
                                            window.google.maps.event.trigger(window.editActivityMap, 'resize');
                                        }}
                                    }}, 200);
                                    
                                    // Add click listener
                                    window.editActivityMap.addListener('click', function(event) {{
                                        const lat = event.latLng.lat();
                                        const lng = event.latLng.lng();
                                        
                                        if (window.editActivityMarker) {{
                                            window.editActivityMarker.setPosition(event.latLng);
                                        }} else {{
                                            window.editActivityMarker = new window.google.maps.Marker({{
                                                position: event.latLng,
                                                map: window.editActivityMap,
                                                draggable: true,
                                                title: 'Activity Location'
                                            }});
                                            
                                            window.editActivityMarker.addListener('dragend', function(event) {{
                                                const lat = event.latLng.lat();
                                                const lng = event.latLng.lng();
                                                updateLocationFromMap(lat, lng);
                                            }});
                                        }}
                                        
                                        updateLocationFromMap(lat, lng);
                                        
                                        const geocoder = new window.google.maps.Geocoder();
                                        geocoder.geocode({{ location: event.latLng }}, function(results, status) {{
                                            if (status === 'OK' && results[0]) {{
                                                const addressInput = document.querySelector('#edit_activity_location_input');
                                                if (addressInput) {{
                                                    addressInput.value = results[0].formatted_address;
                                                    addressInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                                }}
                                            }}
                                        }});
                                    }});
                                    
                                    window.editActivityMapInitialized = true;
                                    console.log('Edit activity map initialized successfully');
                                }} catch (error) {{
                                    console.error('Error initializing edit activity map:', error);
                                    setTimeout(function() {{
                                        window.initEditActivityMap();
                                    }}, 500);
                                }}
                            }};
                            
                            // SIMPLE APPROACH: Just set the text box values directly
                            function updateLocationFromMap(lat, lng) {{
                                console.log('=== Edit: updateLocationFromMap - called with:', lat, lng);
                                const latStr = lat.toString();
                                const lngStr = lng.toString();
                                
                                // Find text box inputs
                                const latInput = document.getElementById('edit_activity_latitude_hidden');
                                const lngInput = document.getElementById('edit_activity_longitude_hidden');
                                
                                if (latInput && lngInput) {{
                                    // Simply set the values
                                    latInput.value = latStr;
                                    lngInput.value = lngStr;
                                    
                                    // Trigger input event (Reflex listens to this)
                                    latInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                    lngInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                    
                                    // Trigger change event
                                    latInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                    lngInput.dispatchEvent(new Event('change', {{ bubbles: true }}));
                                    
                                    console.log('=== Coordinates set in text boxes:', latInput.value, lngInput.value, '===');
                                }} else {{
                                    console.warn('Text box inputs not found');
                                }}
                                
                                // Store in localStorage as backup
                                try {{
                                    localStorage.setItem('edit_activity_latitude', latStr);
                                    localStorage.setItem('edit_activity_longitude', lngStr);
                                }} catch (e) {{
                                    console.error('Failed to save to localStorage:', e);
                                }}
                            }}
                            
                            window.cleanupEditActivityMap = function() {{
                                if (window.editActivityMarker) {{
                                    window.editActivityMarker.setMap(null);
                                    window.editActivityMarker = null;
                                }}
                                if (window.editActivityMap) {{
                                    if (window.google && window.google.maps && window.google.maps.event) {{
                                        window.google.maps.event.clearInstanceListeners(window.editActivityMap);
                                    }}
                                    window.editActivityMap = null;
                                }}
                                window.editActivityMapInitialized = false;
                                
                                // Clear localStorage when map is cleaned up
                                try {{
                                    localStorage.removeItem('edit_activity_latitude');
                                    localStorage.removeItem('edit_activity_longitude');
                                    console.log('=== Cleared coordinates from localStorage ===');
                                }} catch (e) {{
                                    console.error('Failed to clear localStorage:', e);
                                }}
                            }};
                            
                            // SIMPLE APPROACH: Just poll for map container and initialize when visible
                            function checkAndInitMap() {{
                                const mapContainer = document.getElementById('edit_activity_map');
                                if (mapContainer) {{
                                    const isVisible = mapContainer.offsetParent !== null && 
                                                     mapContainer.offsetWidth > 0 && 
                                                     mapContainer.offsetHeight > 0;
                                    
                                    if (isVisible && !window.editActivityMapInitialized) {{
                                        console.log('Edit map container visible, initializing...');
                                        window.initEditActivityMap();
                                    }}
                                }}
                            }}
                            
                            // Check periodically
                            setInterval(checkAndInitMap, 500);
                            
                            // Also check when DOM is ready
                            if (document.readyState === 'loading') {{
                                document.addEventListener('DOMContentLoaded', function() {{
                                    setTimeout(checkAndInitMap, 200);
                                }});
                            }} else {{
                                setTimeout(checkAndInitMap, 200);
                            }}
                            
                            // IMPROVED: Ensure text boxes have values and wait for Reflex state update
                            function setupUpdateButtonInterceptor() {{
                                const updateButton = document.getElementById('update_activity_button');
                                if (updateButton) {{
                                    updateButton.addEventListener('click', function(e) {{
                                        console.log('=== Update Activity button clicked - syncing coordinates ===');
                                        
                                        // Get coordinates from localStorage (backup)
                                        let latStr = '';
                                        let lngStr = '';
                                        
                                        try {{
                                            latStr = localStorage.getItem('edit_activity_latitude') || '';
                                            lngStr = localStorage.getItem('edit_activity_longitude') || '';
                                            console.log('Coordinates from localStorage:', latStr, lngStr);
                                        }} catch (e) {{
                                            console.error('Failed to read from localStorage:', e);
                                        }}
                                        
                                        // Get text box inputs
                                        const latInput = document.getElementById('edit_activity_latitude_hidden');
                                        const lngInput = document.getElementById('edit_activity_longitude_hidden');
                                        
                                        // If we have coordinates in localStorage, always sync them to text boxes
                                        if (latStr && lngStr && latInput && lngInput) {{
                                            console.log('Syncing coordinates from localStorage to text boxes...');
                                            
                                            // Set values
                                            latInput.value = latStr;
                                            lngInput.value = lngStr;
                                            
                                            // Set attribute as well
                                            latInput.setAttribute('value', latStr);
                                            lngInput.setAttribute('value', lngStr);
                                            
                                            // Trigger multiple events to ensure Reflex picks it up
                                            ['input', 'change', 'blur'].forEach(function(eventType) {{
                                                const event1 = new Event(eventType, {{ bubbles: true, cancelable: true, composed: true }});
                                                Object.defineProperty(event1, 'target', {{ value: latInput, enumerable: true }});
                                                latInput.dispatchEvent(event1);
                                                
                                                const event2 = new Event(eventType, {{ bubbles: true, cancelable: true, composed: true }});
                                                Object.defineProperty(event2, 'target', {{ value: lngInput, enumerable: true }});
                                                lngInput.dispatchEvent(event2);
                                            }});
                                            
                                            console.log('Coordinates synced - latInput.value:', latInput.value, 'lngInput.value:', lngInput.value);
                                            
                                            // Wait a bit for Reflex state to update before allowing click to proceed
                                            e.preventDefault();
                                            e.stopPropagation();
                                            
                                            setTimeout(function() {{
                                                console.log('Re-triggering button click after coordinate sync');
                                                // Create and dispatch a new click event
                                                const newClickEvent = new MouseEvent('click', {{
                                                    bubbles: true,
                                                    cancelable: true,
                                                    view: window
                                                }});
                                                updateButton.dispatchEvent(newClickEvent);
                                            }}, 500); // Wait 500ms for Reflex state to update
                                            
                                            return;
                                        }} else {{
                                            console.log('No coordinates in localStorage or text boxes not found');
                                        }}
                                        
                                        // If no coordinates or text boxes not found, proceed normally
                                        console.log('Proceeding with button click');
                                    }}, true); // Use capture phase
                                }} else {{
                                    // Retry if button not found yet
                                    setTimeout(setupUpdateButtonInterceptor, 500);
                                }}
                            }}
                            
                            // Setup interceptor when DOM is ready
                            if (document.readyState === 'loading') {{
                                document.addEventListener('DOMContentLoaded', setupUpdateButtonInterceptor);
                            }} else {{
                                setupUpdateButtonInterceptor();
                            }}
                            
                            window.editActivityMapFunctions = true;
                        }}
                    }})();
                    """
                ),
            ),
            rx.cond(
                State.is_authenticated,
                rx.center(
                    rx.card(
                        rx.vstack(
                            rx.heading("Edit Activity", size="6", margin_bottom="4"),
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
                                    id="edit_activity_location_input",
                                    placeholder="e.g., Alumni Hall",
                                    value=State.activity_location,
                                    on_change=State.set_activity_location,
                                    width="100%",
                                ),
                                width="100%",
                                align_items="start",
                            ),
                            rx.vstack(
                                rx.text("Set Location on Map", weight="bold", size="2", margin_bottom="1"),
                                rx.hstack(
                                    rx.text("Use interactive map?", weight="bold", size="2"),
                                    rx.switch(
                                        is_checked=State.use_map_for_location,
                                        on_change=State.set_use_map_for_location,
                                        id="use_map_switch",
                                    ),
                                    rx.text("Needs chaperone?", weight="bold", size="2"),
                                    rx.switch(
                                        is_checked=State.activity_needs_chaperone,
                                        on_change=State.set_activity_needs_chaperone,
                                    ),
                                    spacing="4",
                                    align_items="center",
                                ),
                                rx.cond(
                                    State.use_map_for_location,
                                    rx.fragment(
                                        rx.cond(
                                            GOOGLE_MAPS_API_KEY != "",
                                            rx.fragment(
                                                rx.vstack(
                                                    rx.text(
                                                        "Coordinates (set by clicking on map)",
                                                        weight="bold",
                                                        size="2",
                                                        margin_bottom="1",
                                                    ),
                                                    rx.hstack(
                                                        rx.vstack(
                                                            rx.text("Latitude", size="1", color="var(--gray-10)"),
                                                            rx.input(
                                                                id="edit_activity_latitude_hidden",
                                                                type="text",
                                                                value=State.activity_latitude,
                                                                on_change=State.set_activity_latitude,
                                                                placeholder="e.g., 42.5364",
                                                                width="100%",
                                                            ),
                                                            width="100%",
                                                            align_items="start",
                                                        ),
                                                        rx.vstack(
                                                            rx.text("Longitude", size="1", color="var(--gray-10)"),
                                                            rx.input(
                                                                id="edit_activity_longitude_hidden",
                                                                type="text",
                                                                value=State.activity_longitude,
                                                                on_change=State.set_activity_longitude,
                                                                placeholder="e.g., -72.5278",
                                                                width="100%",
                                                            ),
                                                            width="100%",
                                                            align_items="start",
                                                        ),
                                                        spacing="2",
                                                        width="100%",
                                                    ),
                                                    width="100%",
                                                    align_items="start",
                                                    margin_bottom="2",
                                                ),
                                                rx.box(
                                                    id="edit_activity_map",
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
                                width="100%",
                                align_items="start",
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
                            rx.hstack(
                                rx.link(
                                    rx.button(
                                        "Cancel",
                                        variant="outline",
                                        size="3",
                                        width="100%",
                                    ),
                                    href=rx.cond(
                                        State.editing_activity_id,
                                        f"/activity/{State.editing_activity_id}",
                                        "/explore",
                                    ),
                                ),
                                rx.button(
                                    "Update Activity",
                                    id="update_activity_button",
                                    on_click=State.update_activity,
                                    size="3",
                                    width="100%",
                                    color_scheme="teal",
                                ),
                                spacing="4",
                                width="100%",
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
                # Redirect to home if not authenticated
                rx.center(
                    rx.vstack(
                        rx.heading("Please Login", size="6"),
                        rx.text("You need to be logged in to edit activities."),
                        rx.link(
                            rx.button("Back to Home"),
                            href="/",
                        ),
                        spacing="4",
                        align="center",
                    ),
                    padding="10",
                    width="100%",
                ),
            ),
            on_mount=State.load_activity_for_edit,
        )
    )
