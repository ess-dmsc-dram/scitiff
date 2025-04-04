# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Ess-dmsc-dram contributors (https://github.com/ess-dmsc-dram)

from typing import Literal

from pydantic import BaseModel, Field

SCITIFF_IMAGE_STACK_DIMENSIONS = ("t", "z", "c", "y", "x")
"""The order of the dimensions in the image stack.

The order is from the outermost dimension to the innermost dimension.
i.e. image[0] is image stack of the first channel.
i.e.2. image[1][0] is the first frame(t) of the second channel.
It is ImageJ Hyperstack default dimension order.

"""


class ScippVariableMetadata(BaseModel):
    """Scipp Variable Metadata without the values."""

    dims: tuple[str, ...]
    shape: tuple[int, ...]
    unit: str | None
    dtype: str


class ScippVariable(ScippVariableMetadata):
    """Scipp Variable Metadata with the values.

    Only 1D variable is allowed for metadata.
    """

    values: list[float] | list[str]
    """The values of the variable."""


class ImageVariableMetadata(ScippVariableMetadata):
    """Image Metadata."""

    dims: tuple[Literal["t"], Literal["z"], Literal["c"], Literal["y"], Literal["x"]]
    """Scitiff image stack has the fixed number and order of dimensions."""
    shape: tuple[int, int, int, int, int]
    """The shape of the image data."""


class ScippDataArrayMetadata(BaseModel):
    """Scipp DataArray Metadata without values(image)."""

    data: ScippVariableMetadata
    masks: dict[str, ScippVariable] = Field(default_factory=dict)
    """Only 1-dimensional masks are supported for metadata."""
    coords: dict[str, ScippVariable] = Field(default_factory=dict)
    """Only 1-dimensional coordinates are supported for metadata."""
    name: str | None = None


class ImageDataArrayMetadata(ScippDataArrayMetadata):
    """Image DataArray Metadata without values(image)."""

    data: ImageVariableMetadata


class ScippDataArray(ScippDataArrayMetadata):
    """Scipp DataArray Metadata with values(image)."""

    data: ScippVariable


class SciTiffMetadata(BaseModel):
    """SCITIFF Metadata."""

    image: ImageDataArrayMetadata
    schema_version: str = "{VERSION_PLACEHOLDER}"


class SciTiffMetadataContainer(BaseModel, extra="allow"):
    """SCITIFF Compatible Metadata."""

    scitiffmeta: SciTiffMetadata


def dump_schemas():
    """Dump all schemas to JSON files."""
    import json
    import pathlib

    # Dump metadata schema
    scitiff_metadata_schema = SciTiffMetadataContainer.model_json_schema()
    metadata_json_path = (
        pathlib.Path(__file__).parent / "_resources/metadata-schema.json"
    )
    with open(metadata_json_path, "w") as f:
        json.dump(scitiff_metadata_schema, f, indent=2)
