/// <reference types="vite/client" />
/// <reference types="vite-plugin-svgr/client" />

export {};

declare global {
  interface Window {
    electronApi: {
      importBuild: (data: any) => void;
      buildImported: (callback: () => void) => void;
    };
  }
}
