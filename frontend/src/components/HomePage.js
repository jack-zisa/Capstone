import AnalyzeDataButton from "./AnalyzeDataButton";
import FitbitLoginForm from "./FitbitLoginForm";
import FitbitSyncButton from "./FitbitSyncButton";

function HomePage() {
  return (
    <div className="HomePage">
      <h2>Welcome</h2>
      <FitbitLoginForm/>
      <FitbitSyncButton/>
      <AnalyzeDataButton/>
    </div>
  );
}

export default HomePage;
