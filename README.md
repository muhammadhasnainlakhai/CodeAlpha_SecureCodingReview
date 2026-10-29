# CodeAlpha_SecureCodingReview

Secure coding review of a small Flask web application. The app was audited using the static analysis tool **Bandit** and manual code inspection. Vulnerabilities were documented and fixed.

## Files

- `vulnerable_app.py` - original app with security flaws (for audit only, do not deploy)
- `fixed_app.py` - remediated version
- `bandit_report_before.txt` - Bandit scan of the vulnerable app
- `bandit_report_after.txt` - Bandit scan of the fixed app

## Scan Results

| Severity | Before | After |
|----------|--------|-------|
| High     | 4      | 0     |
| Medium   | 3      | 0     |
| Low      | 1      | 3     |

The 3 remaining Low findings are warnings about the `subprocess` module. The call uses a list (no `shell=True`), the input is validated with a strict regex, and a timeout is set, so they are accepted residual risk.

## Findings and Remediation

| # | Vulnerability | Location | Detected by | Fix |
|---|---------------|----------|-------------|-----|
| 1 | SQL Injection | /register, /login | Bandit (B608) | Parameterized queries |
| 2 | Command Injection | /ping | Bandit (B605) | subprocess with list args + input validation |
| 3 | Weak hashing (MD5) | Password storage | Bandit (B324) | Salted hashing (werkzeug) |
| 4 | Hardcoded secret | SECRET_KEY | Bandit (B105) | Environment variable / random key |
| 5 | Debug mode enabled | app.run | Bandit (B201) | debug=False |
| 6 | Binding to 0.0.0.0 | app.run | Bandit (B104) | Bind to 127.0.0.1 |
| 7 | Cross-Site Scripting (XSS) | /hello | Manual review only | Output escaping |

Note: Bandit did not detect the XSS issue. It was found by manual inspection, which shows why static tools and manual review should be used together.

## Tools Used

- Bandit (static analysis)
- Manual code review

## Secure Coding Best Practices

- Never build SQL queries with string formatting
- Validate and sanitize all user input
- Never pass user input to shell commands
- Hash passwords with a strong, salted algorithm
- Keep secrets out of source code
- Disable debug mode in production
- Escape output to prevent XSS
- Keep dependencies updated

## Disclaimer

For educational purposes only. Do not deploy `vulnerable_app.py`.

## Author

Muhammad Hasnain Lakhai - CodeAlpha Cyber Security Internship
