/**
 * MCP Admin API - Publish or draft a news post to GitHub
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

function slugify(text) {
  return text.toLowerCase()
    .normalize("NFD").replace(/[\u0300-\u036f]/g, "")
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .trim();
}

module.exports = async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type, Authorization");

  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  // Auth check
  const token = (req.headers.authorization || "").replace("Bearer ", "");
  if (!ADMIN_PASSWORD || token !== ADMIN_PASSWORD) {
    return res.status(401).json({ error: "Unauthorized" });
  }

  const { title, date, author, category, image, image_focus, excerpt, body, draft } = req.body;
  if (!title || !body) return res.status(400).json({ error: "Title and body are required" });

  const postDate = date || new Date().toISOString().slice(0, 10);
  const slug = slugify(title);
  const filename = `${postDate}-${slug}.md`;
  const folder = draft ? "src/drafts" : "src/news";
  const filePath = `${folder}/${filename}`;
  const tags = draft ? "draft" : "post";

  const markdown = `---
layout: layouts/post.njk
tags: ${tags}
title: "${title.replace(/"/g, '\\"')}"
date: ${postDate}
author: "${author || "MCP Staff"}"
image: "${image || ""}"
image_focus: "${image_focus || "50% 50%"}"
category: "${category || "Announcement"}"
excerpt: "${(excerpt || "").replace(/"/g, '\\"')}"
---
${body}`;

  const encoded = Buffer.from(markdown).toString("base64");

  // Check if file already exists (to get SHA for update)
  let sha;
  const existing = await githubRequest("GET", `/repos/${REPO}/contents/${filePath}?ref=${BRANCH}`);
  if (existing.status === 200) sha = existing.body.sha;

  // Create or update file
  const commitBody = {
    message: `${draft ? "💾 Draft" : "📰 Publish"}: ${title}`,
    content: encoded,
    branch: BRANCH,
    ...(sha && { sha }),
  };

  const result = await githubRequest("PUT", `/repos/${REPO}/contents/${filePath}`, commitBody);

  if (result.status === 200 || result.status === 201) {
    return res.status(200).json({
      success: true,
      draft,
      path: filePath,
      url: draft ? null : `/news/${postDate}-${slug}`,
      message: draft ? "Draft saved!" : "Post published! Vercel will rebuild in ~1 minute.",
    });
  }

  return res.status(500).json({ error: "GitHub commit failed", details: result.body });
};
