import path from "node:path";

const aocDay = path.basename(import.meta.dir);
const basePath = path.resolve(import.meta.dir, "../..");
const inputPath = path.resolve(basePath, "input", aocDay, "input.txt");

const inputFile = Bun.file(inputPath);
const inputText = (await inputFile.text()).trim().split("\n");

function toSorted(arr: number[], next: number): number[] {
    if (arr.length === 0) {
        arr.push(next);
        return arr;
    }

    let i = 0;

    while (i < arr.length) {
        if (arr[i] <= next) {
            i += 1;
        } else {
            break;
        }
    }

    arr.splice(i, 0, next);

    return arr;
}

let left: number[] = [];
let right: number[] = [];

for (const line of inputText) {
    const [ln, rn] = line.split(/\s+/);
    left = toSorted(left, parseInt(ln));
    right = toSorted(right, parseInt(rn));
}

let res = 0;

for (let i = 0; i < inputText.length; i += 1) {
    res += Math.abs(left[i] - right[i]);
}

console.log(`Result: ${res}`);

