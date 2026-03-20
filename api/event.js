const { Octokit } = require("@octokit/rest");

const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
const owner = "mcottojr-design";
const repo = "MCP-WEBSITE";

module.exports = async (req, res) => {
  if (req.method === "GET") {
    try {
      const { data } = await octokit.repos.getContent({
        owner,
        repo,
        path: "src/_data/event.json",
      });
      const content = Buffer.from(data.content, "base64").toString();
      return res.status(200).json(JSON.parse(content));
    } catch (err) {
      return res.status(500).json({ error: err.message });
    }
  }

  if (req.method === "POST") {
    const authHeader = req.headers.authorization;
    if (!authHeader || authHeader !== `Bearer ${process.env.ADMIN_PASSWORD}`) {
      return res.status(401).json({ error: "Unauthorized" });
    }

    const { title, date_display, location, image, ticket_link, watch_link } = req.body;
    const eventData = { title, date_display, location, image, ticket_link, watch_link };
    const content = JSON.stringify(eventData, null, 2);

    try {
      // Get current SHA
      let sha;
      try {
        const { data } = await octokit.repos.getContent({ owner, repo, path: "src/_data/event.json" });
        sha = data.sha;
      } catch (e) { /* file might not exist yet */ }

      await octokit.repos.createOrUpdateFileContents({
        owner,
        repo,
        path: "src/_data/event.json",
        message: "Update next event via admin dashboard",
        content: Buffer.from(content).toString("base64"),
        sha,
      });

      return res.status(200).json({ success: true, message: "Event updated successfully!" });
    } catch (err) {
      return res.status(500).json({ error: err.message });
    }
  }

  return res.status(405).json({ error: "Method not allowed" });
};
