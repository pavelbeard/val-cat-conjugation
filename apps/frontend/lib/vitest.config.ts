import viteTsconfigPaths from 'vite-tsconfig-paths'
import { defineConfig } from 'vitest/config'

const folders = {
  unit: ['./app/**/*.test.ts'],
  staff: ['node_modules'],
}

export default defineConfig({
  plugins: [viteTsconfigPaths()],
  test: {
    projects: [
      {
        extends: true,
        test: {
          name: 'unit',
          include: folders.unit,
          exclude: folders.staff,
        },
      },
    ],
  },
})
