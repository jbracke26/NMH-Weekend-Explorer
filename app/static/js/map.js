// Google Maps initialization and marker management
let map;
let homeMap;
let markers = [];
let homeMarkers = [];
let infoWindows = [];
let homeInfoWindows = [];

function initMap() {
    const mapContainer = document.getElementById('map');
    if (!mapContainer) return;

    // Default center (NMH campus approximate location)
    const defaultCenter = { lat: 42.5364, lng: -72.5278 };
    
    map = new google.maps.Map(mapContainer, {
        zoom: 14,
        center: defaultCenter,
        mapTypeControl: true,
        streetViewControl: true,
        fullscreenControl: true,
    });

    // Load activities and add markers
    loadActivities();
}

function initHomeMap() {
    const mapContainer = document.getElementById('home_map');
    if (!mapContainer) return;

    // Default center (NMH campus approximate location)
    const defaultCenter = { lat: 42.5364, lng: -72.5278 };
    
    homeMap = new google.maps.Map(mapContainer, {
        zoom: 14,
        center: defaultCenter,
        mapTypeControl: true,
        streetViewControl: true,
        fullscreenControl: true,
    });

    // Load activities and add markers
    loadHomeMapActivities();
}

function loadActivities() {
    // Get activities from the page data
    const activitiesData = window.activitiesData || [];
    
    // Clear existing markers
    clearMarkers();
    
    if (activitiesData.length === 0) {
        return;
    }

    // Geocode activities and add markers
    const geocoder = new google.maps.Geocoder();
    let geocodedCount = 0;
    
    activitiesData.forEach((activity, index) => {
        const location = activity.location || '';
        if (!location) return;
        
        // Try to geocode the location
        geocoder.geocode({ address: location + ', Northfield, MA' }, (results, status) => {
            if (status === 'OK' && results[0]) {
                const position = results[0].geometry.location;
                addMarker(activity, position);
            } else {
                // If geocoding fails, use default position with offset
                const defaultPos = {
                    lat: 42.5364 + (index * 0.01),
                    lng: -72.5278 + (index * 0.01)
                };
                addMarker(activity, defaultPos);
            }
            
            geocodedCount++;
            if (geocodedCount === activitiesData.length) {
                // Fit map to show all markers
                fitMapToMarkers();
            }
        });
    });
}

function loadHomeMapActivities() {
    // Get activities from the page data
    const activitiesData = window.homeActivitiesData || [];
    
    // Clear existing markers
    clearHomeMarkers();
    
    if (activitiesData.length === 0 || !homeMap) {
        return;
    }

    // Geocode activities and add markers
    const geocoder = new google.maps.Geocoder();
    let geocodedCount = 0;
    
    activitiesData.forEach((activity, index) => {
        const location = activity.location || '';
        if (!location) return;
        
        // Try to geocode the location
        geocoder.geocode({ address: location + ', Northfield, MA' }, (results, status) => {
            if (status === 'OK' && results[0]) {
                const position = results[0].geometry.location;
                addHomeMarker(activity, position);
            } else {
                // If geocoding fails, use default position with offset
                const defaultPos = {
                    lat: 42.5364 + (index * 0.01),
                    lng: -72.5278 + (index * 0.01)
                };
                addHomeMarker(activity, defaultPos);
            }
            
            geocodedCount++;
            if (geocodedCount === activitiesData.length) {
                // Fit map to show all markers
                fitHomeMapToMarkers();
            }
        });
    });
}

function addMarker(activity, position) {
    const marker = new google.maps.Marker({
        position: position,
        map: map,
        title: activity.title,
        icon: {
            url: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
            scaledSize: new google.maps.Size(32, 32)
        }
    });

    const infoWindow = new google.maps.InfoWindow({
        content: `
            <div style="padding: 8px; min-width: 200px;">
                <h3 style="margin: 0 0 8px 0; font-size: 16px; font-weight: bold;">
                    ${activity.title}
                </h3>
                <p style="margin: 4px 0; color: #666; font-size: 12px;">
                    <strong>Category:</strong> ${activity.category || 'Other'}
                </p>
                <p style="margin: 4px 0; color: #666; font-size: 12px;">
                    <strong>Location:</strong> ${activity.location || 'N/A'}
                </p>
                <p style="margin: 4px 0; color: #666; font-size: 12px;">
                    <strong>Time:</strong> ${activity.time || 'N/A'}
                </p>
                <a href="/activity/${activity.id}" 
                   style="display: inline-block; margin-top: 8px; padding: 6px 12px; 
                          background: #007bff; color: white; text-decoration: none; 
                          border-radius: 4px; font-size: 12px;">
                    View Details
                </a>
            </div>
        `
    });

    marker.addListener('click', () => {
        // Close all other info windows
        infoWindows.forEach(iw => iw.close());
        infoWindow.open(map, marker);
    });

    markers.push(marker);
    infoWindows.push(infoWindow);
}

function addHomeMarker(activity, position) {
    const marker = new google.maps.Marker({
        position: position,
        map: homeMap,
        title: activity.title,
        icon: {
            url: 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
            scaledSize: new google.maps.Size(32, 32)
        }
    });

    const infoWindow = new google.maps.InfoWindow({
        content: `
            <div style="padding: 8px; min-width: 200px;">
                <h3 style="margin: 0 0 8px 0; font-size: 16px; font-weight: bold;">
                    ${activity.title}
                </h3>
                <p style="margin: 4px 0; color: #666; font-size: 12px;">
                    <strong>Category:</strong> ${activity.category || 'Other'}
                </p>
                <p style="margin: 4px 0; color: #666; font-size: 12px;">
                    <strong>Location:</strong> ${activity.location || 'N/A'}
                </p>
                <p style="margin: 4px 0; color: #666; font-size: 12px;">
                    <strong>Time:</strong> ${activity.time || 'N/A'}
                </p>
                <a href="/activity/${activity.id}" 
                   style="display: inline-block; margin-top: 8px; padding: 6px 12px; 
                          background: #007bff; color: white; text-decoration: none; 
                          border-radius: 4px; font-size: 12px;">
                    View Details
                </a>
            </div>
        `
    });

    marker.addListener('click', () => {
        // Close all other info windows
        homeInfoWindows.forEach(iw => iw.close());
        infoWindow.open(homeMap, marker);
    });

    homeMarkers.push(marker);
    homeInfoWindows.push(infoWindow);
}

function clearMarkers() {
    markers.forEach(marker => marker.setMap(null));
    markers = [];
    infoWindows = [];
}

function clearHomeMarkers() {
    homeMarkers.forEach(marker => marker.setMap(null));
    homeMarkers = [];
    homeInfoWindows = [];
}

function fitMapToMarkers() {
    if (markers.length === 0 || !map) return;
    
    const bounds = new google.maps.LatLngBounds();
    markers.forEach(marker => {
        bounds.extend(marker.getPosition());
    });
    
    if (markers.length === 1) {
        map.setCenter(markers[0].getPosition());
        map.setZoom(15);
    } else {
        map.fitBounds(bounds);
    }
}

function fitHomeMapToMarkers() {
    if (homeMarkers.length === 0 || !homeMap) return;
    
    const bounds = new google.maps.LatLngBounds();
    homeMarkers.forEach(marker => {
        bounds.extend(marker.getPosition());
    });
    
    if (homeMarkers.length === 1) {
        homeMap.setCenter(homeMarkers[0].getPosition());
        homeMap.setZoom(15);
    } else {
        homeMap.fitBounds(bounds);
    }
}

// Export functions for use in Reflex
window.initMap = initMap;
window.initHomeMap = initHomeMap;
window.loadActivities = loadActivities;
window.loadHomeMapActivities = loadHomeMapActivities;
window.clearMarkers = clearMarkers;
window.clearHomeMarkers = clearHomeMarkers;

