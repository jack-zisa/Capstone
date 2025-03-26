import { useState } from "react";

const GoogleSyncButton = () => {
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    const syncData = async () => {
        setLoading(true);
        setMessage("");

        const response = await fetch("https://ai-health-analytics-968401790916.us-central1.run.app/google/sync", {
            method: "POST",
            credentials: "include",
        });

        const data = await response.json();
        setMessage(data.message || data.error);
        setLoading(false);
    };

    return (
        <div>
            <button onClick={syncData} disabled={loading}>
                {loading ? "Syncing..." : "Sync Google Data"}
            </button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default GoogleSyncButton;