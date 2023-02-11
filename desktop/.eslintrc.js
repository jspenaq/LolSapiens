module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: ["standard-with-typescript", "prettier"],
  overrides: [],
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
    project: ["tsconfig.json"],
    tsconfigRootDir: __dirname,
  },
  rules: {
    "@typescript-eslint/no-floating-promises": "off",
  },
};
