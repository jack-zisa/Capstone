import { useState } from "react";

const FitbitSyncButton = () => {
    const [loading, setLoading] = useState(false);
    const [message, setMessage] = useState("");

    const syncData = async () => {
        setLoading(true);
        setMessage("");

        const response = await fetch("/fitbit/sync", {
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
                {loading ? "Syncing..." : "Sync Fitbit Data"}
            </button>
            {message && <p>{message}</p>}
        </div>
    );
};

export default FitbitSyncButton;