import React, { createContext, useState, useEffect, useContext } from 'react';
import api from '../utils/api';
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkUser = async () => {
            const access = localStorage.getItem('access_token');
            if (access) {
                try {
                    const decoded = jwtDecode(access);
                    const isExpired = decoded.exp * 1000 < Date.now();

                    if (!isExpired) {
                        setUser({ id: decoded.user_id });
                    } else {
                        // Need to implement refresh token logic here eventually, but for now clear token
                        logout();
                    }
                } catch (error) {
                    logout();
                }
            }
            setLoading(false);
        };

        checkUser();
    }, []);

    const login = async (username, password) => {
        try {
            const response = await api.post('/api/token/', { username, password });
            localStorage.setItem('access_token', response.data.access);
            localStorage.setItem('refresh_token', response.data.refresh);
            const decoded = jwtDecode(response.data.access);
            setUser({ id: decoded.user_id });
            return { success: true };
        } catch (error) {
            return {
                success: false,
                message: error.response?.data?.detail || 'Error al iniciar sesión'
            };
        }
    };

    const logout = () => {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        setUser(null);
    };

    const value = {
        user,
        login,
        logout,
        loading
    };

    return (
        <AuthContext.Provider value={value}>
            {!loading && children}
        </AuthContext.Provider>
    );
};
