import path from "node:path";

const aocDay = path.basename(import.meta.dir);
const basePath = path.resolve(import.meta.dir, "../..");
const inputPath = path.resolve(basePath, "input", aocDay, "input.txt");

const inputFile = Bun.file(inputPath);
const inputText = (await inputFile.text()).trim().split("\n");

let left: number[] = [];
let right: Map<number, number> = new Map();

for (const line of inputText) {
    const [l, r] = line.split(/\s+/);
    const ln = parseInt(l)
    const rn = parseInt(r)

    left.push(ln);
    right.set(rn, (right.get(rn) ?? 0) + 1)
}

let res = 0;

for (let i = 0; i < left.length; i += 1) {
    res += left[i] * (right.get(left[i]) ?? 0);
}

console.log(`Result: ${res}`);

