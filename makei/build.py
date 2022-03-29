#! /usr/bin/env python3

# Licensed Materials - Property of IBM
# 57XX-XXX
# (c) Copyright IBM Corp. 2021
""" The module used to build a project"""
from os import unlink
from pathlib import Path
from tempfile import mkstemp
from typing import Any, Dict, List, Optional
from makei.const import BOB_PATH
from makei.utils import objlib_to_path, read_ibmi_json, read_iproj_json, \
    run_command, support_color


class BuildEnv():
    """ The Build Environment used to build or compile a project. """

    color_tty: bool
    src_dir: Path
    targets: List[str]
    make_options: Optional[str]
    bob_path: Path
    bob_makefile: Path
    build_vars_path: Path
    build_vars_handle: Path
    curlib: str
    pre_usr_libl: str
    post_usr_libl: str
    includePath: str
    iproj_json_path: Path
    iproj_json: Dict[str, Any]
    ibmi_env_cmds: str

    def __init__(self, targets: List[str] = None, make_options: Optional[str] = None,
                 overrides: Dict[str, Any] = None):
        overrides = overrides or {}
        self.src_dir = Path.cwd()
        self.targets = targets if targets is not None else ["all"]
        self.make_options = make_options if make_options else ""
        self.bob_path = Path(
            overrides["bob_path"]) if "bob_path" in overrides else BOB_PATH
        self.bob_makefile = self.bob_path / 'mk' / 'Makefile'
        self.build_vars_handle, path = mkstemp()
        self.build_vars_path = Path(path)
        self.iproj_json_path = self.src_dir / "iproj.json"
        self.iproj_json = read_iproj_json(self.iproj_json_path)
        self.color = support_color()

        if "setIBMiEnvCmd" in self.iproj_json:
            cmd_list = self.iproj_json["setIBMiEnvCmd"]
            self.ibmi_env_cmds = "\\n".join(cmd_list)
        else:
            self.ibmi_env_cmds = ""

        self._create_build_vars()

    def __del__(self):
        self.build_vars_path.unlink()

    def generate_make_cmd(self):
        """ Returns the make command used to build the project."""
        cmd = f'make -k BUILDVARSMKPATH="{self.build_vars_path}"' + \
            f' -k BOB="{self.bob_path}" -f "{self.bob_makefile}"'
        if self.make_options:
            cmd = f"{cmd} {self.make_options}"
        cmd = f"{cmd} {' '.join(self.targets)}"
        return cmd

    def _create_build_vars(self):
        target_file_path = self.build_vars_path

        rules_mks = list(Path(".").rglob("Rules.mk"))
        subdirs = list(map(lambda x: x.parents[0], rules_mks))

        subdirs.sort(key=lambda x: len(x.parts))
        dir_var_map = {Path('.'): (
            self.iproj_json['objlib'], self.iproj_json['tgtCcsid'])}

        def map_ibmi_json_var(path):
            if path != Path("."):
                dir_var_map[path] = read_ibmi_json(
                    path / ".ibmi.json", dir_var_map[path.parents[0]])

        list(map(map_ibmi_json_var, subdirs))

        with target_file_path.open("w", encoding="utf8") as file:
            file.write('\n'.join(["# This file is generated by makei, DO NOT EDIT.",
                                  "# Modify .ibmi.json to override values",
                                  "",
                                  f"curlib := {self.iproj_json['curlib']}",
                                  f"preUsrlibl := {self.iproj_json['preUsrlibl']}",
                                  f"postUsrlibl := {self.iproj_json['postUsrlibl']}",
                                  f"INCDIR := {self.iproj_json['includePath']}",
                                  f"IBMiEnvCmd := {self.ibmi_env_cmds}",
                                  f"COLOR_TTY := {'true' if self.color else 'false'}",
                                  "",
                                  "",
                                  ]))

            for subdir in subdirs:
                file.write(
                    f"TGTCCSID_{subdir.absolute()} := {dir_var_map[subdir][1]}\n")
                file.write(
                    f"OBJPATH_{subdir.absolute()} := {objlib_to_path(dir_var_map[subdir][0])}\n")

            for rules_mk in rules_mks:
                with rules_mk.open('r') as rules_mk_file:
                    lines = rules_mk_file.readlines()
                    for line in lines:
                        line = line.rstrip()
                        if line and not line.startswith("#") \
                                and not "=" in line and not line.startswith((' ', '\t')):
                            file.write(
                                f"{line.split(':')[0]}_d := {rules_mk.parents[0].absolute()}\n")

    def make(self):
        """ Generate and execute the make command."""
        if (self.src_dir / ".logs" / "joblog.json").exists():
            (self.src_dir / ".logs" / "joblog.json").unlink()
        if (self.src_dir / ".logs" / "output.log").exists():
            (self.src_dir / ".logs" / "output.log").unlink()

        run_command(self.generate_make_cmd())
        self._post_make()

    def _post_make(self):
        event_files = list(Path(".evfevent").rglob("*.evfevent"))

        for filepath in event_files:
            with filepath.open() as file:
                line = file.read()
            line = line.replace(f'{Path.cwd()}/', '')
            with filepath.open("w") as file:
                file.write(line)
