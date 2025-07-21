import { promises as fs } from "fs";

export const runtime = "nodejs"; // This is a Node.js environment

export async function GET() {
  try {
    const response = await fs.readFile(
      process.cwd() + "/app/api/json/anar.json",
      "utf-8"
    );

    console.log(response);

    // Simulate a fetch request to read the JSON file
    // If you are using a different path or method to fetch the data, adjust accordingly
    // For example, if you are using a fetch API, it would look like this:
    const data = JSON.parse(response);
    return new Response(JSON.stringify(data), {
      headers: { "Content-Type": "application/json" },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: (error as Error).message }), {
      status: 500,
      headers: { "Content-Type": "application/json" },
    });
  }
}
