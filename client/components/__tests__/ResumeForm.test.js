import { render, screen } from '@testing-library/react';
import ResumeForm from '../ResumeForm';

test('renders ResumeForm with initial fields', () => {
  render(<ResumeForm />);
  expect(screen.getByLabelText(/Name/i)).toBeInTheDocument();
});

test('submits form correctly', () => {
  render(<ResumeForm />);
  const submitButton = screen.getByRole('button', { name: /submit/i });
  fireEvent.click(submitButton);
  expect(screen.getByText(/error/i)).toBeInTheDocument();  // if error handling present
});