const API_BASE = "https://ai-health-analytics-968401790916.us-central1.run.app/auth";  // Flask backend

export const registerUser = async (username, password) => {
    try {
        const response = await fetch(`${API_BASE}/register`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });

        return await response.json();
    } catch (error) {
        return { success: false, error: "Server error" };
    }
};

export const loginUser = async (username, password) => {
    try {
        const response = await fetch(`${API_BASE}/login`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, password }),
        });

        return response.json();;
    } catch (error) {
        return { success: false, error: "Server error" };
    }
};

export const loginWithFitbit = () => {
    window.location.href = `${API_BASE}/fitbit/login`;
};
