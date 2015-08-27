from subprocess import call
import os

from flask.ext.script import Manager

from commands.utils import perform


def alt_exec(cmd, alt=None):
    """
    Tries to execute command.
    If command not found, it tries to execute the alternative comand
    """
    try:
        call(cmd)
    except OSError as e:
        if e.errno == os.errno.ENOENT and alt:
            try:
                call(alt)
            except OSError as ex:
                raise ex
        else:
            raise e


StaticCommand = Manager(usage='Commands to build static')


def npm():
    """ Run npm install script """
    with perform(
            name='static npm',
            before='run npm install',
    ):
        alt_exec(
            cmd=["npm", "install"],
        )


@StaticCommand.option(
    '--allow-root',
    dest='allow_root',
    default=False,
    help='Force scripts to allow execution by root user',
    action='store_true',
)
def bower(allow_root):
    """ Run bower install script """
    with perform(
            name='static bower',
            before='run bower install',
    ):
        cmd_args = list()
        if allow_root:
            cmd_args.append("--allow-root")

        alt_exec(
            cmd=["bower", "install"] + cmd_args,
            alt=["./node_modules/bower/bin/bower", "install"] + cmd_args,
        )


@StaticCommand.option(
    '--deploy-type',
    dest='deploy_type',
    default="production",
    help='Set deploy type '
         '(production with minifying, development without minifying etc.)'
)
def gulp(deploy_type=None):
    """ Run gulp build script """
    with perform(
            name='static gulp',
            before='run gulp',
    ):
        cmd_args = list()
        if deploy_type is not None:
            cmd_args.append("--type")
            cmd_args.append(deploy_type)

        alt_exec(
            cmd=["gulp"] + cmd_args,
            alt=["./node_modules/gulp/bin/gulp.js"] + cmd_args,
        )


@StaticCommand.option(
    '--allow-root',
    dest='allow_root',
    default=False,
    help='Force scripts to allow execution by root user',
    action='store_true',
)
@StaticCommand.option(
    '--deploy-type',
    dest='deploy_type',
    default="production",
    help='Set deploy type '
         '(production with minifying, development without minifying etc.)'
)
def collect(allow_root, deploy_type):
    npm()
    bower(allow_root)
    gulp(deploy_type)


@StaticCommand.command
def clean():
    """ Clean built static files """
    with perform(
            name='static clean',
            before='run gulp clean',
    ):
        alt_exec(
            cmd=["gulp", "clean"],
            alt=["./node_modules/gulp/bin/gulp.js", "clean"],
        )
