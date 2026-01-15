# Agent Communication Protocol (ACP)
## Monarch Castle Technologies

> **Protocol Version**: 2.0.0
> **Status**: ACTIVE
> **Classification**: INTERNAL

---

## MESSAGE SCHEMA

All inter-agent communications MUST follow this JSON schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://monarchcastle.tech/schemas/agent-message.json",
  "title": "Agent Communication Protocol Message",
  "type": "object",
  "required": ["header", "payload"],
  
  "properties": {
    "header": {
      "type": "object",
      "required": ["message_id", "timestamp", "from", "to", "type", "priority"],
      "properties": {
        "message_id": {
          "type": "string",
          "format": "uuid",
          "description": "Unique identifier for this message"
        },
        "timestamp": {
          "type": "string",
          "format": "date-time",
          "description": "ISO 8601 timestamp"
        },
        "from": {
          "type": "string",
          "pattern": "^MCT-[A-Z]+-[0-9]{3}$",
          "description": "Sender agent ID"
        },
        "to": {
          "oneOf": [
            {"type": "string", "pattern": "^MCT-[A-Z]+-[0-9]{3}$"},
            {"type": "array", "items": {"type": "string"}}
          ],
          "description": "Recipient agent ID(s)"
        },
        "type": {
          "type": "string",
          "enum": ["REQUEST", "RESPONSE", "HANDOFF", "NOTIFY", "ESCALATE", "QUERY", "ACK"],
          "description": "Message type"
        },
        "priority": {
          "type": "string",
          "enum": ["P0", "P1", "P2", "P3"],
          "description": "Message priority"
        },
        "correlation_id": {
          "type": "string",
          "format": "uuid",
          "description": "Links related messages"
        },
        "reply_to": {
          "type": "string",
          "format": "uuid",
          "description": "Message this replies to"
        }
      }
    },
    
    "payload": {
      "type": "object",
      "required": ["action"],
      "properties": {
        "action": {
          "type": "string",
          "description": "Requested action"
        },
        "context": {
          "type": "object",
          "description": "Contextual information"
        },
        "artifacts": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "type": {"type": "string"},
              "path": {"type": "string"},
              "hash": {"type": "string"}
            }
          }
        },
        "constraints": {
          "type": "object",
          "properties": {
            "deadline": {"type": "string", "format": "date-time"},
            "budget_hours": {"type": "number"},
            "quality_level": {"type": "string"}
          }
        },
        "data": {
          "type": "object",
          "description": "Arbitrary payload data"
        }
      }
    },
    
    "response_required": {
      "type": "object",
      "properties": {
        "required": {"type": "boolean", "default": true},
        "timeout_ms": {"type": "integer", "default": 30000},
        "format": {"type": "string"}
      }
    }
  }
}
```

---

## MESSAGE TYPES

### REQUEST
Asking another agent to perform an action.

```json
{
  "header": {
    "message_id": "550e8400-e29b-41d4-a716-446655440000",
    "timestamp": "2026-01-15T20:00:00Z",
    "from": "MCT-PM-001",
    "to": "MCT-UXD-001",
    "type": "REQUEST",
    "priority": "P1"
  },
  "payload": {
    "action": "create_wireframes",
    "context": {
      "feature": "User Dashboard",
      "prd_ref": "PRD-2026-001"
    },
    "artifacts": [
      {"type": "prd", "path": "/docs/prds/dashboard.md", "hash": "abc123"}
    ],
    "constraints": {
      "deadline": "2026-01-18T17:00:00Z",
      "screens": ["overview", "settings", "profile"]
    }
  },
  "response_required": {
    "required": true,
    "timeout_ms": 1800000
  }
}
```

### HANDOFF
Transferring ownership of work.

```json
{
  "header": {
    "message_id": "550e8400-e29b-41d4-a716-446655440001",
    "timestamp": "2026-01-16T14:00:00Z",
    "from": "MCT-ARCH-001",
    "to": ["MCT-BE-001", "MCT-FE-001"],
    "type": "HANDOFF",
    "priority": "P1"
  },
  "payload": {
    "action": "implement_feature",
    "context": {
      "feature": "User Dashboard",
      "tdd_ref": "TDD-2026-001",
      "component_assignments": {
        "MCT-BE-001": ["api_endpoints", "data_layer"],
        "MCT-FE-001": ["ui_components", "pages"]
      }
    },
    "artifacts": [
      {"type": "tdd", "path": "/docs/tdds/dashboard.md", "hash": "def456"},
      {"type": "api_spec", "path": "/docs/api/dashboard.yaml", "hash": "ghi789"},
      {"type": "linear_tickets", "path": "linear://project/DASH", "hash": null}
    ],
    "constraints": {
      "deadline": "2026-01-25T17:00:00Z",
      "sync_points": ["api_contract_freeze", "integration_ready"]
    }
  },
  "response_required": {
    "required": true,
    "timeout_ms": 300000
  }
}
```

### ESCALATE
Requesting higher authority intervention.

```json
{
  "header": {
    "message_id": "550e8400-e29b-41d4-a716-446655440002",
    "timestamp": "2026-01-17T10:30:00Z",
    "from": "MCT-BE-001",
    "to": "MCT-ARCH-001",
    "type": "ESCALATE",
    "priority": "P0"
  },
  "payload": {
    "action": "resolve_blocker",
    "context": {
      "blocker_type": "technical_decision",
      "description": "Database choice impacts performance requirements",
      "options": [
        {"option": "PostgreSQL", "pros": ["familiar"], "cons": ["scaling"]},
        {"option": "ScyllaDB", "pros": ["performance"], "cons": ["learning curve"]}
      ],
      "recommendation": "PostgreSQL with read replicas",
      "blocked_since": "2026-01-17T08:00:00Z"
    },
    "artifacts": [
      {"type": "analysis", "path": "/docs/decisions/db-choice.md", "hash": "jkl012"}
    ]
  },
  "response_required": {
    "required": true,
    "timeout_ms": 3600000
  }
}
```

---

## SLA DEFINITIONS

```yaml
SLA:
  acknowledgment:
    P0: "5 minutes"
    P1: "30 minutes"
    P2: "2 hours"
    P3: "8 hours"
    
  response:
    P0: "15 minutes"
    P1: "2 hours"
    P2: "8 hours"
    P3: "24 hours"
    
  completion:
    P0: "4 hours"
    P1: "24 hours"
    P2: "72 hours"
    P3: "1 week"
    
  escalation_trigger:
    acknowledgment_missed: "auto_escalate"
    response_missed: "notify_human"
    completion_missed: "review_and_replan"
```

---

## ROUTING RULES

```yaml
routing:
  by_work_type:
    prd_creation:
      primary: "MCT-PM-001"
      backup: "MCT-CPO-001"
      
    ui_design:
      primary: "MCT-PD-001"
      depends_on: "MCT-UXD-001"
      
    api_development:
      primary: "MCT-BE-001"
      review: "MCT-ARCH-001"
      security: "MCT-SEC-001"
      
    frontend_development:
      primary: "MCT-FE-001"
      review: "MCT-ARCH-001"
      
    database_changes:
      primary: "MCT-DBA-001"
      review: "MCT-ARCH-001"
      security: "MCT-SEC-001"
      
    deployment:
      primary: "MCT-OPS-001"
      requires: "MCT-SEC-001"
      approval: "Human"
      
  by_priority:
    P0:
      notify: ["all_relevant", "human"]
      parallel: true
      
    P1:
      notify: ["primary"]
      parallel: false
      
    P2:
      notify: ["primary"]
      queue: true
      
    P3:
      notify: ["primary"]
      queue: true
      batch_ok: true
```

---

## ERROR HANDLING

```yaml
error_handling:
  message_failed:
    retry_count: 3
    retry_delay: "exponential_backoff"
    fallback: "dead_letter_queue"
    
  agent_unavailable:
    action: "route_to_backup"
    notify: "MCT-OPS-001"
    
  timeout:
    action: "cancel_and_escalate"
    notify: ["sender", "human_if_p0_p1"]
    
  validation_failed:
    action: "reject_with_details"
    notify: "sender"
```

---

## AUDIT REQUIREMENTS

Every message exchange MUST be logged:

```typescript
interface MessageAudit {
  message_id: string;
  correlation_id: string;
  timestamp: string;
  from_agent: string;
  to_agent: string[];
  message_type: string;
  priority: string;
  action: string;
  status: 'sent' | 'delivered' | 'acknowledged' | 'completed' | 'failed';
  latency_ms: number;
  error?: string;
}
```

Retention: 90 days hot, 3 years cold storage.

---

*All agents MUST implement this protocol. Non-compliance will trigger automatic escalation.*
