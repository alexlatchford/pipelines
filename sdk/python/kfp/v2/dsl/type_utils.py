# Copyright 2020 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Utilities for component I/O type mapping."""

import textwrap
from typing import List, Optional
from kfp.components import structures
from kfp.v2.proto import pipeline_spec_pb2

# ComponentSpec I/O types to (IR) PipelineTaskSpec I/O types mapping.
# The keys are normalized (lowercased). These are types viewed as Artifacts.
# The values are the corresponding IR artifact type schemas.
_ARTIFACT_TYPES_MAPPING = {
    'gcspath': textwrap.dedent("""\
        title: kfp.Artifact
        type: object
        properties:
    """),
    'model': textwrap.dedent("""\
        title: kfp.Model
        type: object
        properties:
    """),
    'dataset':textwrap.dedent("""\
        title: kfp.Dataset
        type: object
        properties:
    """),
    'metrics':textwrap.dedent("""\
        title: kfp.Metrics
        type: object
        properties:
    """),
    'schema':textwrap.dedent("""\
        title: kfp.Schema
        type: object
        properties:
    """)
}

# ComponentSpec I/O types to (IR) PipelineTaskSpec I/O types mapping.
# The keys are normalized (lowercased). These are types viewed as Parameters.
# The values are the corresponding IR parameter primitive types.
_PARAMETER_TYPES_MAPPING = {
    'integer': pipeline_spec_pb2.PrimitiveType.INT,
    'int': pipeline_spec_pb2.PrimitiveType.INT,
    'double': pipeline_spec_pb2.PrimitiveType.DOUBLE,
    'float': pipeline_spec_pb2.PrimitiveType.DOUBLE,
}


def is_artifact_type(type_name: Optional[str]) -> bool:
  """Check if a ComponentSpec I/O type is considered as an artifact type.

  Args:
    type_name: type name of the ComponentSpec I/O type.

  Returns:
    True if the type name maps to an artifact type else False.
  """
  if not isinstance(type_name, str):
    return False
  return type_name.lower() in _ARTIFACT_TYPES_MAPPING


def get_artifact_type_schema(type_name: str) -> Optional[str]:
  """Get the IR I/O artifact type for the given ComponentSpec I/O type.

  Args:
    type_name: type name of the ComponentSpec I/O type.

  Returns:
     The string value of artifact type schema.

  Raises:
    AttributeError: if type_name os not a string type.
  """
  return _ARTIFACT_TYPES_MAPPING.get(type_name.lower())


def get_parameter_type(
    type_name: Optional[str]) -> pipeline_spec_pb2.PrimitiveType:
  """Get the IR I/O parameter type for the given ComponentSpec I/O type.

  Args:
    type_name: type name of the ComponentSpec I/O type.

  Returns:
    The enum value of the mapped IR I/O primitive type. Default to
    PrimitiveType.STRING for unrecognized type names.
  """
  if not isinstance(type_name, str):
    return pipeline_spec_pb2.PrimitiveType.STRING
  return _PARAMETER_TYPES_MAPPING.get(type_name.lower(),
                                      pipeline_spec_pb2.PrimitiveType.STRING)


def get_input_artifact_type_schema(
    input_name: str,
    inputs: List[structures.InputSpec],
) -> Optional[str]:
  """Find the input artifact type by input name.

  Args:
    input_name: The name of the component input.
    inputs: The list of InputSpec

  Returns:
    The input type schema if found in inputs, or None if not found.
  """
  for component_input in inputs:
    if component_input.name == input_name:
      return get_artifact_type_schema(component_input.type)
  return None
