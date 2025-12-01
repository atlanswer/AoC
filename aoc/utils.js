import * as path from "node:path";

/** Read the input file as string with the current module path
 * @param {string} cur_dir
 * @returns {Promise<string>} input string
 * ```js
 * const input = await getInput(import.meta.dir)
 * ```
 */
export async function getInput(cur_dir) {
  const AOC_DAY = path.basename(cur_dir);
  const INPUT_PATH = path.resolve(
    cur_dir,
    "..",
    "..",
    "input",
    AOC_DAY,
    "input.txt",
  );
  const inputFile = Bun.file(INPUT_PATH);
  return inputFile.text();
}
