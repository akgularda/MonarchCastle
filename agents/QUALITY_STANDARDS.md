# Quality Standards & Gates
## Monarch Castle Technologies

> **Version**: 1.0.0
> **Owner**: MCT-QA-001
> **Review Cycle**: Monthly

---

## QUALITY PHILOSOPHY

```
                    "Quality is not an act, it is a habit."
                                    — Aristotle
                                    
    ┌─────────────────────────────────────────────────────────────┐
    │                                                             │
    │     MONARCH CASTLE QUALITY COMMITMENT                       │
    │                                                             │
    │     We ship software that:                                  │
    │     ✓ Works correctly the first time                        │
    │     ✓ Handles errors gracefully                             │
    │     ✓ Performs under load                                   │
    │     ✓ Remains secure against threats                        │
    │     ✓ Delights users with polish                            │
    │                                                             │
    │     We never ship:                                          │
    │     ✗ Untested code                                         │
    │     ✗ Known security vulnerabilities                        │
    │     ✗ Performance regressions                               │
    │     ✗ Broken accessibility                                  │
    │                                                             │
    └─────────────────────────────────────────────────────────────┘
```

---

## QUALITY GATES

### Gate 0: Pre-Commit
**Triggered**: Before code leaves developer's machine

```yaml
checks:
  - name: "lint"
    tool: "eslint/biome"
    blocking: true
    
  - name: "format"
    tool: "prettier/biome"
    blocking: true
    
  - name: "type_check"
    tool: "tsc"
    blocking: true
    
  - name: "unit_tests"
    tool: "vitest"
    blocking: true
    coverage_threshold: 80%
    
  - name: "secret_scan"
    tool: "gitleaks"
    blocking: true
```

### Gate 1: Pull Request
**Triggered**: PR opened/updated

```yaml
automated_checks:
  - name: "ci_pipeline"
    includes: ["lint", "type_check", "test", "build"]
    blocking: true
    
  - name: "dependency_audit"
    tool: "npm audit"
    blocking_if: "high or critical"
    
  - name: "bundle_size"
    threshold: "+5% max"
    blocking: true
    
  - name: "coverage_diff"
    threshold: "no decrease"
    blocking: true

manual_checks:
  - name: "code_review"
    required_approvers: 1
    from_pool: ["MCT-ARCH-001", "MCT-SEC-001"]
    
  - name: "design_review"
    required_if: "ui_changes"
    approver: "MCT-PD-001"
```

### Gate 2: Security Review
**Triggered**: Before merge

```yaml
checks:
  - name: "sast"
    tool: "semgrep"
    ruleset: "owasp-top-10"
    blocking: true
    
  - name: "dependency_vuln"
    tool: "snyk"
    blocking_if: "cvss >= 7.0"
    
  - name: "secret_detection"
    tool: "trufflehog"
    blocking: true
    
  - name: "auth_review"
    required_if: "auth_code_changed"
    approver: "MCT-SEC-001"
```

### Gate 3: Staging Deployment
**Triggered**: After merge to develop

```yaml
checks:
  - name: "smoke_tests"
    scope: "critical_paths"
    blocking: true
    
  - name: "integration_tests"
    scope: "api_contracts"
    blocking: true
    
  - name: "e2e_tests"
    scope: "user_journeys"
    blocking: true
    
  - name: "performance_baseline"
    metrics: ["lcp", "fid", "cls", "ttfb"]
    regression_threshold: "10%"
    blocking: false  # Alert only
```

### Gate 4: Production Deployment
**Triggered**: Promotion request

```yaml
automated_checks:
  - name: "staging_validation"
    duration: "24 hours minimum"
    blocking: true
    
  - name: "no_open_blockers"
    severity: ["P0", "P1"]
    blocking: true
    
  - name: "rollback_tested"
    blocking: true

manual_checks:
  - name: "human_approval"
    approver: "CEO"
    blocking: true
    
  - name: "qa_signoff"
    approver: "MCT-QA-001"
    blocking: true
```

### Gate 5: Post-Deployment
**Triggered**: After production deploy

```yaml
checks:
  - name: "health_check"
    endpoints: ["/health", "/api/health"]
    expected: "200 OK"
    timeout: "5 minutes"
    
  - name: "error_rate"
    threshold: "< 0.1%"
    window: "15 minutes"
    action_on_breach: "auto_rollback"
    
  - name: "latency"
    threshold: "p95 < 500ms"
    window: "15 minutes"
    action_on_breach: "alert"
```

---

## DEFINITION OF DONE (DoD)

### For User Stories

```markdown
## Story DoD Checklist

### Functionality
- [ ] All acceptance criteria met
- [ ] Edge cases handled
- [ ] Error states designed and implemented
- [ ] Loading states implemented
- [ ] Empty states implemented

### Code Quality
- [ ] Code reviewed by peer
- [ ] No lint errors
- [ ] No type errors
- [ ] Functions < 50 lines
- [ ] No code duplication

### Testing
- [ ] Unit tests written (coverage >= 80%)
- [ ] Integration tests for API calls
- [ ] E2E test for happy path
- [ ] Manual testing completed

### Documentation
- [ ] Code comments for complex logic
- [ ] API documentation updated (if applicable)
- [ ] README updated (if applicable)

### Accessibility
- [ ] Keyboard navigation works
- [ ] Screen reader compatible
- [ ] Color contrast meets WCAG AA
- [ ] Touch targets >= 44x44px on mobile

### Performance
- [ ] No console errors
- [ ] No memory leaks
- [ ] Lazy loading implemented where appropriate
- [ ] Images optimized
```

### For Features (Epic)

```markdown
## Feature DoD Checklist

### All Story DoDs Complete
- [ ] Every story in the epic meets Story DoD

### Integration
- [ ] All components integrate correctly
- [ ] API contracts honored
- [ ] Database migrations applied
- [ ] Feature flags configured

### Testing
- [ ] Full regression suite passes
- [ ] Performance benchmarks met
- [ ] Security scan clean
- [ ] Cross-browser testing complete

### Documentation
- [ ] User documentation written
- [ ] API documentation complete
- [ ] Architecture docs updated
- [ ] Runbook created

### Operational Readiness
- [ ] Monitoring dashboards configured
- [ ] Alerts configured
- [ ] Rollback procedure documented
- [ ] On-call team briefed
```

---

## CODE QUALITY STANDARDS

### TypeScript

```typescript
// ✅ GOOD: Explicit types, small functions, clear naming
interface UserProfile {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
}

async function getUserProfile(userId: string): Promise<UserProfile | null> {
  const user = await db.users.findUnique({ where: { id: userId } });
  
  if (!user) {
    return null;
  }
  
  return {
    id: user.id,
    email: user.email,
    name: user.name,
    createdAt: user.createdAt,
  };
}

// ❌ BAD: Any types, large functions, unclear naming
async function getU(id: any): Promise<any> {
  const x = await db.users.findUnique({ where: { id } });
  // ... 100 more lines
  return x;
}
```

### React Components

```tsx
// ✅ GOOD: Typed props, composition, accessibility
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
}

export function Button({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  disabled,
  children,
  ...props
}: ButtonProps) {
  return (
    <button
      className={cn(buttonVariants({ variant, size }))}
      disabled={disabled || isLoading}
      aria-busy={isLoading}
      {...props}
    >
      {isLoading && <Spinner className="mr-2" aria-hidden />}
      {children}
    </button>
  );
}

// ❌ BAD: No types, inline styles, no accessibility
export function Button(props) {
  return (
    <button style={{ backgroundColor: 'blue' }} {...props}>
      {props.children}
    </button>
  );
}
```

### API Endpoints

```typescript
// ✅ GOOD: Validation, error handling, typed responses
app.post('/api/users', 
  zValidator('json', createUserSchema),
  async (c) => {
    const body = c.req.valid('json');
    
    try {
      const user = await userService.create(body);
      return c.json({ data: user }, 201);
    } catch (error) {
      if (error instanceof ConflictError) {
        return c.json({ error: 'Email already exists' }, 409);
      }
      throw error; // Let error middleware handle
    }
  }
);

// ❌ BAD: No validation, poor error handling
app.post('/api/users', async (c) => {
  const body = await c.req.json();
  const user = await db.users.create({ data: body });
  return c.json(user);
});
```

---

## TESTING STANDARDS

### Unit Tests

```typescript
describe('UserService', () => {
  describe('create', () => {
    it('creates a user with valid data', async () => {
      // Arrange
      const input = { email: 'test@example.com', name: 'Test' };
      
      // Act
      const user = await userService.create(input);
      
      // Assert
      expect(user).toMatchObject({
        email: input.email,
        name: input.name,
      });
      expect(user.id).toBeDefined();
    });

    it('throws ConflictError for duplicate email', async () => {
      // Arrange
      const input = { email: 'existing@example.com', name: 'Test' };
      await userService.create(input);
      
      // Act & Assert
      await expect(userService.create(input))
        .rejects.toThrow(ConflictError);
    });
  });
});
```

### E2E Tests

```typescript
test.describe('User Registration', () => {
  test('allows new user to register', async ({ page }) => {
    // Navigate
    await page.goto('/register');
    
    // Fill form
    await page.fill('[data-testid="email"]', 'new@example.com');
    await page.fill('[data-testid="password"]', 'SecurePass123!');
    await page.fill('[data-testid="name"]', 'New User');
    
    // Submit
    await page.click('[data-testid="submit"]');
    
    // Verify
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="welcome"]'))
      .toContainText('Welcome, New User');
  });

  test('shows validation errors for invalid email', async ({ page }) => {
    await page.goto('/register');
    await page.fill('[data-testid="email"]', 'invalid-email');
    await page.click('[data-testid="submit"]');
    
    await expect(page.locator('[data-testid="email-error"]'))
      .toContainText('Valid email required');
  });
});
```

---

## PERFORMANCE STANDARDS

### Core Web Vitals Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| LCP (Largest Contentful Paint) | < 2.5s | 75th percentile |
| FID (First Input Delay) | < 100ms | 75th percentile |
| CLS (Cumulative Layout Shift) | < 0.1 | 75th percentile |
| TTFB (Time to First Byte) | < 200ms | 75th percentile |

### API Performance Targets

| Metric | Target |
|--------|--------|
| P50 Latency | < 50ms |
| P95 Latency | < 200ms |
| P99 Latency | < 500ms |
| Error Rate | < 0.1% |
| Availability | > 99.9% |

---

## SECURITY STANDARDS

### OWASP Top 10 Prevention

| Vulnerability | Prevention Measure |
|--------------|-------------------|
| Injection | Parameterized queries, input validation |
| Broken Auth | Secure session management, MFA |
| Sensitive Data Exposure | Encryption at rest/transit, no logging PII |
| XXE | Disable XML external entities |
| Broken Access Control | Row-level security, authorization checks |
| Security Misconfiguration | Secure defaults, hardening checklist |
| XSS | Output encoding, CSP headers |
| Insecure Deserialization | Input validation, type checking |
| Vulnerable Components | Dependency scanning, updates |
| Insufficient Logging | Audit logs, alerting |

---

*These standards are non-negotiable. Every agent must comply. Violations are automatically flagged and escalated.*
