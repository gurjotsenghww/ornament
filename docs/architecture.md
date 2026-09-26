# Ornàment Architecture Specification

## Architectural Philosophy
> **"The model should reason about the work, agents should execute specialized tasks, tools should perform actions, tests should provide evidence, and the Main Agent should decide what happens next."**

Ornàment adheres strictly to the **Minimal Change Policy**:
1. Identify symptom
2. Locate root cause
3. Identify affected files
4. Make smallest safe change
5. Build
6. Test
7. Verify

## Subsystem Topology

```text
                  USER / CLI / WEB UI
                           │
                           ▼
                    ┌─────────────┐
                    │ MAIN AGENT  │
                    │ (Architect) │
                    └──────┬──────┘
                           │
                     AGENT MANAGER
         (Hardware-aware concurrency throttle)
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
    CODE AGENT        DEBUG AGENT        TEST AGENT
 (Surgical edits)    (Diagnostician)     (Playwright)
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
                    FILE LOCK MANAGER
                           │
                           ▼
                      FILE MANAGER
              (Sandboxed Project Files)
                           │
                           ▼
                   MULTI-LEVEL TESTS
        (Level 1-7 Static, Build, Playwright, A11y)
                           │
                           ▼
                GIT CHECKPOINT & ROLLBACK
```

## Subsystems

### 1. Hardware Awareness (`ornament/hardware/`)
- `HardwareManager`: Real-time monitoring of CPU, RAM, and GPU telemetry via `psutil` and `nvidia-smi`.
- Throttles agent concurrency dynamically to prevent memory thrashing on 16GB RAM / 6GB VRAM configurations.

### 2. Model Abstraction Layer (`ornament/models/`)
- ModelProvider interface: `generate()`, `generate_structured()`, `stream()`, `estimate_tokens()`, `health_check()`.
- Providers: `OpenAICompatibleProvider`, `DeterministicEngineProvider`.
- Decouples LLM implementations (Qwen2.5, Qwen3, cloud, or offline test engines).

### 3. File Ownership & Minimal Change (`ornament/files/`)
- `FileLockManager`: Prevents simultaneous conflicting modifications by parallel agents. Allows Main Agent override.
- `FileManager`: Sandboxed operations strictly confined to `workspace/`. Prohibits duplicate copy-paste files (`HeroFinal2.tsx`).
- `DependencyGraph`: Maps imports and component dependents to calculate ripple effects.

### 4. Git Checkpoints & Rollbacks (`ornament/git_ops/`)
- `GitCheckpointManager`: Automatically creates Git snapshots before agent tasks. Rolls back to clean commits if tests fail.

### 5. Persistent Memories (`ornament/memory/`)
- `ProjectMemory`: Tracks framework, routes, components, and design system in SQLite.
- `FailureMemory`: Records failure -> diagnosis -> fix sequences for dataset generation.

### 6. Local RAG Retrieval (`ornament/rag/`)
- `LocalVectorStore`: Local TF-IDF / BM25 index providing targeted web standards (Next.js App Router, Tailwind, A11y, Performance) without cloud latency.
