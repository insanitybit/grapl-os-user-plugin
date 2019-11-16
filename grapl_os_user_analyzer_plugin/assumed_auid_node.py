from copy import deepcopy
from typing import *

from grapl_analyzerlib.nodes.comparators import IntCmp, _int_cmps
from grapl_analyzerlib.nodes.types import PropertyT
from grapl_analyzerlib.nodes.viewable import EdgeViewT, ForwardEdgeView
from grapl_analyzerlib.prelude import DynamicNodeQuery, DynamicNodeView, ProcessQuery, ProcessView
from pydgraph import DgraphClient


class AssumedAuidQuery(DynamicNodeQuery):
    def __init__(self) -> None:
        super(AssumedAuidQuery, self).__init__("AssumedAssumedAuid", AssumedAuidView)

    def with_assumed_timestamp(self, eq=IntCmp, gt=IntCmp, lt=IntCmp) -> "AssumedAuidQuery":
        self.set_int_property_filter("assumed_timestamp", _int_cmps("assumed_timestamp", eq=eq, gt=gt, lt=lt))
        return self

    def with_assuming_process_id(self, eq=IntCmp, gt=IntCmp, lt=IntCmp) -> "AssumedAuidQuery":
        self.set_int_property_filter("assuming_process_id", _int_cmps("assuming_process_id", eq=eq, gt=gt, lt=lt))
        return self

    def with_auid(self, eq=IntCmp, gt=IntCmp, lt=IntCmp) -> "AssumedAuidQuery":
        self.set_int_property_filter("auid", _int_cmps("auid", eq=eq, gt=gt, lt=lt))
        return self

    def with_assumed_auid(
            self, assumed_auid_query: "Optional[AuidQuery]" = None
    ) -> "AssumedAuidQuery":
        if assumed_auid_query:
            assumed_auid = deepcopy(assumed_auid_query)
        else:
            assumed_auid = AuidQuery()
        self.set_forward_edge_filter("assumed_auid", assumed_auid)
        assumed_auid.set_reverse_edge_filter("~assumed_auid", self, "assumed_auid")
        return self

    def with_assuming_process(
            self, assuming_process_query: "Optional[ProcessQuery]" = None
    ) -> "AssumedAuidQuery":
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
    ) -> List["AssumedAuidView"]:
        return self._query(dgraph_client, contains_node_key, first)

    def query_first(
            self, dgraph_client: DgraphClient, contains_node_key: Optional[str] = None
    ) -> Optional["AssumedAuidView"]:
        return self._query_first(dgraph_client, contains_node_key)


class AssumedAuidView(DynamicNodeView):
    def __init__(
            self,
            dgraph_client: DgraphClient,
            node_key: str,
            uid: str,
            node_type: str,
            auid: Optional[int] = None,
            assuming_process_id: Optional[int] = None,
            assuming_process: Optional[ProcessQuery] = None,
            assumed_auid: Optional['AuidView'] = None,
    ):
        super(AssumedAuidView, self).__init__(
            dgraph_client=dgraph_client, node_key=node_key, uid=uid, node_type=node_type
        )
        self.node_type = node_type
        self.assuming_process_id = assuming_process_id
        self.assuming_process = assuming_process
        self.assumed_auid = assumed_auid

    @staticmethod
    def _get_property_types() -> Mapping[str, "PropertyT"]:
        return {
            "auid": int,
            "assuming_process_id": int,
        }

    @staticmethod
    def _get_forward_edge_types() -> Mapping[str, "EdgeViewT"]:
        f_edges = {"assuming_process": ProcessView, "assumed_auid": AuidView}

        return {fe[0]: fe[1] for fe in f_edges.items() if fe[1]}

    def _get_forward_edges(self) -> "Mapping[str, ForwardEdgeView]":
        f_edges = {
            "assuming_process": self.assuming_process,
            "assumed_auid": self.assumed_auid
        }

        return {fe[0]: fe[1] for fe in f_edges.items() if fe[1]}

    def _get_properties(self, fetch: bool = False) -> Mapping[str, Union[str, int]]:
        props = {
            "auid": self.auid,
            "assuming_process_id": self.assuming_process_id
        }

        return {p[0]: p[1] for p in props.items() if p[1] is not None}


from grapl_os_user_analyzer_plugin.auid_node import AuidQuery, AuidView