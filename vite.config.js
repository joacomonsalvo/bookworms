import { defineConfig } from "vite";

export default defineConfig({
  server: {
    allowedHosts: ["bookworms-66mj.onrender.com"],
  },
  preview: {
    allowedHosts: ["bookworms-66mj.onrender.com"],
  },
});
