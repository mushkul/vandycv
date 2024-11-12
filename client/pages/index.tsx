import { useEffect } from 'react';
import { useRouter } from 'next/router';

function Index() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to /home
    router.push('/home');
  }, [router]);

  return null; // No need to render anything as we are redirecting
}

export default Index;