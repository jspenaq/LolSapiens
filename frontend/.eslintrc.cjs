module.exports = {
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: ["plugin:react/recommended", "standard-with-typescript", "prettier"],
  overrides: [],
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
    project: ["tsconfig.json"],
    tsconfigRootDir: __dirname,
    jsx: true,
  },
  plugins: ["react"],
  settings: {
    react: {
      version: "detect",
    },
  },
  rules: {
    "react/react-in-jsx-scope": "off",
    "@typescript-eslint/no-floating-promises": "off",
    "@typescript-eslint/consistent-type-imports": [
      "error",
      {
        prefer: "type-imports",
      },
    ],
    "@typescript-eslint/strict-boolean-expressions": "off",
    "@typescript-eslint/naming-convention": [
      "error",
      {
        selector: ["variable"],
        format: ["snake_case", "camelCase", "UPPER_CASE", "PascalCase"],
      },
    ],
  },
};
