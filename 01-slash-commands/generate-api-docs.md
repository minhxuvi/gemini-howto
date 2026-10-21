---
name: generate-api-docs
description: >-
  Inspect route handlers, controllers, DTOs, and validation schemas to generate OpenAPI 3.1
  specifications and developer-friendly Markdown API documentation with runnable examples.
  Use when the user runs /generate-api-docs or asks to document REST, GraphQL, or gRPC endpoints.
---

# API Documentation & OpenAPI 3.1 Generator (`/generate-api-docs`)

Use this skill when invoked via `/generate-api-docs [target-path]` or when the user asks to generate or update API reference documentation from source code.

## Usage Examples

```text
/generate-api-docs src/routes/
/generate-api-docs --openapi docs/openapi.yaml
/generate-api-docs services/billing/handlers.go
```

---

## Step-by-Step Agent Instructions

### Step 1: Discover Endpoints, Schemas & Middleware
1. **Locate Route Definitions**:
   - Scan the target directory (or workspace) for framework routers: Express/Fastify/Hono/Next.js App Router (`route.ts`), FastAPI/Flask (`@app.get`, `@router.post`), Go (`chi`, `gin`, `net/http`), or Spring/Rust (`axum`, `actix`).
2. **Extract Request & Response Contracts**:
   - Inspect validation schemas (`Zod`, `TypeBox`, `Pydantic`, `Joi`, Go struct tags, or Protobuf messages) to determine exact field types, required vs. optional properties, constraints, and default values.
3. **Trace Authentication & Error Paths**:
   - Identify auth middleware (`Bearer` JWT, API keys, OAuth2 scopes, session cookies) and all explicit HTTP status codes returned by the handler and error middleware (`400`, `401`, `403`, `404`, `409`, `422`, `429`, `500`).

### Step 2: Generate or Update OpenAPI 3.1 Specification (Optional / When Requested)
If the project maintains an `openapi.yaml` / `openapi.json` file (or the user requested `--openapi`), generate a valid **OpenAPI 3.1.0** document including:
- `info`, `servers`, and `securitySchemes`
- Reusable `components.schemas` mapped directly from the code's validation types
- Exact `paths` entries with `operationId`, `summary`, `parameters`, `requestBody`, and typed `responses`

### Step 3: Generate Markdown Endpoint Reference
For each endpoint, produce clear, copy-pasteable documentation following this structure:

````markdown
## `POST /api/v1/orders`

Creates a new customer order and reserves inventory atomically.

- **Authentication**: Required (`Authorization: Bearer <token>`, scope: `orders:write`)
- **Idempotency**: Supports `Idempotency-Key` request header (24h TTL)
- **Source**: [`src/routes/orders.ts`](../src/routes/orders.ts)

### Request Headers & Parameters

| Name | In | Type | Required | Description |
| :--- | :--- | :--- | :--- | :--- |
| `Idempotency-Key` | `header` | `string (uuid)` | No | Unique key to safely retry order creation |

### Request Body (`application/json`)

| Field | Type | Required | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `customerId` | `string` | Yes | `^cus_[a-zA-Z0-9]+$` | Unique customer identifier |
| `items` | `Array<OrderItem>` | Yes | `minItems: 1, maxItems: 50` | Line items to purchase |
| `currency` | `"USD" \| "EUR" \| "GBP"` | No | Default: `"USD"` | ISO 4217 3-letter currency code |

### Responses

#### `201 Created`
```json
{
  "id": "ord_9f8e7d6c5b",
  "status": "pending_payment",
  "totalCents": 4500,
  "currency": "USD",
  "createdAt": "2026-10-21T08:30:00Z"
}
```

#### Error Responses

| Status | Error Code | When Triggered |
| :--- | :--- | :--- |
| `400 Bad Request` | `VALIDATION_ERROR` | Missing required fields or invalid `items` array |
| `409 Conflict` | `INSUFFICIENT_INVENTORY` | One or more SKU quantities are out of stock |
| `429 Too Many Requests` | `RATE_LIMIT_EXCEEDED` | Exceeded 60 write requests per minute |

### Runnable Code Examples

**cURL**
```bash
curl -X POST "https://api.example.com/api/v1/orders" \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000" \
  -H "Content-Type: application/json" \
  -d '{"customerId": "cus_12345", "items": [{"sku": "SKU-01", "quantity": 2}]}'
```
````

### Step 4: Verification
1. Cross-check every documented field name, type, and status code against the actual source file to guarantee zero hallucinated parameters.
2. If an OpenAPI validator (`npx @redocly/cli lint` or `spectral lint`) is available in the workspace, run it to verify spec compliance.

---

| Previous Module | Module Home | Next Module |
| :--- | :---: | ---: |
| [🏠 Repository Root](../README.md) | [Module 01: Slash Commands](./README.md) | [Module 02: Rules & Persistent Memory →](../02-memory/README.md) |
