export function zip(...arrays: unknown[][]): unknown[][] {
  if (arrays?.length === 0) return [];

  const minLength = Math.max(...arrays.map((arr) => arr?.length));
  const zipped: unknown[][] = Array.from({ length: minLength }, () => []);

  for (let i = 0; i < minLength; i++) {
    for (const array of arrays) {
      zipped[i].push(array[i]);
    }
  }

  return zipped;
}
