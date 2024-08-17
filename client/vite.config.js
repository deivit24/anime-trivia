export default {
  server: {
    host: "0.0.0.0", // Listen on all network interfaces
    port: 8080, // Ensure the port matches your Docker setup
    strictPort: true, // Fail if the port is already in use
    open: false, // Open browser default false
    cors: true, // Cross domain settings allow
  },
};
