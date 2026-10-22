// Pass one private stdin message to the unmodified official CLI in-process.
// Only public CLI flags are used; no credential or internal provider API access.
import { readFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const entry = new URL('../clients/node_modules/@moonshot-ai/kimi-code/dist/main.mjs', import.meta.url);
const agent = fileURLToPath(new URL('./kimi_text_agent.md', import.meta.url));
const prompt = JSON.parse(readFileSync(0, 'utf8'));
if (typeof prompt !== 'string' || !prompt.trim() || Buffer.byteLength(prompt, 'utf8') > 1048576 - 131072 - 4096) throw new Error('Prompt exceeds technical input envelope');
mkdirSync('empty-skills', { recursive: true });
process.argv = [process.execPath, fileURLToPath(entry), '--model', 'kimi-code/k3',
  '--agent-file', agent, '--skills-dir', 'empty-skills', '-p', prompt,
  '--output-format', 'stream-json'];
await import(entry.href);
