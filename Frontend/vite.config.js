import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [
    tailwindcss(),
    react()
  ],
  server: {
    allowedHosts: ['fabf-27-7-50-101.ngrok-free.app'],   // Accept connections from any IP (including Ngrok)
    port: 5173,          // Optional: match your current port
    strictPort: true,    // Ensures it doesn't fallback to another port
    cors: true           // Allow cross-origin requests
  }
});
