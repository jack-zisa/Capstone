import React, { useState } from "react";

const AnalyzeDataButton = () => {
  const [analysis, setAnalysis] = useState([]);
  const [loading, setLoading] = useState(false);

  const analyzeRecentData = async () => {
    setLoading(true);
    setAnalysis([]); // Clear previous results

    try {
      const response = await fetch("/analysis/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });

      const data = await response.json();

      if (data.response) {
        const parsedData = JSON.parse(data.response);
        setAnalysis(parsedData);
      } else {
        setAnalysis("Error analyzing data.");
      }
    } catch (error) {
      setAnalysis("Failed to connect to server.");
    }

    setLoading(false);
  };

  return (
    <div>
      <button onClick={analyzeRecentData} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Recent Data"}
      </button>
      
      {Array.isArray(analysis) && analysis.length > 0 ? (
        <table>
          <thead>
            <tr>
              {Object.keys(analysis[0]).map((key) => (
                <th key={key}>{key}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {analysis.map((row, index) => (
              <tr key={index}>
                {Object.values(row).map((value, i) => (
                  <td key={i}>{value}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>{analysis}</p>
      )}
    </div>
  );
};

export default AnalyzeDataButton;