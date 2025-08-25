document.addEventListener('DOMContentLoaded', function() {
    initLocationAutocomplete();
    initDeleteConfirmations();
    initGeolocationButton();
});

function initLocationAutocomplete() {
    const locationInputs = document.querySelectorAll('input[name="location"]');
    
    locationInputs.forEach(input => {
        // Add autocomplete functionality
        input.addEventListener('input', debounce(function(e) {
            const query = e.target.value;
            if (query.length < 3) {
                removeSuggestions(input);
                return;
            }
            
            // Search for locations
            fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    // Create suggestions dropdown
                    showLocationSuggestions(data, input);
                })
                .catch(error => console.error('Error fetching locations:', error));
        }, 300));
        
        // Clear suggestions when input loses focus (with a delay to allow clicking)
        input.addEventListener('blur', function() {
            setTimeout(() => {
                removeSuggestions(input);
            }, 200);
        });
    });
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function showLocationSuggestions(locations, input) {
    // Remove existing suggestions
    removeSuggestions(input);
    
    if (locations.length === 0) return;
    
    // Create suggestions list
    const list = document.createElement('ul');
    list.className = 'list-group location-suggestions';
    
    locations.slice(0, 5).forEach(location => {
        const item = document.createElement('li');
        item.className = 'list-group-item list-group-item-action';
        item.textContent = location.display_name;
        item.style.cursor = 'pointer';
        
        item.addEventListener('click', function() {
            input.value = location.display_name;
            document.getElementById('location-lat').value = location.lat;
            document.getElementById('location-lng').value = location.lon;
            removeSuggestions(input);
        });
        
        list.appendChild(item);
    });
    
    input.parentNode.appendChild(list);
}

function removeSuggestions(input) {
    const existingList = input.parentNode.querySelector('.location-suggestions');
    if (existingList) {
        existingList.remove();
    }
}

function initDeleteConfirmations() {
    // Confirm delete actions
    const deleteForms = document.querySelectorAll('form[action*="delete"]');
    deleteForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });
}

function initGeolocationButton() {
    // Add geolocation button to location inputs
    const locationInputs = document.querySelectorAll('input[name="location"]');
    
    if (navigator.geolocation && locationInputs.length > 0) {
        locationInputs.forEach(input => {
            const getLocationBtn = document.createElement('button');
            getLocationBtn.type = 'button';
            getLocationBtn.className = 'btn btn-outline-secondary mt-2';
            getLocationBtn.innerHTML = '<i class="fas fa-location-crosshairs"></i> Use My Current Location';
            
            getLocationBtn.addEventListener('click', function() {
                this.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Getting location...';
                this.disabled = true;
                
                navigator.geolocation.getCurrentPosition(
                    function(position) {
                        const lat = position.coords.latitude;
                        const lng = position.coords.longitude;
                        
                        // Reverse geocode to get address
                        fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
                            .then(response => response.json())
                            .then(data => {
                                if (data.display_name) {
                                    input.value = data.display_name;
                                    document.getElementById('location-lat').value = lat;
                                    document.getElementById('location-lng').value = lng;
                                }
                                getLocationBtn.innerHTML = '<i class="fas fa-location-crosshairs"></i> Use My Current Location';
                                getLocationBtn.disabled = false;
                            })
                            .catch(error => {
                                console.error('Error reverse geocoding:', error);
                                input.value = `${lat.toFixed(4)}, ${lng.toFixed(4)}`;
                                document.getElementById('location-lat').value = lat;
                                document.getElementById('location-lng').value = lng;
                                getLocationBtn.innerHTML = '<i class="fas fa-location-crosshairs"></i> Use My Current Location';
                                getLocationBtn.disabled = false;
                            });
                    },
                    function(error) {
                        alert('Unable to get your location: ' + error.message);
                        getLocationBtn.innerHTML = '<i class="fas fa-location-crosshairs"></i> Use My Current Location';
                        getLocationBtn.disabled = false;
                    }
                );
            });
            
            input.parentNode.appendChild(getLocationBtn);
        });
    }
}