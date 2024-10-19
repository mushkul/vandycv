import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from '../firebase';

const ProtectedRoute = (Component: React.ComponentType) => {
  return function ProtectedComponent(props: any) {
    const router = useRouter();
    const [loading, setLoading] = useState(true);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    useEffect(() => {
      const unsubscribe = onAuthStateChanged(auth, (user) => {
        console.log("Auth state changed: ", user);  // Debugging log to check auth state
        if (user) {
          setIsAuthenticated(true);  // User is logged in
        } else {
          setIsAuthenticated(false);  // User is not logged in
          router.push('/login');  // Redirect to login if not authenticated
        }
        setLoading(false);  // Stop the loading indicator once the auth status is determined
      });

      return () => unsubscribe();  // Cleanup the listener on unmount
    }, [router]);

    if (loading) {
      return <p>Loading...</p>;  // Show loading while checking the auth state
    }

    return isAuthenticated ? <Component {...props} /> : null;  // Render the component only if authenticated
  };
};

export default ProtectedRoute;
