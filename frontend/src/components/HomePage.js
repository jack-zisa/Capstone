import AnalyzeDataButton from "./AnalyzeDataButton";
import FitbitLoginForm from "./FitbitLoginForm";
import FitbitSyncButton from "./FitbitSyncButton";
import { useNavigate } from "react-router-dom"; // Import useNavigate

function HomePage() {
  const navigate = useNavigate();

  return (
    <div className="HomePage">
      <h2>Welcome</h2>
      <FitbitLoginForm/>
      <FitbitSyncButton/>
      <AnalyzeDataButton/>
      <button onClick={() => navigate("/account")}>Account</button>
    </div>
  );
}

export default HomePage;
