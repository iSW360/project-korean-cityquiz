import { defineConfig } from "@apps-in-toss/web-framework/config";

export default defineConfig({
  appName: "mapquiz",
  brand: {
    displayName: "지도퀴즈",
    primaryColor: "#E8B84B",
    icon: "https://mapquiz.co.kr/img/icon-512.png",
  },
  web: {
    host: "localhost",
    port: 5173,
    commands: {
      dev: "vite dev",
      build: "node scripts/build-dist.js",
    },
  },
  permissions: [],
  outdir: "dist",
});
