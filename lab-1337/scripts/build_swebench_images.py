#!/usr/bin/env python3
"""Build SWE-bench Docker images for REP-002 tasks.

This script builds the required Docker images for running SWE-bench
evaluations. Images are built in layers:
1. Base images (ubuntu with python)
2. Environment images (repo-specific dependencies)
3. Instance images (specific commit checkout)

Usage:
    DOCKER_HOST=unix://~/.colima/default/docker.sock python scripts/build_swebench_images.py
"""

import docker
import logging
from datasets import load_dataset
from swebench.harness.docker_build import (
    build_base_images,
    build_env_images,
    build_instance_images,
    get_test_specs_from_dataset,
)
from swebench.harness.constants import SWEbenchInstance

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
log = logging.getLogger(__name__)

# Our REP-002 tasks
TASKS = [
    # Low ambiguity
    'sympy__sympy-13480',
    'pytest-dev__pytest-10051',
    'scikit-learn__scikit-learn-10297',
    'matplotlib__matplotlib-20488',
    'django__django-10554',
    # High ambiguity
    'django__django-10097',
    'django__django-11848',
    'astropy__astropy-13236',
    'astropy__astropy-13977',
    'django__django-11087',
]


def main():
    # Connect to Docker
    log.info("Connecting to Docker...")
    client = docker.from_env()
    log.info(f"Docker connected: {client.ping()}")

    # Load dataset
    log.info("Loading SWE-bench Verified dataset...")
    ds = load_dataset('princeton-nlp/SWE-bench_Verified', split='test')

    # Filter to our tasks
    instances = [item for item in ds if item['instance_id'] in TASKS]
    log.info(f"Found {len(instances)} instances to build")

    # Convert to SWEbenchInstance objects
    swebench_instances = [SWEbenchInstance(**item) for item in instances]

    # Get test specs (this figures out which images we need)
    log.info("Generating test specs...")
    test_specs = get_test_specs_from_dataset(
        swebench_instances,
        namespace=None,  # Use default namespace
        instance_image_tag='latest',
        env_image_tag='latest',
    )
    log.info(f"Generated {len(test_specs)} test specs")

    # Build base images first
    log.info("=" * 60)
    log.info("Step 1: Building base images...")
    log.info("=" * 60)
    build_base_images(
        client=client,
        dataset=swebench_instances,
        force_rebuild=False,
        namespace=None,
        instance_image_tag='latest',
        env_image_tag='latest',
    )
    log.info("Base images complete!")

    # Build environment images
    log.info("=" * 60)
    log.info("Step 2: Building environment images...")
    log.info("=" * 60)
    build_env_images(
        client=client,
        dataset=swebench_instances,
        force_rebuild=False,
        max_workers=2,  # Don't overwhelm
        namespace=None,
        instance_image_tag='latest',
        env_image_tag='latest',
    )
    log.info("Environment images complete!")

    # Build instance images
    log.info("=" * 60)
    log.info("Step 3: Building instance images...")
    log.info("=" * 60)
    build_instance_images(
        client=client,
        dataset=swebench_instances,
        force_rebuild=False,
        max_workers=2,
        namespace=None,
        tag='latest',
        env_image_tag='latest',
    )
    log.info("Instance images complete!")

    # List built images
    log.info("=" * 60)
    log.info("Built images:")
    log.info("=" * 60)
    images = client.images.list()
    swebench_images = [img for img in images if any('sweb' in tag for tag in img.tags)]
    for img in swebench_images:
        log.info(f"  {img.tags}")

    log.info("Done! You can now run the experiment with --grader swebench-docker")


if __name__ == '__main__':
    main()
