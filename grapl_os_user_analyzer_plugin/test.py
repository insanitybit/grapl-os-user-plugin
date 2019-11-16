from copy import deepcopy
from typing import *

from grapl_analyzerlib.nodes.comparators import IntCmp, _int_cmps, StrCmp
from grapl_analyzerlib.nodes.types import PropertyT
from grapl_analyzerlib.nodes.viewable import EdgeViewT, ForwardEdgeView
from grapl_analyzerlib.prelude import DynamicNodeQuery, DynamicNodeView, ProcessQuery, ProcessView
from pydgraph import DgraphClient

from grapl_os_user_analyzer_plugin.assumed_auid_node import AssumedAuidQuery


class Auid(DynamicNodeQuery):
    def __init__(self) -> None:
        super(Auid, self).__init__("Auid", AuidView)

    def with_auid(self, eq=IntCmp, gt=IntCmp, lt=IntCmp) -> "Auid":
        self.set_int_property_filter("auid", _int_cmps("auid", eq=eq, gt=gt, lt=lt))
        return self

    def with_asset_id(self, eq=StrCmp, gt=StrCmp, lt=StrCmp) -> "Auid":
        self.set_int_property_filter("asset_id", _int_cmps("asset_id", eq=eq, gt=gt, lt=lt))
        return self

    def with_auid_assumptions(self, auid_assumption_query: AssumedAuidQuery):
        if auid_assumption_query:
            auid_assumption = deepcopy(auid_assumption_query)
        else:
            auid_assumption = ProcessQuery()
        self.set_forward_edge_filter("auid_assumption", auid_assumption)
        auid_assumption.set_reverse_edge_filter("~auid_assumption", self, "auid_assumption")
        return self

    def query(
            self,
            dgraph_client: DgraphClient,
            contains_node_key: Optional[str] = None,
            first: Optional[int] = 1000,
    ) -> List["AuidView"]:
        return self._query(dgraph_client, contains_node_key, first)

    def query_first(
            self, dgraph_client: DgraphClient, contains_node_key: Optional[str] = None
    ) -> Optional["AuidView"]:
        return self._query_first(dgraph_client, contains_node_key)


class AuidView(DynamicNodeView):
    def __init__(
            self,
            dgraph_client: DgraphClient,
            node_key: str,
            uid: str,
            node_type: str,
            auid: Optional[int] = None,
            asset_id: Optional[str] = None,
    ):
        super(AuidView, self).__init__(
            dgraph_client=dgraph_client, node_key=node_key, uid=uid, node_type=node_type
        )
        self.node_type = node_type
        self.auid = auid
        self.asset_id = asset_id

    @staticmethod
    def _get_property_types() -> Mapping[str, "PropertyT"]:
        return {"src_pid": int, "dst_pid": int}

    @staticmethod
    def _get_forward_edge_types() -> Mapping[str, "EdgeViewT"]:
        f_edges = {"auid_assumption": ProcessView, "ipc_recipient": ProcessView}

        return {fe[0]: fe[1] for fe in f_edges.items() if fe[1]}

    def _get_forward_edges(self) -> "Mapping[str, ForwardEdgeView]":
        f_edges = {
            "auid_assumption": self.auid_assumption,
            "ipc_recipient": self.ipc_recipient
        }

        return {fe[0]: fe[1] for fe in f_edges.items() if fe[1]}

    def _get_properties(self, fetch: bool = False) -> Mapping[str, Union[str, int]]:
        props = {"src_pid": self.src_pid, "dst_pid": self.dst_pid}
        return {p[0]: p[1] for p in props.items() if p[1] is not None}
