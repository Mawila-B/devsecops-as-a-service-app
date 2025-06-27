import { useState } from "react";

export default function Home() {
  const [repoUrl, setRepoUrl] = useState("");
  const [file, setFile] = useState(null);
  const [scanId, setScanId] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!repoUrl && !file) {
      alert("Please enter a repo URL or upload a ZIP file");
      return;
    }
    setLoading(true);
    const formData = new FormData();
    if (repoUrl) formData.append("repo_url", repoUrl);
    if (file) formData.append("file", file);

    try {
      const res = await fetch("/api/scan", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (res.ok) {
        setScanId(data.scan_id);
      } else {
        alert(data.detail || "Scan failed");
      }
    } catch (err) {
      alert("Error: " + err.message);
    }
    setLoading(false);
  }

  return (
    <main style={{ maxWidth: 600, margin: "auto", padding: 20 }}>
      <h1>DevSecOps Scan</h1>
      {!scanId ? (
        <form onSubmit={handleSubmit}>
          <label>
            GitHub Repo URL (optional):
            <input
              type="url"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              style={{ width: "100%", marginBottom: 10 }}
            />
          </label>
          <label>
            Or upload ZIP file (optional):
            <input
              type="file"
              accept=".zip"
              onChange={(e) => setFile(e.target.files[0])}
              style={{ marginBottom: 10 }}
            />
          </label>
          <button type="submit" disabled={loading}>
            {loading ? "Scanning..." : "Start Scan"}
          </button>
        </form>
      ) : (
        <div>
          <h2>Scan started!</h2>
          <p>
            View your report{" "}
            <a href={`/api/report/${scanId}`} target="_blank" rel="noreferrer">
              here
            </a>
          </p>
          <button onClick={() => setScanId(null)}>Start New Scan</button>
        </div>
      )}
    </main>
  );
}
