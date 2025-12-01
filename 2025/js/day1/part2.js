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
    const starts_at_0 = dial === 0;

    const direction = line.substring(0, 1);
    const distance = parseInt(line.substring(1));
    // console.debug(`${direction}, ${distance}`);

    dial = direction === "L" ? dial - distance : dial + distance;
    const cross = Math.floor(dial / 100);
    dial = ((dial % 100) + 100) % 100;
    const ends_at_0 = dial === 0;
    // console.debug(dial);

    if (cross === 0 && ends_at_0) passwd += 1;
    if (cross > 0) passwd += cross;
    if (cross < 0) {
      passwd += Math.abs(cross);
      if (starts_at_0) passwd -= 1;
      if (ends_at_0) passwd += 1;
    }
  }

  console.debug(`passwd: ${passwd}`);
}

const tStart = performance.now();
await main();
const tEnd = performance.now();
console.debug(`Execution time: ${(tEnd - tStart).toFixed(3)} ms.`);
