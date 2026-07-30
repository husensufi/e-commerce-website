import { API_URL } from "@/api";


const TOKEN_KEY = import.meta.env.VITE_TOKEN_KEY || "user_token";


export class AuthService {
    async login(data = {}) {
        const response = await fetch(`${API_URL}/auth/login`, {
            method: "POST",
            body: JSON.stringify(data),   // ✅ serialize to JSON string
            headers: {
                "Content-Type": "application/json",
            },
        }).then(res => res.json());

        if (response.access_token) {
            localStorage.setItem(TOKEN_KEY, response.access_token);
        }

        return response;
    }

    async signup(data = {}) {
        const response = await fetch(`${API_URL}/auth/signup`, {
            method: "POST",
            body: JSON.stringify(data),   // ✅ serialize to JSON string
            headers: {
                "Content-Type": "application/json",
            },
        }).then(res => res.json());

        return response;
    }

    logout() {
        localStorage.removeItem(TOKEN_KEY);
    }

    saveUser(user = undefined) {
        if (!user) return;
        localStorage.setItem(TOKEN_KEY, JSON.stringify(user));
    }

    getUser() {
        try {
            return JSON.parse(localStorage.getItem(TOKEN_KEY));
        } catch (err) {
            return {};
        }
    }

    isLoggedIn() {
        return !!localStorage.getItem(TOKEN_KEY);
    }
}


export const authService = new AuthService();