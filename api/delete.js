/**
 * MCP Admin API - Delete a news post from GitHub
 */

const https = require("https");

const GITHUB_TOKEN = process.env.GITHUB_TOKEN;
const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD;
const REPO = "mcottojr-design/MCP-WEBSITE";
const BRANCH = "main";

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
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  const token = (req.headers.authorization || "").replace("Bearer ", "");
  if (!ADMIN_PASSWORD || token !== ADMIN_PASSWORD) {
    return res.status(401).json({ error: "Unauthorized" });
  }

  const { path, sha } = req.body;
  if (!path || !sha) return res.status(400).json({ error: "path and sha are required" });

  // Safety: only allow deleting from src/news/ or src/drafts/
  if (!path.startsWith("src/news/") && !path.startsWith("src/drafts/")) {
    return res.status(403).json({ error: "Can only delete from news or drafts folders" });
  }

  const result = await githubRequest("DELETE", `/repos/${REPO}/contents/${path}`, {
    message: `🗑️ Delete post: ${path.split("/").pop()}`,
    sha,
    branch: BRANCH,
  });

  if (result.status === 200) {
    return res.status(200).json({ success: true, message: "Post deleted. Site will rebuild in ~1 minute." });
  }

  return res.status(500).json({ error: "Delete failed", details: result.body });
};
