import js from '@eslint/js';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  {ignores: ['node_modules/**', 'build/**', 'out/**', 'work/**']},
  js.configs.recommended,
  ...tseslint.configs.recommended,
);
