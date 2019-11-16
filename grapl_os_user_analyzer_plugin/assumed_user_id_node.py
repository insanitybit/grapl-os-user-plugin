from copy import deepcopy
from typing import *

from grapl_analyzerlib.nodes.comparators import IntCmp, _int_cmps
from grapl_analyzerlib.nodes.types import PropertyT
from grapl_analyzerlib.nodes.viewable import EdgeViewT, ForwardEdgeView
from grapl_analyzerlib.prelude import DynamicNodeQuery, DynamicNodeView, ProcessQuery, ProcessView
from pydgraph import DgraphClient


class AssumedUserIdQuery(DynamicNodeQuery):
    def __init__(self) -> None:
        super(AssumedUserIdQuery, self).__init__("AssumedAssumedUserId", AssumedUserIdView)

    def with_assumed_timestamp(self, eq=IntCmp, gt=IntCmp, lt=IntCmp) -> "AssumedUserIdQuery":
        self.set_int_property_filter("assumed_timestamp", _int_cmps("assumed_timestamp", eq=eq, gt=gt, lt=lt))
        return self

    def with_assuming_process_id(self, eq=IntCmp, gt=IntCmp, lt=IntCmp) -> "AssumedUserIdQuery":
        self.set_int_property_filter("assuming_process_id", _int_cmps("assuming_process_id", eq=eq, gt=gt, lt=lt))
        return self

    def with_user_id(self, eq=IntCmp, gt=IntCmp, lt=IntCmp) -> "AssumedUserIdQuery":
        self.set_int_property_filter("user_id", _int_cmps("user_id", eq=eq, gt=gt, lt=lt))
        return self

    def with_assuming_process(
            self, assuming_process_query: "Optional[ProcessQuery]" = None
    ) -> "AssumedUserIdQuery":
        if assuming_process_query:
            assuming_process = deepcopy(assuming_process_query)
        else:
            assuming_process = ProcessQuery()
        self.set_forward_edge_filter("assuming_process", assuming_process)
        assuming_process.set_reverse_edge_filter("~assuming_process", self, "assuming_process")
        return self

    def query(
            self,
            dgraph_client: DgraphClient,
            contains_node_key: Optional[str] = None,
            first: Optional[int] = 1000,
    ) -> List["AssumedUserIdView"]:
        return self._query(dgraph_client, contains_node_key, first)

    def query_first(
            self, dgraph_client: DgraphClient, contains_node_key: Optional[str] = None
    ) -> Optional["AssumedUserIdView"]:
        return self._query_first(dgraph_client, contains_node_key)


class AssumedUserIdView(DynamicNodeView):
    def __init__(
            self,
            dgraph_client: DgraphClient,
            node_key: str,
            uid: str,
            node_type: str,
            src_pid: Optional[int] = None,
            dst_pid: Optional[int] = None,
            assuming_process: Optional[ProcessQuery] = None,
            ipc_recipient: Optional[ProcessQuery] = None,
    ):
        super(AssumedUserIdView, self).__init__(
            dgraph_client=dgraph_client, node_key=node_key, uid=uid, node_type=node_type
        )
        self.node_type = node_type
        self.src_pid = src_pid
        self.dst_pid = dst_pid
        self.assuming_process = assuming_process
        self.ipc_recipient = ipc_recipient

    @staticmethod
    def _get_property_types() -> Mapping[str, "PropertyT"]:
        return {"src_pid": int, "dst_pid": int}

    @staticmethod
    def _get_forward_edge_types() -> Mapping[str, "EdgeViewT"]:
        f_edges = {"assuming_process": ProcessView, "ipc_recipient": ProcessView}

        return {fe[0]: fe[1] for fe in f_edges.items() if fe[1]}

    def _get_forward_edges(self) -> "Mapping[str, ForwardEdgeView]":
        f_edges = {
            "assuming_process": self.assuming_process,
            "ipc_recipient": self.ipc_recipient
        }

        return {fe[0]: fe[1] for fe in f_edges.items() if fe[1]}

    def _get_properties(self, fetch: bool = False) -> Mapping[str, Union[str, int]]:
        props = {"src_pid": self.src_pid, "dst_pid": self.dst_pid}
        return {p[0]: p[1] for p in props.items() if p[1] is not None}
