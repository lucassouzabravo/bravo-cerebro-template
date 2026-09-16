---
name: process-visualizer
description: Create clear, accurate visual explanations of workflows, systems, automations, dependencies, handoffs, queues, and decision paths. Use whenever the user asks to explain something visually, wants a flow showing what triggers what, asks where data goes, or needs a complex process made easier to understand.
---

# Process Visualizer

Turn a process into the smallest visual that makes its relationships obvious. Preserve the user's terminology and make reasonable assumptions instead of blocking on minor gaps.

## Choose the visual

Use the diagram type that matches the relationship, not a generic flowchart by default.

| Need to explain | Use |
|---|---|
| What happens next; what triggers what; data handoffs | Mermaid flowchart |
| Exchanges between people, systems, or agents | Mermaid sequence diagram |
| Ticket, approval, or lifecycle statuses | Mermaid state diagram |
| Dates, phases, or scheduled work | Mermaid timeline or Gantt |
| Exact fields, roles, comparisons, or inputs/outputs | Markdown table |
| Ownership or nested structure | Mermaid mindmap or a compact tree |

Use a short prose explanation instead of a diagram when there is only one direct relationship. Use an overview plus one drill-down diagram when a single diagram would become dense.

## Build the visual

1. Identify the trigger, actors/systems, transformations, decisions, outputs, and termination condition.
2. Keep labels short, concrete, and in the user's language. Prefer verbs: "Cria job", "Busca contexto", "Grava sugestão".
3. Show only the relationships needed to answer the request. Put implementation detail beneath the diagram.
4. For a flowchart, use top-down direction by default. Do not place more than five nodes horizontally.
5. Use decisions only when a branch changes the route. Label outcomes clearly, such as "Sucesso" and "Falha".
6. Distinguish the durable record from a temporary action when relevant: for example, "fila no banco" versus "sessão do agente".
7. Check every arrow against the explanation. Do not invent systems, permissions, or automatic actions that were not stated.

## Mermaid rules

- Put diagrams in fenced `mermaid` blocks.
- Keep one diagram focused on one relationship.
- Quote labels containing punctuation or parentheses.
- Avoid HTML, click directives, styling configuration, and decorative nodes.
- Do not use Mermaid for precise multi-field comparisons; use a table.
- If a diagram is long, split it into an overview and a focused subflow rather than shrinking text or making a wide chain.

## Response pattern

Lead with one sentence that states the process in plain language. Then provide the visual. Add only the notes that materially improve interpretation:

- **Como ler:** explain the trigger and end condition when they are not obvious.
- **Ponto crítico:** call out the one dependency, queue, approval, or failure condition that changes the behavior.
- **Assumption:** state an assumption only when it materially affects the diagram.

When the user asks for a visual explanation of a process, produce the diagram directly. Do not describe how Mermaid works unless asked.
