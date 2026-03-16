/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: { typedRoutes: true },
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://nbgi.onrender.com/api/:path*',
      },
      {
        source: '/docs',
        destination: 'https://nbgi.onrender.com/docs',
      },
      {
        source: '/docs/:path*',
        destination: 'https://nbgi.onrender.com/docs/:path*',
      },
      {
        source: '/redoc',
        destination: 'https://nbgi.onrender.com/redoc',
      },
      {
        source: '/openapi.json',
        destination: 'https://nbgi.onrender.com/openapi.json',
      },
      {
        source: '/api/v1/openapi.json',
        destination: 'https://nbgi.onrender.com/openapi.json',
      },
      {
        source: '/docs/oauth2-redirect',
        destination: 'https://nbgi.onrender.com/docs/oauth2-redirect',
      },
    ];
  },
};

module.exports = nextConfig;
