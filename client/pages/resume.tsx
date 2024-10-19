import ResumeQuestionnaire from '../components/ResumeQuestionnaire';
import Navbar from '../components/Navbar';
import ProtectedRoute from '../components/ProtectedRoute';

const ResumePage = () => {
    return (
        <div>
            <Navbar />
            <ResumeQuestionnaire />
        </div>
    );
};

export default ProtectedRoute(ResumePage);