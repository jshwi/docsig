import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const THRESHOLD = 100;
const here = dirname(fileURLToPath(import.meta.url));
const summaryPath = join(here, "../coverage/coverage-summary.json");

let summary;
try {
  summary = JSON.parse(readFileSync(summaryPath, "utf8"));
} catch {
  console.error(`missing coverage summary at ${summaryPath}`);
  process.exit(1);
}

const lines = summary.total?.lines?.pct;
if (typeof lines !== "number" || lines < THRESHOLD) {
  const pct = typeof lines === "number" ? lines : "unknown";
  console.error(`line coverage ${pct}% is below the ${THRESHOLD}% threshold`);
  process.exit(1);
}

console.log(`line coverage ${lines}% meets the ${THRESHOLD}% threshold`);
