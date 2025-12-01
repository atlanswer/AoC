import { getInput } from "aoc";

async function main() {
//   const input = `L68
// L30
// R48
// L5
// R60
// L55
// L1
// L99
// R14
// L82
// `;
  const input = await getInput(import.meta.dir);

  let dial = 50;
  let passwd = 0;

  for (const line of input.trim().split("\n")) {
    const direction = line.substring(0, 1);
    const distance = parseInt(line.substring(1));
    // console.debug(`${direction}, ${distance}`);

    dial = direction === "L" ? dial - distance : dial + distance;
    dial = ((dial % 100) + 100) % 100;
    // console.debug(dial);

    if (dial === 0) passwd += 1;
  }

  console.debug(`passwd: ${passwd}`);
}

const tStart = performance.now();
await main();
const tEnd = performance.now();
console.debug(`Execution time: ${(tEnd - tStart).toFixed(3)} ms.`);
