from dataclasses import dataclass

from tato._node_type import NodeType, TopLevelNode


@dataclass(frozen=True)
class OrderedNode:
    """Information needed to order TopLevelNodes."""

    node: TopLevelNode
    node_type: NodeType
    # Number of times a node is referenced throughout a package. Requires the
    # package has been indexed with `tato index <path>`.
    num_references: int
    # The earlier a TopLevelNode is accessed, the earlier it should appear in
    # the output.
    # Acesss is the (lineno, colno) in the original file.
    first_access: tuple[int, int]
    # Tie break should be the order of the node in the original file.
    prev_body_index: int
    _debug_source_code: str

    def __hash__(self) -> int:
        return hash(self.node)

    def __eq__(self, other: "OrderedNode") -> bool:
        return self.node == other.node

    def __lt__(self, other: "OrderedNode") -> bool:
        return self._as_tuple() < other._as_tuple()

    def _as_tuple(self) -> tuple:
        if self.node_type == NodeType.IMPORT:
            # Try and keep imports sorted by their previous location.
            return (self.node_type, self.prev_body_index)
        else:
            return (
                self.node_type,
                -1 * self.num_references,  # more reference should come first
                self.first_access,
                self.prev_body_index,
            )
