module.exports = {
  packagerConfig: {
    extraResource: ["../frontend/dist"],
    icon:
      process.platform === "darwin"
        ? "assets/logo_darwin.icns"
        : "assets/logo.ico",
    name: "LolSapiens",
  },
  rebuildConfig: {},
  makers: [
    {
      name: "@electron-forge/maker-zip",
      platforms: ["win32", "darwin"],
    },
  ],
};
