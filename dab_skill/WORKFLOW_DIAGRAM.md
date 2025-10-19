# Workflow Diagrams

## Overall Skill Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│  "Create a DAB for my pipeline with tasks A, B, C..."      │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                        CLAUDE                                │
│  1. Reads SKILL.md documentation                            │
│  2. Reads references/examples.md (if needed)                │
│  3. Formats task description properly                       │
│  4. Determines cluster configuration                        │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                  generate_dab.py SCRIPT                      │
│  1. Parses task descriptions                                │
│  2. Extracts dependencies                                   │
│  3. Detects file types (.ipynb vs .py)                      │
│  4. Builds YAML structure                                   │
│  5. Generates databricks.yml                                │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                   databricks.yml FILE                        │
│  - Complete bundle configuration                            │
│  - All tasks with dependencies                              │
│  - Cluster configurations                                   │
│  - Dev and prod targets                                     │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│                         USER                                 │
│  1. Reviews configuration                                   │
│  2. Customizes if needed                                    │
│  3. Validates: databricks bundle validate                   │
│  4. Deploys: databricks bundle deploy -t dev                │
│  5. Runs: databricks bundle run job_name -t dev             │
└─────────────────────────────────────────────────────────────┘
```

## Task Description Processing

```
USER INPUT:
"task1: file1.py
 task2: file2.ipynb [depends_on: task1]
 task3: file3.py [depends_on: task1, task2]"

         ↓ [Parse]

PARSED STRUCTURE:
┌────────────────────────────────┐
│ Task 1                         │
│  - name: task1                 │
│  - path: file1.py              │
│  - type: python_wheel          │
│  - dependencies: []            │
└────────────────────────────────┘
         ↓
┌────────────────────────────────┐
│ Task 2                         │
│  - name: task2                 │
│  - path: file2.ipynb           │
│  - type: notebook              │
│  - dependencies: [task1]       │
└────────────────────────────────┘
         ↓
┌────────────────────────────────┐
│ Task 3                         │
│  - name: task3                 │
│  - path: file3.py              │
│  - type: python_wheel          │
│  - dependencies: [task1,task2] │
└────────────────────────────────┘

         ↓ [Generate YAML]

YAML OUTPUT:
tasks:
  - task_key: task1
    python_wheel_task: ...
  - task_key: task2
    depends_on: [{task_key: task1}]
    notebook_task: ...
  - task_key: task3
    depends_on: [{task_key: task1}, {task_key: task2}]
    python_wheel_task: ...
```

## Dependency Pattern Examples

### Linear Pipeline
```
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Task A  │────▶│ Task B  │────▶│ Task C  │
└─────────┘     └─────────┘     └─────────┘

Description:
- task_a: file_a.py
- task_b: file_b.py [depends_on: task_a]
- task_c: file_c.py [depends_on: task_b]
```

### Parallel with Merge
```
┌─────────┐
│ Task A  │────┐
└─────────┘    │     ┌─────────┐
               ├────▶│ Task C  │
┌─────────┐    │     └─────────┘
│ Task B  │────┘
└─────────┘

Description:
- task_a: file_a.py
- task_b: file_b.py
- task_c: file_c.py [depends_on: task_a, task_b]
```

### Fan-out Pattern
```
               ┌────▶│ Task B  │
               │     └─────────┘
┌─────────┐    │
│ Task A  │────┼────▶│ Task C  │
└─────────┘    │     └─────────┘
               │
               └────▶│ Task D  │
                     └─────────┘

Description:
- task_a: file_a.py
- task_b: file_b.py [depends_on: task_a]
- task_c: file_c.py [depends_on: task_a]
- task_d: file_d.py [depends_on: task_a]
```

### Diamond Pattern
```
               ┌────▶│ Task B  │────┐
               │     └─────────┘    │
┌─────────┐    │                    │    ┌─────────┐
│ Task A  │────┤                    ├───▶│ Task D  │
└─────────┘    │                    │    └─────────┘
               │     ┌─────────┐    │
               └────▶│ Task C  │────┘
                     └─────────┘

Description:
- task_a: file_a.py
- task_b: file_b.py [depends_on: task_a]
- task_c: file_c.py [depends_on: task_a]
- task_d: file_d.py [depends_on: task_b, task_c]
```

## Execution Timeline Examples

### Linear Execution
```
Timeline ────────────────────────────────────────▶

Task A:  [========]
Task B:            [========]
Task C:                      [========]

Total Time: Sum of all tasks
```

### Parallel Execution
```
Timeline ────────────────────────────────────────▶

Task A:  [========]
Task B:  [========]
Task C:            [========]

Total Time: Max(A,B) + C
```

### Mixed Execution (Diamond)
```
Timeline ────────────────────────────────────────▶

Task A:  [====]
Task B:       [========]
Task C:       [====]
Task D:                  [====]

Total Time: A + Max(B,C) + D
```

## File Type Detection Flow

```
Input File
    │
    ├── Ends with .ipynb?
    │   │
    │   YES─▶ notebook_task
    │   │     └─ notebook_path: ./notebooks/file.ipynb
    │   │        source: WORKSPACE
    │   │
    │   NO──▶ Ends with .py?
    │         │
    │         YES─▶ python_wheel_task
    │              └─ package_name: bundle_name
    │                 entry_point: path.to.file
```

## Cluster Configuration Flow

```
User Specifies Cluster Config?
    │
    ├── YES ─▶ Parse parameters:
    │         - spark_version
    │         - node_type_id
    │         - num_workers
    │
    └── NO ──▶ Use defaults:
              - spark_version: 13.3.x-scala2.12
              - node_type_id: i3.xlarge
              - num_workers: 2

              ↓
    
    Generate new_cluster block
              ↓
    
    Apply to all tasks
    (with YAML anchors for efficiency)
```

## Deployment Flow

```
┌─────────────────────────────────────────┐
│ databricks.yml generated                │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│ databricks bundle validate              │
│ (checks syntax and structure)           │
└────────────────┬────────────────────────┘
                 │
                 ▼
         ┌───────┴────────┐
         │                │
    Valid?           Invalid?
         │                │
         ▼                ▼
    ┌─────────┐    ┌──────────┐
    │ Deploy  │    │ Fix      │
    │         │    │ Errors   │
    └────┬────┘    └────┬─────┘
         │              │
         │              └─────────┐
         │                        │
         ▼                        ▼
┌─────────────────────┐    ┌──────────────┐
│ databricks bundle   │    │ Re-validate  │
│ deploy -t dev       │    └──────────────┘
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ databricks bundle   │
│ run job_name -t dev │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Job executes tasks  │
│ based on deps       │
└─────────────────────┘
```

## Data Flow Through Skill

```
Natural Language Request
         ↓
[Claude reads SKILL.md]
         ↓
Structured Task Description
         ↓
[generate_dab.py parses]
         ↓
Internal Task Objects
         ↓
[YAML generation]
         ↓
databricks.yml Configuration
         ↓
[User deploys]
         ↓
Running Databricks Job
```

## Error Handling Flow

```
Script Execution
    │
    ├─ Parse task description
    │  │
    │  ├─ Success ──▶ Continue
    │  │
    │  └─ Failure ──▶ Error: "No valid tasks found"
    │                 └─ Check format
    │
    ├─ Validate dependencies
    │  │
    │  ├─ All deps exist ──▶ Continue
    │  │
    │  └─ Missing dep ──▶ Error: "Invalid dependency"
    │                     └─ Check task names
    │
    ├─ Generate YAML
    │  │
    │  └─ Success ──▶ Write file
    │
    └─ Output
       └─ Success message with next steps
```
