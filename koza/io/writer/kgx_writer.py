from typing import Any, Iterable, Optional

from biolink_model_pydantic.model import Entity
from kgx.graph.nx_graph import NxGraph
from kgx.sink import Sink
from kgx.sink.json_sink import JsonSink
from kgx.sink.jsonl_sink import JsonlSink
from kgx.sink.tsv_sink import TsvSink
from kgx.source.graph_source import GraphSource
from kgx.transformer import Transformer

from koza.converter.kgx_converter import KGXConverter
from koza.io.writer.writer import KozaWriter
from koza.model.config.source_config import OutputFormat


class KGXWriter(KozaWriter):
    def __init__(
        self,
        output_dir: str,
        output_format: OutputFormat,
        source_name: str,
    ):
        self.output_dir = output_dir
        self.output_format = output_format
        self.source_name = source_name
        self.converter: KGXConverter = KGXConverter()
        self.transformer: Transformer = Transformer(stream=True)
        self.source: GraphSource = GraphSource()
        self.transformer.transform(
                input_args={
                    "format": "graph",
                    "graph": NxGraph()
                },
                output_args={
                    "filename": f"{self.output_dir}/{self.source_name}",
                    "stream": True,
                    "format": str(output_format).split(".")[1],
                    "finalize": False,
                    # TODO: these properties need to be expanded, probably passed in or (possibly) inferred
                    # TODO: based on which classes are used
                    "node_properties": ['id', 'category'],
                    "edge_properties": ['subject', 'predicate', 'object', 'relation']
                },
        )

    def write(self, *entities: Iterable[Entity]):

        (nodes, edges) = self.converter.convert(*entities)

        graph = NxGraph()

        for node in nodes:
            graph.add_node(node['id'], **node)
        for edge in edges:
            graph.add_edge(edge['subject'], edge['object'], edge['id'], **edge)

        self.transformer.process(self.source.parse(graph), self.transformer.sink)

    def finalize(self):
        self.transformer.sink.finalize()

    def writerow(self, row: Iterable[Any]) -> Optional[int]:
        pass

    def writerows(self, rows: Iterable[Iterable[Any]]) -> Optional[int]:
        pass
