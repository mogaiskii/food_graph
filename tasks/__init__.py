import os

import invoke


@invoke.task
def upgrade(ctx):
    with ctx.cd(os.getcwd()):
        ctx.run('alembic upgrade head', pty=True)


@invoke.task
def start(ctx):
    with ctx.cd(os.getcwd()):
        ctx.run('uvicorn main:app')
