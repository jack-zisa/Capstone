import Alerts from "./Alerts";
import AnalyzeDataButton from "./AnalyzeDataButton";
import FitbitLoginForm from "./FitbitLoginForm";
import FitbitSyncButton from "./FitbitSyncButton";
import { useNavigate } from "react-router-dom"; // Import useNavigate
import { useAuth } from "../context/AuthContext"
import GoogleAuthButton from "./GoogleAuthButton";
import GoogleSyncButton from "./GoogleSyncButton";

function HomePage() {
  const navigate = useNavigate();
  const { isFitbitSynced, isGoogleSynced } = useAuth();

  return (
    <div className="HomePage">
      <h2>Welcome</h2>
      {isFitbitSynced ? <></> : <FitbitLoginForm/>}
      <FitbitSyncButton/>
      {isGoogleSynced ? <></> : <GoogleAuthButton/>}
      {isGoogleSynced ? <GoogleSyncButton/> : <></>}
      <AnalyzeDataButton/>
      <button onClick={() => navigate("/account")}>Account</button>
      <Alerts/>
    </div>
  );
}

export default HomePage;
