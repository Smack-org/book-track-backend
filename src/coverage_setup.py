from fastapi import APIRouter
import os
import signal

router = APIRouter()


# We need this to shut down properly during the e2e testing procedure.
# Ensured that this endpoint is only available in testing environment.
@router.get("/die")
async def die():
    print("Received end of testing porcedure call, shutting down...")
    os.kill(os.getpid(), signal.SIGINT)
