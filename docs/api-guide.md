# DevSecOps API Guide

## Authentication
All API endpoints require authentication via API key. Include your API key in the `X-API-Key` header.

## Endpoints

### Start a Scan
`POST /scans/`

**Request Body:**
```json
{
  "target": "https://example.com",
  "scan_type": "web"
}