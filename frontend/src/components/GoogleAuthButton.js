import { GoogleOAuthProvider, GoogleLogin } from '@react-oauth/google';
import { useAuth } from "../context/AuthContext"

const clientId = "968401790916-rg4avbapuai2u68dv9ivedlddfbp2ock.apps.googleusercontent.com";

function GoogleAuthButton() {
  const { setGoogleSynced } = useAuth();

  const handleSuccess = (response) => {
    fetch("https://ai-health-analytics-968401790916.us-central1.run.app/auth/google/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: response.credential }),
    })
      .then((res) => res.json())
      .then((data) => {
        setGoogleSynced(true);
        console.log("Authenticated:", data)
    })
      .catch((err) => console.error("Login failed", err));
  };

  return (
    <GoogleOAuthProvider clientId={clientId}>
      <GoogleLogin onSuccess={handleSuccess} onError={() => console.log("Login failed")} />
    </GoogleOAuthProvider>
  );
}

export default GoogleAuthButton;