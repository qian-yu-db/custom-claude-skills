# Mermaid Syntax Reference Guide

Comprehensive syntax reference for all Mermaid diagram types. Load this file when creating complex diagrams or when the user needs advanced features.

## Table of Contents
- [Flowchart Advanced](#flowchart-advanced)
- [Sequence Diagram Advanced](#sequence-diagram-advanced)
- [Class Diagram Advanced](#class-diagram-advanced)
- [ER Diagram Advanced](#er-diagram-advanced)
- [State Diagram Advanced](#state-diagram-advanced)
- [Gantt Chart Advanced](#gantt-chart-advanced)
- [Git Graph](#git-graph)
- [Pie Chart](#pie-chart)
- [Mindmap](#mindmap)
- [Timeline](#timeline)
- [Styling Reference](#styling-reference)
- [Escaping and Special Characters](#escaping-and-special-characters)

---

## Flowchart Advanced

### All Node Shapes
```mermaid
flowchart TB
    rect[Rectangle]
    rounded(Rounded Rectangle)
    stadium([Stadium])
    subroutine[[Subroutine]]
    database[(Database)]
    circle((Circle))
    diamond{Diamond}
    hexagon{{Hexagon}}
    parallelogram[/Parallelogram/]
    parallelogram2[\Parallelogram Alt\]
    trapezoid[/Trapezoid\]
    trapezoid2[\Trapezoid Alt/]
    flag>Flag]
    double_circle(((Double Circle)))
```

### Link Types
```mermaid
flowchart LR
    A --> B
    A --- C
    A -.-> D
    A ==> E
    A --text--> F
    A -.text.-> G
    A ==text==> H
    A --o I
    A --x J
    A o--o K
    A <--> L
```

### Link Length Control
```mermaid
flowchart TD
    A --> B
    A ---> C
    A ----> D
```

### Complex Subgraphs
```mermaid
flowchart TB
    subgraph Cloud["Cloud Infrastructure"]
        direction TB
        subgraph Region1["US-East"]
            LB1[Load Balancer]
            S1[Server 1]
            S2[Server 2]
        end
        subgraph Region2["US-West"]
            LB2[Load Balancer]
            S3[Server 3]
            S4[Server 4]
        end
    end
    
    User --> LB1 & LB2
    LB1 --> S1 & S2
    LB2 --> S3 & S4
```

### Interactions (for web embedding)
```mermaid
flowchart LR
    A --> B
    click A "https://example.com" "Tooltip"
    click B callback "Tooltip"
```

---

## Sequence Diagram Advanced

### All Arrow Types
```mermaid
sequenceDiagram
    A->>B: Solid line with arrowhead
    A-->>B: Dotted line with arrowhead
    A-xB: Solid line with cross
    A--xB: Dotted line with cross
    A-)B: Solid line with open arrow (async)
    A--)B: Dotted line with open arrow (async)
```

### Activation and Nesting
```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant D as Database
    
    C->>+S: Request
    S->>+D: Query
    D-->>-S: Results
    S-->>-C: Response
```

### Loops, Conditionals, and Parallel
```mermaid
sequenceDiagram
    participant U as User
    participant S as System
    
    U->>S: Login
    
    alt Valid credentials
        S-->>U: Welcome
    else Invalid credentials
        S-->>U: Error
    end
    
    loop Health check
        S->>S: Check status
    end
    
    par Parallel tasks
        S->>S: Task A
    and
        S->>S: Task B
    end
    
    opt Optional step
        U->>S: Logout
    end
    
    critical Critical section
        S->>S: Transaction
    option Timeout
        S-->>U: Retry
    end
    
    break Connection lost
        S-->>U: Reconnect
    end
```

### Notes
```mermaid
sequenceDiagram
    participant A
    participant B
    
    Note left of A: Left note
    Note right of B: Right note
    Note over A: Over one
    Note over A,B: Over multiple
    
    A->>B: Message
```

### Actors vs Participants
```mermaid
sequenceDiagram
    actor User
    participant System
    participant Database
    
    User->>System: Request
```

### Autonumbering
```mermaid
sequenceDiagram
    autonumber
    A->>B: First
    B->>C: Second
    C->>A: Third
```

---

## Class Diagram Advanced

### Visibility Modifiers
```mermaid
classDiagram
    class Example {
        +publicAttribute
        -privateAttribute
        #protectedAttribute
        ~packagePrivate
        +publicMethod()
        -privateMethod()
        #protectedMethod()
        ~packageMethod()
    }
```

### Generic Types
```mermaid
classDiagram
    class Container~T~ {
        +List~T~ items
        +add(T item) void
        +get(int index) T
    }
```

### All Relationship Types
```mermaid
classDiagram
    classA <|-- classB : Inheritance
    classC *-- classD : Composition
    classE o-- classF : Aggregation
    classG <-- classH : Association
    classI -- classJ : Link (solid)
    classK <.. classL : Dependency
    classM <|.. classN : Realization
    classO .. classP : Link (dashed)
```

### Cardinality
```mermaid
classDiagram
    Customer "1" --> "*" Order
    Order "1" --> "1..*" LineItem
    Student "0..*" --> "1..*" Course
```

### Annotations and Stereotypes
```mermaid
classDiagram
    class Shape {
        <<interface>>
        +draw() void
    }
    class Circle {
        <<service>>
        +radius: float
    }
    class Color {
        <<enumeration>>
        RED
        GREEN
        BLUE
    }
```

### Namespaces
```mermaid
classDiagram
    namespace Models {
        class User
        class Order
    }
    namespace Services {
        class UserService
        class OrderService
    }
```

---

## ER Diagram Advanced

### All Cardinality Options
```mermaid
erDiagram
    A ||--|| B : "one to one"
    C ||--o{ D : "one to zero or more"
    E ||--|{ F : "one to one or more"
    G |o--o| H : "zero or one to zero or one"
    I }o--o{ J : "zero or more to zero or more"
```

### Attribute Types and Keys
```mermaid
erDiagram
    CUSTOMER {
        int id PK "Primary key"
        string email UK "Must be unique"
        string name "Customer name"
        int address_id FK "Foreign key to ADDRESS"
    }
```

### Complex Schema Example
```mermaid
erDiagram
    USER ||--o{ POST : creates
    USER ||--o{ COMMENT : writes
    POST ||--o{ COMMENT : has
    POST }o--o{ TAG : tagged_with
    
    USER {
        uuid id PK
        varchar email UK
        varchar username UK
        timestamp created_at
    }
    POST {
        uuid id PK
        uuid author_id FK
        text content
        timestamp published_at
    }
    COMMENT {
        uuid id PK
        uuid post_id FK
        uuid user_id FK
        text body
    }
    TAG {
        int id PK
        varchar name UK
    }
```

---

## State Diagram Advanced

### Composite States
```mermaid
stateDiagram-v2
    [*] --> Active
    
    state Active {
        [*] --> Idle
        Idle --> Processing : start
        Processing --> Idle : complete
    }
    
    Active --> Suspended : suspend
    Suspended --> Active : resume
    Active --> [*] : terminate
```

### Forks and Joins (Parallel States)
```mermaid
stateDiagram-v2
    [*] --> fork_state
    state fork_state <<fork>>
    fork_state --> State2
    fork_state --> State3
    
    state join_state <<join>>
    State2 --> join_state
    State3 --> join_state
    join_state --> State4
    State4 --> [*]
```

### Choice Pseudostate
```mermaid
stateDiagram-v2
    [*] --> IsValid
    state IsValid <<choice>>
    IsValid --> Valid : if valid
    IsValid --> Invalid : if invalid
    Valid --> [*]
    Invalid --> [*]
```

### Notes
```mermaid
stateDiagram-v2
    [*] --> Active
    Active --> Inactive
    
    note right of Active
        This is a note
        spanning multiple lines
    end note
    
    note left of Inactive : Short note
```

### Concurrency
```mermaid
stateDiagram-v2
    [*] --> Active
    state Active {
        [*] --> Working
        --
        [*] --> Listening
    }
```

---

## Gantt Chart Advanced

### Task Dependencies and Milestones
```mermaid
gantt
    title Development Timeline
    dateFormat YYYY-MM-DD
    excludes weekends
    
    section Planning
        Requirements    :done, req, 2024-01-01, 14d
        Design          :active, des, after req, 21d
        Review          :milestone, m1, after des, 0d
    
    section Development
        Backend         :crit, dev1, after des, 30d
        Frontend        :dev2, after des, 25d
        Integration     :after dev1 dev2, 10d
    
    section Testing
        QA Testing      :test, after dev1, 14d
        UAT             :after test, 7d
```

### Task States
- `done` - Completed task
- `active` - Current task
- `crit` - Critical path task
- `milestone` - Zero-duration milestone

---

## Git Graph

```mermaid
gitGraph
    commit id: "Initial"
    branch develop
    checkout develop
    commit id: "Feature A"
    commit id: "Feature B"
    checkout main
    merge develop id: "Merge develop"
    commit id: "Hotfix"
    branch release
    checkout release
    commit id: "Release prep"
    checkout main
    merge release tag: "v1.0"
```

### Options
```mermaid
gitGraph TB:
    commit
    branch develop
    commit
    checkout main
    merge develop
```

---

## Pie Chart

```mermaid
pie showData
    title Browser Market Share
    "Chrome" : 65
    "Safari" : 19
    "Firefox" : 8
    "Edge" : 5
    "Other" : 3
```

---

## Mindmap

```mermaid
mindmap
    root((Project))
        Planning
            Requirements
            Timeline
            Budget
        Development
            Frontend
                React
                CSS
            Backend
                API
                Database
        Testing
            Unit Tests
            Integration
            E2E
```

---

## Timeline

```mermaid
timeline
    title Product History
    2020 : Initial concept
         : Market research
    2021 : MVP development
         : Beta launch
    2022 : Public release
         : Series A funding
    2023 : International expansion
```

---

## Styling Reference

### Class-based Styling
```mermaid
flowchart LR
    A:::success --> B:::warning --> C:::error
    
    classDef success fill:#9f6,stroke:#333
    classDef warning fill:#ff9,stroke:#333
    classDef error fill:#f66,stroke:#333
```

### Inline Styling
```mermaid
flowchart LR
    A --> B --> C
    style A fill:#bbf,stroke:#333,stroke-width:2px
    style B fill:#fbf,stroke:#f66,stroke-dasharray: 5 5
```

### Link Styling
```mermaid
flowchart LR
    A --> B --> C
    linkStyle 0 stroke:#ff3,stroke-width:4px
    linkStyle 1 stroke:#f00,stroke-width:2px,stroke-dasharray: 3
```

### Theme Configuration
```mermaid
%%{init: {'theme': 'forest'}}%%
flowchart LR
    A --> B --> C
```

Available themes: `default`, `forest`, `dark`, `neutral`, `base`

---

## Escaping and Special Characters

### Characters Requiring Quotes
Always wrap labels in quotes when they contain:
- Parentheses: `A["getData()"]`
- Brackets: `A["array[0]"]`
- Colons: `A["Key: Value"]`
- Semicolons: `A["a; b"]`
- Pipes: `A["a | b"]`
- Hashes: `A["#channel"]`

### HTML Entities
```mermaid
flowchart LR
    A["Less than: &lt;"]
    B["Greater than: &gt;"]
    C["Ampersand: &amp;"]
```

### Line Breaks in Labels
```mermaid
flowchart LR
    A["Line 1<br>Line 2<br>Line 3"]
```

### Unicode
```mermaid
flowchart LR
    A["✓ Success"] --> B["⚠ Warning"] --> C["✗ Error"]
```
