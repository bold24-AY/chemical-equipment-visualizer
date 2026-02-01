import React, { useState } from 'react';
import { login, register } from '../services/auth';
import '../App.css';

function Login({ onLoginSuccess }) {
  const [isSignup, setIsSignup] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isSignup) {
        if (password !== confirmPassword) {
          throw new Error('Passwords do not match');
        }
        await register(username, password, email);
      } else {
        await login(username, password);
      }
      onLoginSuccess();
    } catch (err) {
      const msg = err.response?.data?.error || err.response?.data?.username || err.message || 'Authentication failed. Please try again.';
      setError(Array.isArray(msg) ? msg[0] : msg);
    } finally {
      setLoading(false);
    }
  };

  const toggleMode = (e) => {
    e.preventDefault();
    setIsSignup(!isSignup);
    setError('');
    setPassword('');
    setConfirmPassword('');
  };

  return (
    <div className="login-scroll-container">
      <div className="login-page">
        {/* Left Side: Illustrative/Branding Area */}
        <div className="login-graphic">
          <div className="graphic-content">
            <img src={require('../assets/logo.svg').default} alt="Logo" className="graphic-logo" />
            <h2>Industrial Analytics <br /> Redefined</h2>
            <p> Visualize flowrates, pressures, and temperatures with precision.</p>
          </div>
          <div className="graphic-overlay"></div>
        </div>

        {/* Right Side: Login Form */}
        <div className="login-form-container">
          <div className="login-card">

            <div className="mobile-header">
              <img src={require('../assets/logo.svg').default} alt="Logo" className="mobile-logo" />
            </div>

            <div className="form-header">
              <div className="form-logo-container">
                <img src={require('../assets/logo.svg').default} alt="Logo" className="form-logo" />
              </div>
              <h1>Chemical Equipment Visualizer</h1>
              <p className="subtitle">{isSignup ? 'Create an account to get started' : 'Login to access your dashboard'}</p>
            </div>

            <form onSubmit={handleSubmit} className="login-form">
              <div className="form-group">
                <label htmlFor="username">Username</label>
                <input
                  type="text"
                  id="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Enter your username"
                  required
                  autoFocus
                />
              </div>

              {isSignup && (
                <div className="form-group">
                  <label htmlFor="email">Email Address</label>
                  <input
                    type="email"
                    id="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="name@company.com"
                  />
                </div>
              )}

              <div className="form-group">
                <label htmlFor="password">Password</label>
                <input
                  type="password"
                  id="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  required
                />
              </div>

              {isSignup && (
                <div className="form-group">
                  <label htmlFor="confirmPassword">Confirm Password</label>
                  <input
                    type="password"
                    id="confirmPassword"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="••••••••"
                    required
                  />
                </div>
              )}

              {error && <div className="error-alert">⚠️ {error}</div>}

              <button type="submit" className="btn-primary" disabled={loading}>
                {loading ? 'Processing...' : (isSignup ? 'Create Account' : 'Sign in')}
              </button>
            </form>

            <div className="login-footer">
              <p>
                {isSignup ? 'Already have an account? ' : 'Don\'t have an account? '}
                <button
                  onClick={toggleMode}
                  className="toggle-link"
                >
                  {isSignup ? 'Sign in' : 'Sign up'}
                </button>
              </p>
              {!isSignup && <div className="demo-badge">Demo: trial12 / Trial@1234</div>}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
