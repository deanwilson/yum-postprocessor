from yum.plugins import PluginYumExit, TYPE_CORE, TYPE_INTERACTIVE
import subprocess

requires_api_version = "2.5"

plugin_type = (TYPE_INTERACTIVE,)


def config_hook(conduit):
    parser = conduit.getOptParser()
    parser.add_option(
        "",
        "--post-process",
        dest="postprocess",
        action="store_true",
        default=True,
        help="Run a command with change details everytime yum changes installed package state",
    )


def posttrans_hook(conduit):
    opts, commands = conduit.getCmdLine()

    command = conduit.confString("main", "command", default=None).split()

    if opts.postprocess:
        action = commands[0]
        packages = {}

        for transaction in conduit.getTsInfo():
            if transaction.name not in packages:
                packages[transaction.name] = {}

            packages[transaction.name]["action"] = action

            if action == "downgrade":
                if transaction.ts_state == "e":
                    packages[transaction.name]["current"] = transaction.version

                if transaction.ts_state == "u":
                    packages[transaction.name]["pending"] = transaction.version

            elif action == "update":
                if transaction.ts_state == "u":
                    packages[transaction.name]["pending"] = transaction.version

                if transaction.ts_state is None:
                    packages[transaction.name]["current"] = transaction.version

            else:
                packages[transaction.name]["pending"] = transaction.version

        for package in packages:
            if action in ["install", "remove", "erase", "reinstall", "localinstall"]:
                details = "action=%s name=%s version=%s" % (
                    packages[package]["action"],
                    package,
                    packages[package]["pending"],
                )
                command.append(details)

            if action in ["update", "downgrade"]:
                details = "action=%s name=%s version=%s pending=%s" % (
                    packages[package]["action"],
                    package,
                    packages[package]["current"],
                    packages[package]["pending"],
                )
                command.append(details)

            subprocess.call(command)
