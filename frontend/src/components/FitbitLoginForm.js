import React, { useState } from 'react';
import axios from 'axios';

const FitbitLoginForm = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const clientId = '23Q3B8';
  const redirectUri = 'https://ai-health-analytics-968401790916.us-central1.run.app/auth/fitbit/callback';
  const scope = 'heartrate profile';

  const fitbitAuthUrl = `https://www.fitbit.com/oauth2/authorize?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirectUri)}&response_type=code&scope=${encodeURIComponent(scope)}`;

  const handleFitbitAuth = () => {
    // Redirect to Fitbit's OAuth login page with the necessary parameters
    window.location.href = fitbitAuthUrl;
  };  

  // Handle form submission
  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Example POST request to authenticate the user
      const response = await axios.post('https://https://ai-health-analytics-968401790916.us-central1.run.app/auth/fitbit/login', {
        email,
        password,
      });

      // Handle successful login
      if (response.data.success) {
        // Redirect to another page or show success
        console.log('Login successful!');
      } else {
        setError('Invalid credentials');
      }
    } catch (err) {
      setError('An error occurred during login');
      console.error('Error during login:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fitbit-login-form">
        <h2>Fitbit Login</h2>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="email">Email</label>
            <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
            />
            </div>
            <div>
            <label htmlFor="password">Password</label>
            <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
            />
            </div>
              {error && <div className="error-message">{error}</div>}
            <div>
          </div>
        </form>

    {/* Fitbit OAuth Login Button */}
    <div>
        <button onClick={handleFitbitAuth} disabled={loading}>
            Login with Fitbit
        </button>
    </div>

    </div>
  );
};

export default FitbitLoginForm;