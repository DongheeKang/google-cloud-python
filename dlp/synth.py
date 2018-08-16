# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This script is used to synthesize generated parts of this library."""

import synthtool as s
import synthtool.gcp as gcp
import logging

logging.basicConfig(level=logging.DEBUG)

gapic = gcp.GAPICGenerator()
common = gcp.CommonTemplates()

client_library_version = '0.6.0'

library = gapic.py_library(
    'dlp', 'v2',
    config_path='/google/privacy/dlp/artman_dlp_v2.yaml')

s.copy(library, excludes=["README.rst", "nox.py"])

# Set Release Status
release_status = 'Development Status :: 3 - Alpha'
s.replace('setup.py',
          '(release_status = )(.*)$',
          f"\\1'{release_status}'")

# Set version
s.replace('setup.py', "version = .*", f"version = '{client_library_version}'")

# Fix namespace
s.replace('**/*.py', 'google\.cloud\.privacy\.dlp_v2', 'google.cloud.dlp_v2')

# Add changelog to index.rst
s.replace(
    'docs/index.rst',
    '    gapic/v2/types',
    '    gapic/v2/types\n    changelog\n')

# Add newlines to end of files
s.replace(
    ['google/__init__.py', 'google/cloud/__init__.py'],
    '__path__ = pkgutil.extend_path\(__path__, __name__\)',
    '\g<0>\n')

# Add missing utf-8 marker
s.replace(
    'google/cloud/dlp_v2/proto/dlp_pb2.py',
    '# Generated by the protocol buffer compiler.  DO NOT EDIT!',
    '# -*- coding: utf-8 -*-\n\g<0>')

# Fix unindentation of bullet list second line
s.replace(
    'google/cloud/dlp_v2/gapic/dlp_service_client.py',
    '(                \* .*\n                )([^\s*])',
    '\g<1>  \g<2>')

s.replace(
    'google/cloud/dlp_v2/gapic/dlp_service_client.py',
    '(\s+)\*.*\n\s+::\n\n',
    '\g<1>  ::\n')