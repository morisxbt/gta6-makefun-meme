import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const botDir = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';

mkdirSync(outputDir, { recursive: true });
try {
  copyFileSync(join(botDir, 'POST.json'), join(outputDir, 'POST.json'));
} catch (error) {
  const detail = error instanceof Error ? error.message : String(error);
  console.error(`Could not copy POST.json from ${botDir} to ${outputDir}: ${detail}`);
  process.exitCode = 1;
}
