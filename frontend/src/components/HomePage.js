import AnalyzeDataButton from "./AnalyzeDataButton";
import FitbitLoginForm from "./FitbitLoginForm";
import FitbitSyncButton from "./FitbitSyncButton";
import { useAuth } from "../context/AuthContext"

function HomePage() {
  const { isLoggedIn } = useAuth();
  return (
    <div className="HomePage">
      <h2>Welcome</h2>
      {isLoggedIn ? <></> : <FitbitLoginForm/>}
      <FitbitSyncButton/>
      <AnalyzeDataButton/>
    </div>
  );
}

export default HomePage;
