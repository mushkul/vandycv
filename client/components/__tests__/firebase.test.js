
import { signIn, getUserData } from '../firebase';
jest.mock('firebase/app', () => ({
  auth: jest.fn(() => ({
    signInWithEmailAndPassword: jest.fn(() => Promise.resolve({ user: { uid: '123' } })),
  })),
}));

test('Firebase signIn function', async () => {
  const user = await signIn('test@example.com', 'password');
  expect(user.uid).toBe('123');
});

test('Firebase getUserData fails with invalid user', async () => {
  await expect(getUserData(null)).rejects.toThrow('User not found');
});