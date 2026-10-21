# Security Policy

## Reporting a Vulnerability

If you discover a security issue in any of the shell scripts, Python SDK examples, hook templates, or MCP configurations in **gemini-howto**, please report it responsibly before disclosing it publicly.

### What Qualifies as a Security Issue in This Repository

1. **Hook Script Command Injection (`06-hooks/`)**: Unquoted shell variable expansion or unsafe `eval` of untrusted `toolInput` fields from stdin JSON.
2. **Overly Permissive Default Templates (`05-mcp/`, `09-advanced-features/`)**: Configurations that unintentionally disable the OS Terminal Sandbox (`unsandboxed(*)`) or expose credentials in plaintext.
3. **Path Traversal in Helper Scripts (`03-skills/`, `10-cli/`)**: Scripts that write outside the workspace without validation.

### Best Practices Enforced in All Templates

- All bash hook scripts parse stdin JSON strictly using `jq` rather than regex/grep over raw JSON strings.
- All MCP configurations use `${ENV_VAR}` interpolation or `~/.gemini/.env` rather than hardcoded tokens.
- Permission examples follow the **Deny > Ask > Allow** precedence model with OS Seatbelt / `nsjail` / `AppContainer` sandboxing enabled by default.
