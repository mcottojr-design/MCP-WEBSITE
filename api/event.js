/**
 * MCP Admin API - Get or update next event data in GitHub
 */

const https = require("https");

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD;
const REPO = "mcottojr-design/MCP-WEBSITE";
const BRANCH = "main";
const FILE_PATH = "src/_data/event.json";

function githubRequest(method, path, body) {
  return new Promise((resolve, reject) => {
    const data = body ? JSON.stringify(body) : null;
    const options = {
      hostname: "api.github.com",
      path,
      method,
      headers: {
        Authorization: `token ${GITHUB_TOKEN}`,
        "User-Agent": "MCP-Admin/1.0",
        Accept: "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        ...(data && { "Content-Length": Buffer.byteLength(data) }),
      },
    };
    const req = https.request(options, (res) => {
      let raw = "";
      res.on("data", (c) => (raw += c));
      res.on("end", () => {
        try { resolve({ status: res.statusCode, body: JSON.parse(raw) }); }
        catch { resolve({ status: res.statusCode, body: raw }); }
      });
    });
    req.on("error", reject);
    if (data) req.write(data);
    req.end();
  });
}

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

  if (req.method === "OPTIONS") return res.status(200).end();

  if (req.method === "GET") {
    try {
      const result = await githubRequest("GET", `/repos/${REPO}/contents/${FILE_PATH}?ref=${BRANCH}`);
      if (result.status === 200) {
        const content = Buffer.from(result.body.content, "base64").toString();
        return res.status(200).json(JSON.parse(content));
      }
      return res.status(result.status).json({ error: "File not found", details: result.body });
    } catch (err) {
      return res.status(500).json({ error: err.message });
    }
  }

  if (req.method === "POST") {
    const token = (req.headers.authorization || "").replace("Bearer ", "");
    if (!ADMIN_PASSWORD || token !== ADMIN_PASSWORD) {
      return res.status(401).json({ error: "Unauthorized" });
    }

    const { title, date_display, location, image, image_focus, ticket_link, watch_link } = req.body;
    const eventData = { title, date_display, location, image, image_focus, ticket_link, watch_link };
    const content = JSON.stringify(eventData, null, 2);
    const encoded = Buffer.from(content).toString("base64");

    try {
      // Get current SHA
      let sha;
      const existing = await githubRequest("GET", `/repos/${REPO}/contents/${FILE_PATH}?ref=${BRANCH}`);
      if (existing.status === 200) sha = existing.body.sha;

      const commitBody = {
        message: "Update next event via admin dashboard",
        content: encoded,
        branch: BRANCH,
        ...(sha && { sha }),
      };

      const result = await githubRequest("PUT", `/repos/${REPO}/contents/${FILE_PATH}`, commitBody);
      if (result.status === 200 || result.status === 201) {
        return res.status(200).json({ success: true, message: "Event updated!" });
      }
      return res.status(500).json({ error: "GitHub update failed", details: result.body });
    } catch (err) {
      return res.status(500).json({ error: err.message });
    }
  }

  return res.status(405).json({ error: "Method not allowed" });
};
