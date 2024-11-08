const API_BASE_URL = 'http://localhost:8000/api';

async function handleResponse(response) {
    if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.message || 'An error occurred');
    }
    return response.json();
}

export async function fetchWithAuth(endpoint, options = {}) {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers: {
            'Content-Type': 'application/json',
            ...options.headers,
        },
    });
    return handleResponse(response);
}