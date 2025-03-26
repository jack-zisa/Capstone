import { createContext, useState, useContext } from "react";

// Create the context
const AuthContext = createContext();

// Provider component
export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [isFitbitSynced, setFitbitSynced] = useState(false);
  const [isGoogleSynced, setGoogleSynced] = useState(false);

  return (
    <AuthContext.Provider value={{ isLoggedIn, setIsLoggedIn, isFitbitSynced, setFitbitSynced, isGoogleSynced, setGoogleSynced }}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook for using auth
export const useAuth = () => useContext(AuthContext);