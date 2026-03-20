/**
 * MCP Admin API - List all published news posts
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

function parseFrontMatter(markdown) {
  const match = markdown.match(/^---\n([\s\S]*?)\n---/);
  if (!match) return {};
  const fm = {};
  match[1].split("\n").forEach((line) => {
    const [key, ...rest] = line.split(":");
    if (key && rest.length) fm[key.trim()] = rest.join(":").trim().replace(/^["']|["']$/g, "");
  });
  return fm;
}

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "GET") return res.status(405).json({ error: "Method not allowed" });

  const token = (req.headers.authorization || "").replace("Bearer ", "");
  if (!ADMIN_PASSWORD || token !== ADMIN_PASSWORD) {
    return res.status(401).json({ error: "Unauthorized" });
  }

  // List both published and draft folders
  const [newsRes, draftsRes] = await Promise.all([
    githubRequest("GET", `/repos/${REPO}/contents/src/news?ref=${BRANCH}`),
    githubRequest("GET", `/repos/${REPO}/contents/src/drafts?ref=${BRANCH}`),
  ]);

  const newsFiles = newsRes.status === 200 ? newsRes.body.filter((f) => f.name.endsWith(".md")) : [];
  const draftFiles = draftsRes.status === 200 ? draftsRes.body.filter((f) => f.name.endsWith(".md")) : [];

  // Fetch content in batches of 5 to avoid overloading
  async function batchFetch(files, isDraft) {
    const results = [];
    for (let i = 0; i < files.length; i += 5) {
      const batch = files.slice(i, i + 5);
      const fetched = await Promise.all(
        batch.map(async (file) => {
          try {
            const r = await githubRequest("GET", `/repos/${REPO}/contents/${file.path}?ref=${BRANCH}`);
            if (r.status === 200 && r.body.content) {
              const markdown = Buffer.from(r.body.content, "base64").toString("utf8");
              const fm = parseFrontMatter(markdown);
              return {
                name: file.name,
                path: file.path,
                sha: r.body.sha,
                title: fm.title || file.name.replace(".md", ""),
                date: fm.date || "",
                category: fm.category || "",
                featured: fm.featured === "true",
                image: fm.image || "",
                image_focus: fm.image_focus || "50% 50%",
                excerpt: fm.excerpt || "",
                gallery: fm.gallery || [],
                body: markdown.split("---").slice(2).join("---").trim(),
                draft: isDraft,
              };
            }
          } catch (e) {}
          return {
            name: file.name,
            path: file.path,
            sha: file.sha,
            title: file.name.replace(".md", ""),
            date: "",
            category: "",
            image: "",
            excerpt: "",
            draft: isDraft,
          };
        })
      );
      results.push(...fetched);
    }
    return results;
  }

  const [newsPosts, draftPosts] = await Promise.all([
    batchFetch(newsFiles, false),
    batchFetch(draftFiles, true),
  ]);

  const allPosts = [...newsPosts, ...draftPosts].sort((a, b) =>
    b.date.localeCompare(a.date)
  );

  return res.status(200).json({ posts: allPosts });
};
