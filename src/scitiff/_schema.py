# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2025 Ess-dmsc-dram contributors (https://github.com/ess-dmsc-dram)

from typing import Literal

from pydantic import BaseModel, Field

SCITIFF_IMAGE_STACK_DIMENSIONS = ("c", "t", "z", "y", "x")
"""The order of the dimensions in the image stack.

The order is from the fastest changing dimension to the slowest changing dimension.
i.e. image[0] is image stack of the first channel.
It is inherited from ImageJ Hyperstack.

"""


class ScippVariableMetadata(BaseModel):
    """Scipp Variable Metadata without the values."""

    dims: tuple[str, ...]
    shape: tuple[int, ...]
    unit: str
    dtype: str
    variance: list[float] | None = None


class ScippVariable(ScippVariableMetadata):
    """Scipp Variable Metadata with the values."""

    values: list[float]


class ImageVariableMetadata(ScippVariableMetadata):
    """Image Metadata."""

    dims: tuple[Literal["c"], Literal["t"], Literal["z"], Literal["y"], Literal["x"]]
    """Scitiff image stack has the fixed number and order of dimensions."""
    shape: tuple[int, int, int, int, int]


class ScippDataArrayMetadata(BaseModel):
    """Scipp DataArray Metadata without values(image)."""

    data: ScippVariableMetadata
    masks: dict[str, ScippVariable] = Field(default_factory=dict)
    coords: dict[str, ScippVariable] = Field(default_factory=dict)
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


class SciTiffMetadataContainer(BaseModel):
    """SCITIFF Compatible Metadata."""

    scitiffmeta: SciTiffMetadata


class SciTiff(BaseModel):
    """SCITIFF object."""

    metadata: SciTiffMetadata
    data: list
    """The image data in the order of the dimensions specified in the metadata."""


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

    # Dump scitiff schema
    scitiff_schema_path = (
        pathlib.Path(__file__).parent / "_resources/scitiff-schema.json"
    )
    scitiff_schema = SciTiff.model_json_schema()
    with open(scitiff_schema_path, "w") as f:
        json.dump(scitiff_schema, f, indent=2)
