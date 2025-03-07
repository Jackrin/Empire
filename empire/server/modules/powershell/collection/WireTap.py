from __future__ import print_function

from builtins import object, str
from typing import Dict

from empire.server.core.module_models import EmpireModule
from empire.server.utils.module_util import handle_error_message


class Module(object):
    @staticmethod
    def generate(
        main_menu,
        module: EmpireModule,
        params: Dict,
        obfuscate: bool = False,
        obfuscation_command: str = "",
    ):
        # read in the common module source code
        script, err = main_menu.modulesv2.get_module_source(
            module_name=module.script_path,
            obfuscate=obfuscate,
            obfuscate_command=obfuscation_command,
        )

        if err:
            return handle_error_message(err)

        script_end = 'Invoke-WireTap -Command "'

        # Add any arguments to the end execution of the script
        for option, values in params.items():
            if option.lower() != "agent":
                if values and values != "":
                    if values.lower() == "true":
                        # if we're just adding a switch
                        script_end += str(option)
                    elif option.lower() == "time":
                        # if we're just adding a switch
                        script_end += " " + str(values)
                    else:
                        script_end += " " + str(option) + " " + str(values)
        script_end += '"'

        script = main_menu.modulesv2.finalize_module(
            script=script,
            script_end=script_end,
            obfuscate=obfuscate,
            obfuscation_command=obfuscation_command,
        )
        return script
