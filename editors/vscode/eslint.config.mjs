import { defineConfig } from "eslint/config";
import eslintConfigPrettier from "eslint-config-prettier";
import checkFile from "eslint-plugin-check-file";
import tseslint from "typescript-eslint";

const CHECK_FILE_OPTIONS = { ignoreMiddleExtensions: true };

export default defineConfig(
  {
    ignores: ["out/**"],
  },
  {
    extends: [
      tseslint.configs.recommended,
      tseslint.configs.recommendedTypeChecked,
    ],
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
      ...eslintConfigPrettier.rules,
    },
  },
  {
    files: ["src/main/**/*.ts", "src/test/**/*.ts"],
    plugins: {
      "check-file": checkFile,
    },
    rules: {
      "check-file/folder-naming-convention": [
        "error",
        {
          "src/{main,test}/**/": "FLAT_CASE",
        },
      ],
      "check-file/filename-naming-convention": [
        "error",
        {
          "**/extension.ts": "FLAT_CASE",
          "src/test/**/*.test.ts": "PASCAL_CASE",
          "src/**/!(extension).ts": "PASCAL_CASE",
        },
        CHECK_FILE_OPTIONS,
      ],
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
