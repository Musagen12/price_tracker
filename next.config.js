/** @type {import('next').NextConfig} */
const nextConfig = {
    images: {
      domains: [
        'm.media-amazon.com', // Amazon image domain
        'ke.jumia.is',        // Jumia image domain
        'jumia.co.ke',        // Another Jumia domain if needed
      ],
    },
  }
  
  module.exports = nextConfig;
  