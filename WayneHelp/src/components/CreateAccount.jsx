import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { UserContext } from "../UserContext";
import "./CreateAccount.css";

const CreateAccount = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("student");
  const { setUser } = useContext(UserContext);
  const navigate = useNavigate();

  // const handleCreateAccount = (e) => {
  //   e.preventDefault();
  //   setUser({ username, password, email });
  //   navigate("/student-login");
  // };

  const handleCreateAccount = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          username: "testuser",
          email: "testuser@example.com",
          password: "securepassword",
          role: "student",
        }),
      });

      const data = await response.json();
      if (response.ok) {
        alert("Registration successful, please login");
        // localStorage.setItem("token", data.access_token);
        // localStorage.setItem("role", data.role);
        window.location.href = "/signin";
      } else {
        alert(data.error);
      }
    } catch (error) {
      console.error("Error registering:", error);
    }
  };

  return (
    <div className="create-account-container">
      <header>
        <h1>Create Account</h1>
      </header>
      <div className="create-account-box">
        <h2>Welcome to Wayne Help</h2>
        <form onSubmit={handleCreateAccount}>
          <div className="input-container">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              placeholder="Enter your username"
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="input-container">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <div className="input-container">
            <label htmlFor="email">Email</label>
            <input
              type="email"
              id="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <select value={role} onChange={(e) => setRole(e.target.value)}>
            <option value="student">Student</option>
            <option value="professional">Professional</option>
          </select>
          <button className="create-account-button" type="submit">
            Create Account
          </button>
        </form>
      </div>
    </div>
  );
};

export default CreateAccount;
