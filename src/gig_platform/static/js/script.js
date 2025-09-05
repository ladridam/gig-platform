/**
 * Gig Platform JavaScript utilities
 * Enhanced with better error handling and modern JS features
 */

class GigPlatform {
    constructor() {
        this.debounceTimers = new Map();
        this.init();
    }

    init() {
        this.initLocationAutocomplete();
        this.initDeleteConfirmations();
        this.initGeolocationButton();
        this.initFormValidations();
        this.initMapInteractions();
    }

    initLocationAutocomplete() {
        const locationInputs = document.querySelectorAll('input[name="location"]');
        
        locationInputs.forEach(input => {
            input.addEventListener('input', this.debounce(async (e) => {
                const query = e.target.value.trim();
                if (query.length < 3) {
                    this.removeSuggestions(input);
                    return;
                }
                
                try {
                    const response = await fetch(
                        `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`
                    );
                    
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    
                    const data = await response.json();
                    this.showLocationSuggestions(data, input);
                } catch (error) {
                    console.error('Error fetching locations:', error);
                    this.showErrorToast('Failed to fetch location suggestions');
                }
            }, 300));
            
            input.addEventListener('blur', () => {
                setTimeout(() => {
                    this.removeSuggestions(input);
                }, 200);
            });
        });
    }

    debounce(func, wait) {
        return (...args) => {
            clearTimeout(this.debounceTimers.get(func));
            this.debounceTimers.set(func, setTimeout(() => func.apply(this, args), wait));
        };
    }

    showLocationSuggestions(locations, input) {
        this.removeSuggestions(input);
        
        if (locations.length === 0) {
            this.showNoResultsMessage(input);
            return;
        }
        
        const list = document.createElement('ul');
        list.className = 'list-group location-suggestions';
        
        locations.slice(0, 5).forEach(location => {
            const item = document.createElement('li');
            item.className = 'list-group-item list-group-item-action';
            item.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <span>${location.display_name}</span>
                    <small class="text-muted">${location.type}</small>
                </div>
            `;
            item.style.cursor = 'pointer';
            
            item.addEventListener('click', () => {
                input.value = location.display_name;
                document.getElementById('location-lat').value = location.lat;
                document.getElementById('location-lng').value = location.lon;
                this.removeSuggestions(input);
            });
            
            list.appendChild(item);
        });
        
        input.parentNode.appendChild(list);
    }

    showNoResultsMessage(input) {
        this.removeSuggestions(input);
        
        const message = document.createElement('div');
        message.className = 'alert alert-warning mt-2';
        message.textContent = 'No locations found. Try a different search term.';
        
        input.parentNode.appendChild(message);
        
        // Remove message after 3 seconds
        setTimeout(() => {
            message.remove();
        }, 3000);
    }

    removeSuggestions(input) {
        const existingList = input.parentNode.querySelector('.location-suggestions');
        const existingAlert = input.parentNode.querySelector('.alert');
        
        if (existingList) existingList.remove();
        if (existingAlert) existingAlert.remove();
    }

    initDeleteConfirmations() {
        const deleteForms = document.querySelectorAll('form[action*="delete"]');
        
        deleteForms.forEach(form => {
            form.addEventListener('submit', (e) => {
                if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                    e.preventDefault();
                }
            });
        });
    }

    initGeolocationButton() {
        const locationInputs = document.querySelectorAll('input[name="location"]');
        
        if (!navigator.geolocation || locationInputs.length === 0) return;
        
        locationInputs.forEach(input => {
            // Check if button already exists
            if (input.parentNode.querySelector('.geolocation-btn')) return;
            
            const getLocationBtn = document.createElement('button');
            getLocationBtn.type = 'button';
            getLocationBtn.className = 'btn btn-outline-secondary mt-2 geolocation-btn';
            getLocationBtn.innerHTML = '<i class="fas fa-location-crosshairs"></i> Use My Current Location';
            
            getLocationBtn.addEventListener('click', async () => {
                const originalText = getLocationBtn.innerHTML;
                getLocationBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Getting location...';
                getLocationBtn.disabled = true;
                
                try {
                    const position = await this.getCurrentPosition();
                    const { latitude: lat, longitude: lng } = position.coords;
                    
                    const address = await this.reverseGeocode(lat, lng);
                    if (address) {
                        input.value = address;
                    } else {
                        input.value = `${lat.toFixed(6)}, ${lng.toFixed(6)}`;
                    }
                    
                    document.getElementById('location-lat').value = lat;
                    document.getElementById('location-lng').value = lng;
                    
                } catch (error) {
                    console.error('Geolocation error:', error);
                    this.showErrorToast('Unable to get your location: ' + error.message);
                } finally {
                    getLocationBtn.innerHTML = originalText;
                    getLocationBtn.disabled = false;
                }
            });
            
            input.parentNode.appendChild(getLocationBtn);
        });
    }

    getCurrentPosition() {
        return new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(resolve, reject, {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 60000
            });
        });
    }

    async reverseGeocode(lat, lng) {
        try {
            const response = await fetch(
                `https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&zoom=18&addressdetails=1`
            );
            
            if (!response.ok) throw new Error('Reverse geocoding failed');
            
            const data = await response.json();
            return data.display_name || null;
            
        } catch (error) {
            console.error('Reverse geocoding error:', error);
            return null;
        }
    }

    initFormValidations() {
        const forms = document.querySelectorAll('form');
        
        forms.forEach(form => {
            form.addEventListener('submit', (e) => {
                const requiredFields = form.querySelectorAll('[required]');
                let isValid = true;
                
                requiredFields.forEach(field => {
                    if (!field.value.trim()) {
                        isValid = false;
                        this.highlightError(field, 'This field is required');
                    }
                });
                
                if (!isValid) {
                    e.preventDefault();
                    this.showErrorToast('Please fill in all required fields');
                }
            });
        });
    }

    highlightError(field, message) {
        field.classList.add('is-invalid');
        
        let errorDiv = field.parentNode.querySelector('.invalid-feedback');
        if (!errorDiv) {
            errorDiv = document.createElement('div');
            errorDiv.className = 'invalid-feedback';
            field.parentNode.appendChild(errorDiv);
        }
        
        errorDiv.textContent = message;
    }

    initMapInteractions() {
        // Additional map functionality can be added here
        const mapElement = document.getElementById('map');
        if (mapElement) {
            this.enhanceMapFunctionality();
        }
    }

    enhanceMapFunctionality() {
        // Add zoom controls, layer toggles, etc.
        console.log('Map enhancement initialized');
    }

    showErrorToast(message) {
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = 'alert alert-danger alert-dismissible fade show position-fixed';
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 5000);
    }

    showSuccessToast(message) {
        const toast = document.createElement('div');
        toast.className = 'alert alert-success alert-dismissible fade show position-fixed';
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        setTimeout(() => {
            if (toast.parentNode) {
                toast.remove();
            }
        }, 3000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.gigPlatform = new GigPlatform();
});

// Utility functions for backward compatibility
function initLocationAutocomplete() {
    if (window.gigPlatform) {
        window.gigPlatform.initLocationAutocomplete();
    }
}

function initDeleteConfirmations() {
    if (window.gigPlatform) {
        window.gigPlatform.initDeleteConfirmations();
    }
}

function initGeolocationButton() {
    if (window.gigPlatform) {
        window.gigPlatform.initGeolocationButton();
    }
}

// Export for global access if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = GigPlatform;
}