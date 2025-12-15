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
                        console.log('=== Create Activity Map Script Loaded ===');
                        
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
                            window._createActivityMapApiCallback = function() {{
                                console.log('Google Maps API loaded via callback');
                                window.googleMapsApiLoaded = true;
                                delete window._createActivityMapApiCallback;
                                if (callback) {{
                                    // Small delay to ensure everything is ready
                                    setTimeout(callback, 100);
                                }}
                            }};
                            
                            // Load the script
                            const script = document.createElement('script');
                            script.src = 'https://maps.googleapis.com/maps/api/js?key={GOOGLE_MAPS_API_KEY}&loading=async&callback=_createActivityMapApiCallback';
                            script.async = true;
                            script.defer = true;
                            script.onerror = function() {{
                                console.error('Failed to load Google Maps API');
                                delete window._createActivityMapApiCallback;
                            }};
                            document.head.appendChild(script);
                            console.log('Loading Google Maps API...');
                        }}
                        
                        if (!window.createActivityMapFunctions) {{
                            window.createActivityMap = null;
                            window.createActivityMarker = null;
                            window.createActivityMapInitialized = false;
                            window.createActivityMapInitAttempts = 0;
                            
                            window.initCreateActivityMap = function() {{
                                // Prevent too many attempts
                                if (window.createActivityMapInitAttempts > 10) {{
                                    console.error('Too many map initialization attempts, giving up');
                                    return;
                                }}
                                
                                window.createActivityMapInitAttempts++;
                                
                                const mapContainer = document.getElementById('create_activity_map');
                                if (!mapContainer) {{
                                    console.log('Map container not found');
                                    return;
                                }}
                                
                                // Check if container is visible
                                const computedStyle = window.getComputedStyle(mapContainer);
                                const isVisible = mapContainer.offsetParent !== null && 
                                                 computedStyle.display !== 'none' &&
                                                 computedStyle.visibility !== 'hidden' &&
                                                 mapContainer.offsetWidth > 0 &&
                                                 mapContainer.offsetHeight > 0;
                                
                                if (!isVisible) {{
                                    console.log('Map container not visible yet');
                                    return;
                                }}
                                
                                // Ensure Google Maps API is loaded
                                if (!window.google || !window.google.maps || !window.google.maps.Map) {{
                                    console.log('Google Maps API not ready, ensuring it is loaded...');
                                    ensureGoogleMapsApi(function() {{
                                        setTimeout(window.initCreateActivityMap, 100);
                                    }});
                                    return;
                                }}
                                
                                // Prevent double initialization
                                if (window.createActivityMap && window.createActivityMapInitialized) {{
                                    try {{
                                        const mapDiv = window.createActivityMap.getDiv();
                                        if (mapDiv && mapDiv === mapContainer) {{
                                            console.log('Map already initialized and attached');
                                            // Just trigger resize
                                            setTimeout(function() {{
                                                if (window.google && window.google.maps && window.google.maps.event && window.createActivityMap) {{
                                                    window.google.maps.event.trigger(window.createActivityMap, 'resize');
                                                }}
                                            }}, 100);
                                            return;
                                        }}
                                    }} catch (e) {{
                                        console.log('Error checking map attachment, reinitializing...');
                                        window.cleanupCreateActivityMap();
                                    }}
                                }}
                                
                                try {{
                                    // Ensure container has size
                                    if (mapContainer.offsetWidth < 100) {{
                                        mapContainer.style.width = '100%';
                                    }}
                                    if (mapContainer.offsetHeight < 100) {{
                                        mapContainer.style.height = '400px';
                                    }}
                                    
                                    // Wait a bit more if container still doesn't have proper size
                                    if (mapContainer.offsetWidth < 100 || mapContainer.offsetHeight < 100) {{
                                        setTimeout(window.initCreateActivityMap, 200);
                                        return;
                                    }}
                                    
                                    console.log('Initializing map with container size:', mapContainer.offsetWidth, 'x', mapContainer.offsetHeight);
                                    
                                    // Initialize map
                                    window.createActivityMap = new window.google.maps.Map(mapContainer, {{
                                        zoom: 14,
                                        center: {{ lat: 42.5364, lng: -72.5278 }},
                                        mapTypeControl: true,
                                        streetViewControl: true,
                                        fullscreenControl: true,
                                    }});
                                    
                                    // Trigger resize after a short delay
                                    setTimeout(function() {{
                                        if (window.google && window.google.maps && window.google.maps.event && window.createActivityMap) {{
                                            window.google.maps.event.trigger(window.createActivityMap, 'resize');
                                        }}
                                    }}, 200);
                                    
                                    // Add click listener
                                    window.createActivityMap.addListener('click', function(event) {{
                                        const lat = event.latLng.lat();
                                        const lng = event.latLng.lng();
                                        
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
                                                updateLocationFromMap(lat, lng);
                                            }});
                                        }}
                                        
                                        updateLocationFromMap(lat, lng);
                                        
                                        const geocoder = new window.google.maps.Geocoder();
                                        geocoder.geocode({{ location: event.latLng }}, function(results, status) {{
                                            if (status === 'OK' && results[0]) {{
                                                const addressInput = document.querySelector('#activity_location_input');
                                                if (addressInput) {{
                                                    addressInput.value = results[0].formatted_address;
                                                    addressInput.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                                }}
                                            }}
                                        }});
                                    }});
                                    
                                    window.createActivityMapInitialized = true;
                                    window.createActivityMapInitAttempts = 0;
                                    console.log('Create activity map initialized successfully');
                                }} catch (error) {{
                                    console.error('Error initializing create activity map:', error);
                                    window.createActivityMapInitialized = false;
                                    // Retry after a delay
                                    setTimeout(function() {{
                                        window.initCreateActivityMap();
                                    }}, 500);
                                }}
                            }};
                            
                            // NEW APPROACH: Directly update Reflex state using a more reliable method
                            function updateLocationFromMap(lat, lng) {{
                                console.log('updateLocationFromMap called with:', lat, lng);
                                const latStr = lat.toString();
                                const lngStr = lng.toString();
                                
                                // Store coordinates in window object as backup
                                window._tempLatitude = latStr;
                                window._tempLongitude = lngStr;
                                window._activityCoordinates = {{
                                    latitude: parseFloat(latStr),
                                    longitude: parseFloat(lngStr)
                                }};
                                
                                // Get hidden inputs
                                const latInput = document.getElementById('activity_latitude_hidden');
                                const lngInput = document.getElementById('activity_longitude_hidden');
                                
                                if (!latInput || !lngInput) {{
                                    console.error('Hidden inputs not found!');
                                    return;
                                }}
                                
                                // NEW APPROACH: Use React's synthetic event system if available
                                // Otherwise, use native events with proper structure
                                function updateInputValue(input, value) {{
                                    // Method 1: Direct value assignment
                                    input.value = value;
                                    
                                    // Method 2: Set attribute
                                    input.setAttribute('value', value);
                                    
                                    // Method 3: Use Object.defineProperty
                                    try {{
                                        Object.defineProperty(input, 'value', {{
                                            value: value,
                                            writable: true,
                                            configurable: true,
                                            enumerable: true
                                        }});
                                    }} catch (e) {{
                                        // If defineProperty fails, just set value normally
                                        input.value = value;
                                    }}
                                    
                                    // Method 4: Trigger React's onChange if available
                                    if (input._valueTracker) {{
                                        input._valueTracker.setValue('');
                                        input._valueTracker.setValue(value);
                                    }}
                                    
                                    // Method 5: Dispatch native events
                                    const inputEvent = new Event('input', {{ bubbles: true, cancelable: true }});
                                    const changeEvent = new Event('change', {{ bubbles: true, cancelable: true }});
                                    
                                    Object.defineProperty(inputEvent, 'target', {{ value: input, enumerable: true }});
                                    Object.defineProperty(changeEvent, 'target', {{ value: input, enumerable: true }});
                                    
                                    input.dispatchEvent(inputEvent);
                                    input.dispatchEvent(changeEvent);
                                    
                                    // Method 6: Try React's synthetic event system
                                    if (window.React && window.ReactDOM) {{
                                        try {{
                                            const nativeEvent = new Event('input', {{ bubbles: true }});
                                            Object.defineProperty(nativeEvent, 'target', {{ value: input }});
                                            const syntheticEvent = window.React.__SECRET_INTERNALS_DO_NOT_USE_OR_YOU_WILL_BE_FIRED?.ReactCurrentDispatcher?.current?.createSyntheticEvent?.(nativeEvent);
                                            if (syntheticEvent) {{
                                                input.dispatchEvent(syntheticEvent);
                                            }}
                                        }} catch (e) {{
                                            // React synthetic events not available, use native events
                                        }}
                                    }}
                                }}
                                
                                // Update both inputs
                                updateInputValue(latInput, latStr);
                                updateInputValue(lngInput, lngStr);
                                
                                console.log('Coordinates updated - lat:', latInput.value, 'lng:', lngInput.value);
                                
                                // Force a state update by triggering multiple events
                                setTimeout(function() {{
                                    // Trigger blur events to ensure state is updated
                                    latInput.focus();
                                    setTimeout(function() {{
                                        latInput.blur();
                                        const blurEvent = new Event('blur', {{ bubbles: true, cancelable: true }});
                                        Object.defineProperty(blurEvent, 'target', {{ value: latInput, enumerable: true }});
                                        latInput.dispatchEvent(blurEvent);
                                        
                                        lngInput.focus();
                                        setTimeout(function() {{
                                            lngInput.blur();
                                            const blurEvent2 = new Event('blur', {{ bubbles: true, cancelable: true }});
                                            Object.defineProperty(blurEvent2, 'target', {{ value: lngInput, enumerable: true }});
                                            lngInput.dispatchEvent(blurEvent2);
                                            
                                            // Final change event
                                            const finalChange = new Event('change', {{ bubbles: true, cancelable: true }});
                                            Object.defineProperty(finalChange, 'target', {{ value: latInput, enumerable: true }});
                                            latInput.dispatchEvent(finalChange);
                                            
                                            const finalChange2 = new Event('change', {{ bubbles: true, cancelable: true }});
                                            Object.defineProperty(finalChange2, 'target', {{ value: lngInput, enumerable: true }});
                                            lngInput.dispatchEvent(finalChange2);
                                            
                                            console.log('Final coordinates after all events:', latInput.value, lngInput.value);
                                        }}, 100);
                                    }}, 100);
                                }}, 100);
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
                                window.createActivityMapInitialized = false;
                                window.createActivityMapInitAttempts = 0;
                            }};
                            
                            // Function to force map initialization when container becomes visible
                            window.forceInitCreateActivityMap = function() {{
                                const mapContainer = document.getElementById('create_activity_map');
                                if (!mapContainer) {{
                                    return;
                                }}
                                
                                // Reset initialization flag if container was hidden
                                const computedStyle = window.getComputedStyle(mapContainer);
                                const isVisible = mapContainer.offsetParent !== null && 
                                                 computedStyle.display !== 'none' &&
                                                 computedStyle.visibility !== 'hidden';
                                
                                if (!isVisible) {{
                                    window.createActivityMapInitialized = false;
                                    window.createActivityMapInitAttempts = 0;
                                    return;
                                }}
                                
                                // If already initialized and attached, just trigger resize
                                if (window.createActivityMap && window.createActivityMapInitialized) {{
                                    try {{
                                        const mapDiv = window.createActivityMap.getDiv();
                                        if (mapDiv && mapDiv === mapContainer) {{
                                            setTimeout(function() {{
                                                if (window.google && window.google.maps && window.google.maps.event && window.createActivityMap) {{
                                                    window.google.maps.event.trigger(window.createActivityMap, 'resize');
                                                }}
                                            }}, 100);
                                            return;
                                        }}
                                    }} catch (e) {{
                                        console.log('Error checking map attachment, reinitializing...');
                                        window.cleanupCreateActivityMap();
                                    }}
                                }}
                                
                                // Ensure Google Maps API is loaded first
                                if (!window.google || !window.google.maps || !window.google.maps.Map) {{
                                    ensureGoogleMapsApi(function() {{
                                        window.forceInitCreateActivityMap();
                                    }});
                                    return;
                                }}
                                
                                // Wait for container to have size, then initialize
                                const checkAndInit = function(attempts) {{
                                    if (attempts > 30) {{
                                        console.log('Gave up initializing map after', attempts, 'attempts');
                                        return;
                                    }}
                                    
                                    const width = mapContainer.offsetWidth || mapContainer.clientWidth;
                                    const height = mapContainer.offsetHeight || mapContainer.clientHeight;
                                    
                                    if (width > 0 && height > 0) {{
                                        window.initCreateActivityMap();
                                    }} else {{
                                        setTimeout(function() {{
                                            checkAndInit(attempts + 1);
                                        }}, 100);
                                    }}
                                }};
                                
                                checkAndInit(0);
                            }};
                            
                            // Watch for map container visibility changes with MutationObserver
                            const observer = new MutationObserver(function(mutations) {{
                                const mapContainer = document.getElementById('create_activity_map');
                                if (mapContainer) {{
                                    window.forceInitCreateActivityMap();
                                }}
                            }});
                            
                            // Start observing when DOM is ready
                            if (document.readyState === 'loading') {{
                                document.addEventListener('DOMContentLoaded', function() {{
                                    observer.observe(document.body, {{
                                        childList: true,
                                        subtree: true,
                                        attributes: true,
                                        attributeFilter: ['style', 'class', 'display', 'id']
                                    }});
                                    
                                    // Initial check after DOM is ready
                                    setTimeout(function() {{
                                        window.forceInitCreateActivityMap();
                                    }}, 200);
                                }});
                            }} else {{
                                observer.observe(document.body, {{
                                    childList: true,
                                    subtree: true,
                                    attributes: true,
                                    attributeFilter: ['style', 'class', 'display', 'id']
                                }});
                                
                                // Initial check
                                setTimeout(function() {{
                                    window.forceInitCreateActivityMap();
                                }}, 200);
                            }}
                            
                            // Watch for switch changes and initialize map immediately
                            const watchSwitch = function() {{
                                const switchElement = document.querySelector('input[type="checkbox"][id*="use_map"], input[type="checkbox"]');
                                if (switchElement) {{
                                    switchElement.addEventListener('change', function() {{
                                        console.log('Switch toggled, forcing map initialization...');
                                        setTimeout(function() {{
                                            window.forceInitCreateActivityMap();
                                        }}, 300);
                                    }});
                                }} else {{
                                    setTimeout(watchSwitch, 200);
                                }}
                            }};
                            
                            // Start watching for switch after DOM is ready
                            if (document.readyState === 'loading') {{
                                document.addEventListener('DOMContentLoaded', watchSwitch);
                            }} else {{
                                watchSwitch();
                            }}
                            
                            // Aggressive polling when map container exists but map is not initialized
                            let checkCount = 0;
                            const aggressiveCheck = setInterval(function() {{
                                checkCount++;
                                const mapContainer = document.getElementById('create_activity_map');
                                
                                if (mapContainer) {{
                                    const computedStyle = window.getComputedStyle(mapContainer);
                                    const isVisible = mapContainer.offsetParent !== null && 
                                                     computedStyle.display !== 'none' &&
                                                     computedStyle.visibility !== 'hidden' &&
                                                     mapContainer.offsetWidth > 0 &&
                                                     mapContainer.offsetHeight > 0;
                                    
                                    if (isVisible && !window.createActivityMapInitialized) {{
                                        window.forceInitCreateActivityMap();
                                    }}
                                    
                                    // Stop aggressive checking after map is initialized or after many attempts
                                    if ((window.createActivityMapInitialized && isVisible) || checkCount > 50) {{
                                        clearInterval(aggressiveCheck);
                                    }}
                                }} else if (checkCount > 50) {{
                                    clearInterval(aggressiveCheck);
                                }}
                            }}, 150);
                            
                            // Simple interceptor: just sync coordinates to hidden inputs without preventing click
                            // This avoids infinite loops by not re-triggering the button click
                            function setupCreateButtonInterceptor() {{
                                const createButton = document.getElementById('create_activity_button');
                                if (createButton) {{
                                    createButton.addEventListener('click', function(e) {{
                                        console.log('Create Activity button clicked - syncing coordinates');
                                        
                                        // Get coordinates from multiple sources
                                        const latInput = document.getElementById('activity_latitude_hidden');
                                        const lngInput = document.getElementById('activity_longitude_hidden');
                                        
                                        let latStr = '';
                                        let lngStr = '';
                                        
                                        // Try hidden inputs first
                                        if (latInput && lngInput) {{
                                            latStr = latInput.value || '';
                                            lngStr = lngInput.value || '';
                                        }}
                                        
                                        // Fallback to window object
                                        if (!latStr || !lngStr) {{
                                            latStr = window._tempLatitude || '';
                                            lngStr = window._tempLongitude || '';
                                        }}
                                        
                                        console.log('Coordinates found:', latStr, lngStr);
                                        
                                        // If we have coordinates, sync them to hidden inputs
                                        // Don't prevent click - just sync and let it proceed
                                        if (latStr && lngStr && latInput && lngInput) {{
                                            latInput.value = latStr;
                                            lngInput.value = lngStr;
                                            
                                            // Dispatch change events to update Reflex state
                                            const changeEvent = new Event('change', {{ bubbles: true, cancelable: true }});
                                            Object.defineProperty(changeEvent, 'target', {{ value: latInput, enumerable: true }});
                                            latInput.dispatchEvent(changeEvent);
                                            
                                            const changeEvent2 = new Event('change', {{ bubbles: true, cancelable: true }});
                                            Object.defineProperty(changeEvent2, 'target', {{ value: lngInput, enumerable: true }});
                                            lngInput.dispatchEvent(changeEvent2);
                                            
                                            console.log('Coordinates synced to hidden inputs:', latInput.value, lngInput.value);
                                        }}
                                        
                                        // Allow click to proceed normally - no preventDefault, no re-triggering
                                        console.log('Proceeding with button click');
                                    }}, true); // Use capture phase
                                }} else {{
                                    // Retry if button not found yet
                                    setTimeout(setupCreateButtonInterceptor, 500);
                                }}
                            }}
                            
                            // Setup interceptor when DOM is ready
                            if (document.readyState === 'loading') {{
                                document.addEventListener('DOMContentLoaded', setupCreateButtonInterceptor);
                            }} else {{
                                setupCreateButtonInterceptor();
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
                                                            id="activity_latitude_hidden",
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
                                                            id="activity_longitude_hidden",
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
                            width="100%",
                            align_items="start",
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
                            id="create_activity_button",
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
