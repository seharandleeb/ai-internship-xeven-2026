"""Day 24 - Conversation memory (modern message-list pattern).

Holds chat history as a plain list of (question, answer) pairs. Keeps
the most recent exchanges verbatim and compresses older ones into a
running summary using a caller-supplied summarizer function. No
deprecated LangChain memory classes are used.
"""

MAX_RECENT = 10


class ConversationMemory:
    """Stores recent Q&A pairs verbatim and summarizes older ones."""

    def __init__(self, max_recent=MAX_RECENT):
        self.max_recent = max_recent
        self.recent = []  # list of (question, answer) tuples
        self.summary = ""  # running summary of pruned exchanges

    def add(self, question, answer):
        """Record a new exchange. Caller prunes separately."""
        self.recent.append((question, answer))

    def needs_pruning(self):
        """True when more pairs are stored than the window allows."""
        return len(self.recent) > self.max_recent

    def overflow(self):
        """Return the oldest pairs that exceed the window."""
        extra = len(self.recent) - self.max_recent
        if extra <= 0:
            return []
        return self.recent[:extra]

    def prune(self, summarizer):
        """Compress overflow pairs via summarizer, then drop them.

        summarizer is a function that takes (old_summary, pairs) and
        returns a new summary string.
        """
        old = self.overflow()
        if not old:
            return
        self.summary = summarizer(self.summary, old)
        self.recent = self.recent[len(old):]

    def as_context(self):
        """Build the history text block for the prompt."""
        parts = []
        if self.summary:
            parts.append("Summary of earlier conversation:")
            parts.append(self.summary)
        if self.recent:
            parts.append("Recent conversation:")
            for question, answer in self.recent:
                parts.append(f"User: {question}")
                parts.append(f"Assistant: {answer}")
        return "\n".join(parts)