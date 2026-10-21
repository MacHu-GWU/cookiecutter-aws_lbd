# -*- coding: utf-8 -*-

"""
Convert the seed repo into a cookiecutter template.

Input: the git-visible files of the seed repo (``CCTPL_SEED_DIR``).
Output: ``tmp/cctpl/template/``, a complete cookiecutter template root.

Rules: ``.claude/skills/cctpl-base-cn/references/03-parameterization.md``.
"""

import re
import sys
import json
import tomllib

from cookiecutter_maker.api import Parameter, Maker

import cctpl

try:
    dir_seed = cctpl.get_seed_dir()
except cctpl.TaskError as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(1)

with open(dir_seed / "pyproject.toml", "rb") as f:
    _pyproject = tomllib.load(f)
with open(dir_seed / "mise.toml", "rb") as f:
    _mise_config = tomllib.load(f)

# Every environment of the seed deploys to the same region; it becomes one variable.
_ENV_CONFIG_FILES = [
    "config/config-dev.json5",
    "config/config-tst.json5",
    "config/config-prd.json5",
]
_CONSOLE_URL_FILES = ["mise.toml", "QUICK_LINKS.md"]
_aws_regions = {
    re.search(r'aws_region: "([^"]+)"', (dir_seed / path).read_text(encoding="utf-8")).group(1)
    for path in _ENV_CONFIG_FILES
}
assert len(_aws_regions) == 1, f"Every config-<env>.json5 must use one aws_region: {_aws_regions}"


class SeedValues:
    """Concrete values in the seed repo that become cookiecutter variables."""

    # --- identity
    package_name = "cookiecutter_aws_lbd_demo"
    package_name_slug = "cookiecutter-aws-lbd-demo"
    github_username = "MacHu-GWU"
    # Not a parameter: only scanned for leaks (UNIQUE_SEED_VALUES).
    pypi_username = "machugwu"

    # --- license
    license = "MIT"

    # --- author
    author = "Sanhe Hu"
    author_email = "husanhe@gmail.com"

    # --- versioning (read from the seed)
    version = _pyproject["project"]["version"]
    dev_python_version = _mise_config["tools"]["python"]

    # --- AWS (read from the seed)
    aws_region = _aws_regions.pop()

    # --- secret token fields
    github_token_field = "github.accounts.sh.users.sh.secrets.dev.value"


_parts = SeedValues.version.split(".")
assert len(_parts) == 3 and all(v.isdigit() for v in _parts), (
    f"Invalid version: {SeedValues.version}"
)

_HOME_SECRET_HELP = (
    "Read https://github.com/MacHu-GWU/home_secret_toml-project to learn how to "
    "set up your tokens using home_secret.toml"
)

# Files that link to the seed repo on GitHub as the reference implementation,
# such as ``github.com/MacHu-GWU/cookiecutter_aws_lbd_demo-project/blob/0.2.1/...``.
# The links must keep pointing at the seed, so package_name and github_username
# leave them alone.
_SEED_LINK_FILES = sorted(
    str(path.relative_to(dir_seed))
    for path in (dir_seed / ".claude/skills/pywf-aws-lbd-base").rglob("*.md")
    if "github.com/MacHu-GWU/cookiecutter_aws_lbd_demo-project"
    in path.read_text(encoding="utf-8")
)

# Files that only mention the maintainer's own projects (plugin marketplace,
# home_secret_toml, docfly, cdk_mate) and the template author's bio.
_MAINTAINER_LINK_FILES = [
    ".claude/settings.local.json.example",
    ".claude/skills/pypi-cdk_mate/SKILL.md",
    ".claude/skills/pypi-cdk_mate/ref/best-practices.md",
    ".claude/skills/pypi-cdk_mate/ref/public-api.md",
    ".claude/skills/pywf-oss-base/references/01-secrets.md",
    ".claude/skills/pywf-oss-base/references/14-docfly.md",
]

PARAMETERS = [
    # Also the config's project_name (config/config-shared.json5), from which
    # every AWS resource name derives, such as the stack names in the
    # generated <cdk-stack-tasks> block of mise.toml (package_name_slug).
    Parameter(
        selector=[SeedValues.package_name],
        name="package_name",
        default="your_package_name",
        prompt="Your Python package name, in snake case (e.g. my_package)",
        exclude=_SEED_LINK_FILES,
    ),
    Parameter(
        selector=[SeedValues.package_name_slug],
        name="package_name_slug",
        custom_placeholder="{{ cookiecutter.package_name | slugify }}",
        in_cookiecutter_json=False,
    ),
    # The seed also links to itself, to the maintainer's own projects, and
    # credits the template's author in AUTHORS.rst. Those must stay literal.
    Parameter(
        selector=[SeedValues.github_username],
        name="github_username",
        default="your_github_username",
        prompt="Your GitHub username, the owner of the new repo",
        exclude=[*_SEED_LINK_FILES, *_MAINTAINER_LINK_FILES, "AUTHORS.rst"],
    ),
    # Generic value: only the project license field in pyproject.toml.
    # That field is an SPDX expression (PEP 639) and setuptools refuses to
    # build with an invalid one, so every choice is a valid SPDX expression,
    # exactly the value written to pyproject.toml.
    Parameter(
        selector=[f'license = "{SeedValues.license}"', SeedValues.license],
        name="license",
        choice=["MIT", "AGPL-3.0-or-later", "LicenseRef-Proprietary"],
        prompt="Pick a license, as an SPDX expression for pyproject.toml, see https://choosealicense.com/ for details",
        include=["pyproject.toml"],
    ),
    # AUTHORS.rst is the template author's bio, kept as is (LEGAL_RESIDUES).
    Parameter(
        selector=[SeedValues.author],
        name="author",
        default="Firstname Lastname",
        prompt="Author name for pyproject.toml",
        exclude=["AUTHORS.rst"],
    ),
    Parameter(
        selector=[SeedValues.author_email],
        name="author_email",
        default="firstname.lastname@email.com",
        prompt="Author email for pyproject.toml",
    ),
    # Generic value: only the project version line in pyproject.toml.
    Parameter(
        selector=[f'version = "{SeedValues.version}"', SeedValues.version],
        name="version",
        default="0.1.1",
        prompt="Semantic Version, in {major}.{minor}.{micro} (e.g. 0.1.1)",
        include=["pyproject.toml"],
    ),
    # Generic value: only the dev Python pin in mise.toml.
    Parameter(
        selector=[
            f'python = "{SeedValues.dev_python_version}"',
            SeedValues.dev_python_version,
        ],
        name="dev_python_version",
        default=SeedValues.dev_python_version,
        prompt=f"Python version for local development, in {{major}}.{{minor}} (e.g. {SeedValues.dev_python_version})",
        include=["mise.toml"],
    ),
    # Generic value: only the aws_region field of each environment's config
    # (config/example/ keeps its placeholder) ...
    Parameter(
        selector=[f'aws_region: "{SeedValues.aws_region}"', SeedValues.aws_region],
        name="aws_region",
        default=SeedValues.aws_region,
        prompt=f"AWS region every environment (dev, tst, prd) deploys to (e.g. {SeedValues.aws_region})",
        include=_ENV_CONFIG_FILES,
    ),
    # ... and the console URLs in mise.toml (the generated <cdk-stack-tasks>
    # block; the seed's test_mise_toml_is_up_to_date fails if it and the config
    # disagree) and QUICK_LINKS.md (generated by gen-quick-links from config/).
    Parameter(
        selector=[
            f"https://{SeedValues.aws_region}.console.aws.amazon.com/",
            SeedValues.aws_region,
        ],
        name="aws_region",
        include=_CONSOLE_URL_FILES,
        in_cookiecutter_json=False,
    ),
    Parameter(
        selector=[f"region={SeedValues.aws_region}", SeedValues.aws_region],
        name="aws_region",
        include=_CONSOLE_URL_FILES,
        in_cookiecutter_json=False,
    ),
    Parameter(
        selector=[SeedValues.github_token_field],
        name="github_token_field",
        default="your_github_token_field",
        prompt=f"GitHub token field. {_HOME_SECRET_HELP}",
    ),
]

# Git-visible seed files that must not enter the template.
EXCLUDE = [
    "LICENSE.txt",  # generated by hooks/post_gen_project.py
    "uv.lock",  # carries the seed's own package name; generated projects re-lock
]

# Files copied byte for byte (no variable replacement).
NO_RENDER = [
    "*/vendor/**/*.*",
    "requirements.txt",
    "requirements-dev.txt",
    "requirements-doc.txt",
    "requirements-mise.txt",
    "requirements-test.txt",
    "*.jinja",
    "*.j2",
    "*.html",
]

# Choice variables whose values send hooks or the template down different
# branches. test-template generates once per extra choice value
# (03-parameterization.md, "Choice Coverage").
CHOICE_COVERAGE = [
    "license",  # hooks/post_gen_project.py writes a different LICENSE.txt per value
]

# Files the hooks create or rewrite in a generated project. check-roundtrip
# allows them to differ from the seed.
HOOK_OUTPUTS = [
    "LICENSE.txt",  # hooks/post_gen_project.py writes it from the chosen license
    # hooks/post_gen_project.py copies these from their examples; git-ignored in the seed
    ".env",
    "config/config-shared-secret.json5",
    "config/config-dev-secret.json5",
    "config/config-tst-secret.json5",
    "config/config-prd-secret.json5",
]

# Seed values unique enough that any occurrence left in the template is a
# leak, scanned by check-seed-values. Generic values (license, version,
# dev_python_version, aws_region) also appear legitimately elsewhere; check-roundtrip
# verifies them instead.
UNIQUE_SEED_VALUES = {
    "package_name": SeedValues.package_name,
    "package_name_slug": SeedValues.package_name_slug,
    "github_username": SeedValues.github_username,
    "pypi_username": SeedValues.pypi_username,
    "author": SeedValues.author,
    "author_email": SeedValues.author_email,
    "github_token_field": SeedValues.github_token_field,
}

_SEED_LINK = "links to the seed repo as the reference implementation, must stay literal"
_MAINTAINER_LINK = "links to the maintainer's own project, must stay literal"
_TEMPLATE_AUTHOR = "credits the template's author, not the generated project's"

# Unique seed values that may legally remain in the template, consumed by
# check-seed-values. Each entry: (seed value name, template-relative file, reason).
LEGAL_RESIDUES: list[tuple[str, str, str]] = [
    *[("package_name", path, _SEED_LINK) for path in _SEED_LINK_FILES],
    *[("github_username", path, _SEED_LINK) for path in _SEED_LINK_FILES],
    *[("github_username", path, _MAINTAINER_LINK) for path in _MAINTAINER_LINK_FILES],
    ("github_username", "AUTHORS.rst", _TEMPLATE_AUTHOR),
    ("pypi_username", "AUTHORS.rst", _TEMPLATE_AUTHOR),
    ("author", "AUTHORS.rst", _TEMPLATE_AUTHOR),
]


def get_seed_context() -> dict[str, str]:
    """
    The cookiecutter context that renders the template back into the seed.
    """
    return {
        p.name: getattr(SeedValues, p.name)
        for p in PARAMETERS
        if p.in_cookiecutter_json
    }


def add_template_version(path_json) -> None:
    """
    Record the tpl repo's own version as the private variable
    ``_template_version``: cookiecutter never prompts for it, but it is part of
    every generation's context. It goes right after the last prompted variable.
    """
    data = json.loads(path_json.read_text(encoding="utf-8"))
    result = {}
    for key, value in data.items():
        if key.startswith("_") and "_template_version" not in result:
            result["_template_version"] = cctpl.get_tpl_version()
        result[key] = value
    path_json.write_text(json.dumps(result, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    dir_stage_seed = cctpl.dir_stage / dir_seed.name
    cctpl.reset_dir(cctpl.dir_stage)
    n_files = cctpl.stage_git_visible_files(dir_seed, dir_stage_seed)
    print(f"Staged {n_files} git-visible files from {dir_seed}")

    if cctpl.dir_template.exists():
        cctpl.reset_dir(cctpl.dir_template)
        cctpl.dir_template.rmdir()
    maker = Maker(
        dir_input=dir_stage_seed,
        dir_output=cctpl.dir_template,
        parameters=PARAMETERS,
        exclude=EXCLUDE,
        no_render=NO_RENDER,
        dir_hooks=cctpl.dir_project_root / "hooks",
        verbose=False,
    )
    maker.make_template()
    add_template_version(maker.path_cookiecutter_json)
    print(f"Template written to {cctpl.dir_template}")
    return 0


if __name__ == "__main__":
    cctpl.run_task(main)
