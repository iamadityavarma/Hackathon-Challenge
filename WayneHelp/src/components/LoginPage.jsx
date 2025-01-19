import React from 'react'
import {useNavigate} from 'react-router-dom'
import './LoginPage.css'

const LoginPage = () => {
    const navigate = useNavigate()
    return (
        <div className='login-container'>
            <h1>Login Page</h1>
            <div className="button-container" onClick={() => navigate('/student-login')}>
                <button className="login-button">
                    Student Login
                </button>
                <button className="login-button">
                    Health Expert Login
                </button>
            </div>
        </div>
    )
}

export default LoginPage