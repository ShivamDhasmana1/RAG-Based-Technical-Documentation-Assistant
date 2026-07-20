# LangGraph Basics

LangGraph is a library for building stateful, multi-step applications on
top of language models, expressed as a graph of nodes and edges rather
than a single linear chain.

## StateGraph

The core building block is `StateGraph`, which is initialized with a
schema describing the shared state that flows between nodes — commonly a
`TypedDict`. Every node receives the current state, may modify it, and
returns the updated state.

## Nodes

A node is a plain Python function (or callable) that takes the state as
its argument and returns a dictionary of updates to merge into it. Nodes
are registered on the graph with `add_node(name, function)`.

## Edges

Edges connect nodes and determine execution order. A fixed edge, created
with `add_edge(source, destination)`, always moves execution from one
node to the next. `START` and `END` are special markers for the entry
point and the terminal point of the graph.

## Conditional edges

A conditional edge, created with `add_conditional_edges(source, router,
mapping)`, uses a router function to inspect the current state and decide
which node to go to next. This is the mechanism used to implement retry
loops, branching logic, or early termination based on intermediate
results — for example, retrying a step if a quality check fails.

## Compiling and running

Once nodes and edges are registered, calling `.compile()` on the
`StateGraph` produces a runnable graph object. That graph is invoked with
`.invoke(initial_state)`, which runs nodes in order (following any
conditional routing) until it reaches `END`, then returns the final
state.

## Troubleshooting: infinite loops

If a conditional edge routes back to an earlier node without a way to
eventually reach `END`, the graph can loop indefinitely. A common fix is
to track an attempt counter in the state and have the router function
check it against a maximum before deciding whether to retry again.
