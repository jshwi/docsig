import eslintConfigPrettier from "eslint-config-prettier";
import tseslint from "typescript-eslint";

// noinspection JSCheckFunctionSignatures
export default tseslint.config(
  {
    ignores: ["out/**"],
  },
  ...tseslint.configs.recommended,
  ...tseslint.configs.recommendedTypeChecked,
  eslintConfigPrettier,
  {
    languageOptions: {
      parserOptions: {
        projectService: true,
        tsconfigRootDir: import.meta.dirname,
      },
    },

    rules: {
      "@typescript-eslint/naming-convention": [
        "warn",
        {
          selector: "import",
          format: ["camelCase", "PascalCase"],
        },
      ],

      curly: "warn",
      eqeqeq: "warn",
      "no-throw-literal": "warn",
    },
  },
  {
    files: ["src/test/**/*.ts"],
    rules: {
      "@typescript-eslint/no-unused-vars": "error",
      "@typescript-eslint/require-await": "off",
    },
  },
);
