/**
 * Vercel Serverless OAuth Proxy for Decap CMS / GitHub
 * 
 * Handles the GitHub OAuth flow:
 *   GET  /api/auth          → redirect to GitHub login
 *   GET  /api/auth?code=... → exchange code for token, return to CMS
 */

const https = require("https");

const CLIENT_ID = process.env.GITHUB_OAUTH_CLIENT_ID;
const CLIENT_SECRET = process.env.GITHUB_OAUTH_CLIENT_SECRET;
const REDIRECT_URI = process.env.GITHUB_OAUTH_REDIRECT_URI ||
  "https://mcp-website-dun.vercel.app/api/auth";

// Utility: POST JSON to GitHub token endpoint
function exchangeCodeForToken(code) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
      code,
      redirect_uri: REDIRECT_URI,
    });

    const options = {
      hostname: "github.com",
      path: "/login/oauth/access_token",
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
        "Content-Length": Buffer.byteLength(body),
      },
    };

    const req = https.request(options, (res) => {
      let data = "";
      res.on("data", (chunk) => (data += chunk));
      res.on("end", () => {
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error("Failed to parse GitHub response"));
        }
      });
    });

    req.on("error", reject);
    req.write(body);
    req.end();
  });
}

// The HTML page that sends the token back to the CMS window
function buildSuccessPage(token, provider = "github") {
  const message = JSON.stringify({
    token,
    provider,
  });

  return `<!DOCTYPE html>
<html>
<body>
<script>
  (function() {
    function receiveMessage(e) {
      console.log("receiveMessage", e);
      window.opener.postMessage(
        'authorization:${`github`}:success:${`{"token":"${token}","provider":"github"}`}',
        e.origin
      );
    }
    window.addEventListener("message", receiveMessage, false);
    window.opener.postMessage("authorizing:github", "*");
  })()
</script>
</body>
</html>`;
}

function buildErrorPage(message) {
  return `<!DOCTYPE html>
<html>
<body>
<script>
  window.opener.postMessage('authorization:github:error:${message}', '*');
</script>
</body>
</html>`;
}

module.exports = async function handler(req, res) {
  const { code, error } = req.query;

  // Step 1: No code yet — redirect to GitHub OAuth login
  if (!code && !error) {
    const params = new URLSearchParams({
      client_id: CLIENT_ID,
      redirect_uri: REDIRECT_URI,
      scope: "repo,user",
    });

    return res.redirect(`https://github.com/login/oauth/authorize?${params}`);
  }

  // Handle errors from GitHub
  if (error) {
    res.setHeader("Content-Type", "text/html");
    return res.send(buildErrorPage(error));
  }

  // Step 2: Exchange the code for a token
  try {
    const data = await exchangeCodeForToken(code);

    if (data.error || !data.access_token) {
      res.setHeader("Content-Type", "text/html");
      return res.send(buildErrorPage(data.error || "No access token received"));
    }

    res.setHeader("Content-Type", "text/html");
    return res.send(buildSuccessPage(data.access_token));
  } catch (err) {
    res.setHeader("Content-Type", "text/html");
    return res.send(buildErrorPage(err.message));
  }
};
