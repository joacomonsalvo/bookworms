import { defineConfig } from "vite";

export default defineConfig({
  server: {
    // en producción el flag 'true' permite cualquier host
    allowedHosts: true,
  },
  preview: {
    allowedHosts: true,
  },
});
