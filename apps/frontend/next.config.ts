import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  experimental: {
    devtoolSegmentExplorer: true,
    // browserDebugInfoInTerminal: true,
  },
};

export default nextConfig;
