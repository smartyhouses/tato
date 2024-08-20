from typing import DefaultDict

import libcst as cst
from libcst.codemod import ContextAwareVisitor
from libcst.metadata import (
    Assignment,
    CodeRange,
    FullyQualifiedNameProvider,
    GlobalScope,
    PositionProvider,
    ScopeProvider,
)

from tato.indexer._filecache import get_or_create_file
from tato.indexer._types import DefRef, Definition, Reference
from tato.lib.uuid import uuid7str


class DefinitionCollector(ContextAwareVisitor):
    METADATA_DEPENDENCIES = (
        ScopeProvider,
        PositionProvider,
        FullyQualifiedNameProvider,
    )

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.definitions: list[Definition] = []

    def visit_Module(self, node: cst.Module) -> bool:
        f = get_or_create_file(self.context)
        global_scope = self.get_metadata(ScopeProvider, node)
        global_scope = cst.ensure_type(global_scope, GlobalScope)
        for assignment in global_scope.assignments:
            assignment = cst.ensure_type(assignment, Assignment)
            position = cst.ensure_type(
                self.get_metadata(PositionProvider, assignment.node), CodeRange
            )
            fqns = self.get_metadata(FullyQualifiedNameProvider, assignment.node, set())
            # Each assignment should only have 1 fqn
            assert len(fqns) <= 1, f"Expected 0 or 1 fqn, got {len(fqns)}"
            if fqns:
                [fqn] = fqns
                d = Definition(
                    id=uuid7str(),
                    file_id=f.id,
                    fully_qualified_name=fqn.name,
                    start_line=position.start.line,
                    start_col=position.start.column,
                )
                self.definitions.append(d)
        return False


class ReferenceCollector(ContextAwareVisitor):
    METADATA_DEPENDENCIES = (
        ScopeProvider,
        PositionProvider,
        FullyQualifiedNameProvider,
    )

    def __init__(
        self, *args, definitions: DefaultDict[str, list[Definition]], **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.definitions: DefaultDict[str, list[Definition]] = definitions
        self.references: list[Reference] = []
        self.defsrefs: list[DefRef] = []

    def visit_Attribute(self, node: cst.Attribute) -> bool:
        return self._visit_name_attr_alike(node)

    def visit_Name(self, node: cst.Name) -> bool:
        return self._visit_name_attr_alike(node)

    def _visit_name_attr_alike(self, node: cst.CSTNode) -> bool:
        f = get_or_create_file(self.context)
        fqnames = self.get_metadata(FullyQualifiedNameProvider, node, set())
        for fqname in fqnames:
            if defs := self.definitions[fqname.name]:
                position = cst.ensure_type(
                    self.get_metadata(PositionProvider, node), CodeRange
                )
                r = Reference(
                    id=uuid7str(),
                    file_id=f.id,
                    fully_qualified_name=fqname.name,
                    start_line=position.start.line,
                    start_col=position.start.column,
                )
                self.references.append(r)
                for d in defs:
                    dr = DefRef(
                        id=uuid7str(),
                        definition_id=d.id,
                        reference_id=r.id,
                    )
                    self.defsrefs.append(dr)

        # Optimization tos top recursing on children if we've found the reference.
        return False if any(self.definitions[fq.name] for fq in fqnames) else True
