// Exact known-record metadata only; no search, download or browser request.
import fs from "node:fs";
import path from "node:path";
import { pathToFileURL, fileURLToPath } from "node:url";
const runtime = process.env.NATURE_RUNTIME_DIR || path.dirname(fileURLToPath(import.meta.url));
const source = process.env.NATURE_SOURCE_DIR || path.join(path.dirname(runtime), "nature-skills");
const doi = process.argv[2];
if (!doi?.startsWith("10.") || !doi.includes("/")) throw new Error("Pass one existing project DOI");
const contact = JSON.parse(fs.readFileSync(path.join(runtime, "config", "contact.json"), "utf8"));
const { fetchCrossrefByDoi } = await import(pathToFileURL(path.join(source, "skills/nature-downloader/scripts/lib/metadata.mjs")));
const observations = [];
const report = { doi, requested_at_utc: new Date().toISOString(), search_executed: false,
  node_version: process.version, node_use_env_proxy: process.env.NODE_USE_ENV_PROXY === "1",
  proxy_variable_present: Boolean(process.env.HTTPS_PROXY || process.env.https_proxy),
  tls_verification_enabled: process.env.NODE_TLS_REJECT_UNAUTHORIZED !== "0", attempts: 1 };
try {
  const record = await fetchCrossrefByDoi(doi, {mailto: contact.contact_email, fetchImpl: async (url, options) => {
    const response = await fetch(url, options);
    observations.push({ host: new URL(url).hostname, path: new URL(url).pathname,
      http_status: response.status, response_host: new URL(response.url).hostname,
      response_date: response.headers.get("date"), content_type: response.headers.get("content-type") });
    return response;
  }});
  report.metadata_received = true;
  report.doi_matches = record.doi.toLowerCase() === doi.toLowerCase();
  report.returned_title = record.title;
} catch (error) {
  report.metadata_received = false;
  report.error_class = error.name;
  report.cause_class = error.cause?.name || null;
  // No raw exception output: nested transport errors can contain environment data.
}
report.http_observations = observations;
fs.writeFileSync(path.join(runtime, "node_network_validation.json"), JSON.stringify(report, null, 2) + "\n");
console.log(JSON.stringify(report, null, 2));
process.exitCode = report.metadata_received && report.doi_matches ? 0 : 1;
