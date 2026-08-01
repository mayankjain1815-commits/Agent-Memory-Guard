-- PyPI BigQuery Analysis for Agent Memory Guard
-- Dataset: bigquery-public-data.pypi.file_downloads
-- Run in Google BigQuery console: https://console.cloud.google.com/bigquery
--
-- This gives you granular download data that pypistats.org doesn't expose:
-- - Downloads by country
-- - Downloads by Python version
-- - Downloads by installer (pip vs poetry vs uv)
-- - Downloads by CI vs human (system name)

-- 1. Total downloads by day (last 30 days)
SELECT
  DATE(timestamp) as download_date,
  COUNT(*) as downloads,
  COUNT(DISTINCT country_code) as countries
FROM `bigquery-public-data.pypi.file_downloads`
WHERE file.project = 'agent-memory-guard'
  AND DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY download_date
ORDER BY download_date DESC;

-- 2. Downloads by country (identify your markets)
SELECT
  country_code,
  COUNT(*) as downloads,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as pct
FROM `bigquery-public-data.pypi.file_downloads`
WHERE file.project = 'agent-memory-guard'
  AND DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
GROUP BY country_code
ORDER BY downloads DESC
LIMIT 20;

-- 3. Downloads by Python version (are users on modern Python?)
SELECT
  details.python as python_version,
  COUNT(*) as downloads
FROM `bigquery-public-data.pypi.file_downloads`
WHERE file.project = 'agent-memory-guard'
  AND DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
GROUP BY python_version
ORDER BY downloads DESC
LIMIT 10;

-- 4. Downloads by installer (pip vs poetry vs uv vs conda)
SELECT
  details.installer.name as installer,
  COUNT(*) as downloads
FROM `bigquery-public-data.pypi.file_downloads`
WHERE file.project = 'agent-memory-guard'
  AND DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
GROUP BY installer
ORDER BY downloads DESC;

-- 5. CI vs Human detection (Linux + pip + specific versions = likely CI)
SELECT
  CASE
    WHEN details.system.name = 'Linux' AND details.installer.name = 'pip' THEN 'Likely CI'
    WHEN details.system.name IN ('Darwin', 'Windows') THEN 'Likely Human'
    ELSE 'Unknown'
  END as user_type,
  COUNT(*) as downloads,
  ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 1) as pct
FROM `bigquery-public-data.pypi.file_downloads`
WHERE file.project = 'agent-memory-guard'
  AND DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
GROUP BY user_type
ORDER BY downloads DESC;

-- 6. Downloads by package version (are users on latest?)
SELECT
  file.version,
  COUNT(*) as downloads,
  MIN(DATE(timestamp)) as first_seen,
  MAX(DATE(timestamp)) as last_seen
FROM `bigquery-public-data.pypi.file_downloads`
WHERE file.project = 'agent-memory-guard'
  AND DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 90 DAY)
GROUP BY file.version
ORDER BY downloads DESC;

-- 7. Also check langchain-agent-memory-guard
SELECT
  DATE(timestamp) as download_date,
  COUNT(*) as downloads
FROM `bigquery-public-data.pypi.file_downloads`
WHERE file.project = 'langchain-agent-memory-guard'
  AND DATE(timestamp) >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
GROUP BY download_date
ORDER BY download_date DESC;
